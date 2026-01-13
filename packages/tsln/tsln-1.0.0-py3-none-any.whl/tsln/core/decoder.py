"""TSLN Decoder - Decode TSLN format back to data points."""
import json
from datetime import datetime, timedelta
from typing import Any, Dict, List, Optional, Tuple

from ..types import (
    TSLN_ESCAPED_SEPARATOR,
    TSLN_NULL,
    TSLN_REPEAT,
    TSLN_SEPARATOR,
    BufferedDataPoint,
    TSLNFieldType,
    TSLNSchema,
)
from .schema import parse_schema_header


def decode_tsln(tsln_string: str) -> List[Dict[str, Any]]:
    """Decode TSLN string back to data points.

    Args:
        tsln_string: TSLN formatted string

    Returns:
        List of decoded data points (dictionaries with 'timestamp' and 'data' keys)
    """
    lines = tsln_string.split("\n")
    if len(lines) == 0:
        raise ValueError("Empty TSLN string")

    # Parse header
    schema, data_start_line = _parse_header(lines)

    # Parse data rows
    data_points: List[Dict[str, Any]] = []
    previous_encoded_values: List[str] = []
    previous_decoded_values: List[Any] = []

    for i in range(data_start_line, len(lines)):
        line = lines[i].strip()
        if not line or line.startswith("#"):
            continue

        values = line.split(TSLN_SEPARATOR)
        expected_fields = len(schema.fields) + 1  # +1 for timestamp

        if len(values) != expected_fields:
            raise ValueError(
                f"Line {i + 1}: expected {expected_fields} fields, got {len(values)}"
            )

        # Decode timestamp
        timestamp = _decode_timestamp(
            values[0],
            schema.base_timestamp,
            schema.timestamp_mode,
            schema.expected_interval,
            len(data_points),
        )

        # Decode data fields
        data: Dict[str, Any] = {}
        current_decoded_values: List[Any] = []

        for j, field in enumerate(schema.fields):
            prev_encoded = previous_encoded_values[j] if j < len(previous_encoded_values) else ""
            prev_decoded = previous_decoded_values[j] if j < len(previous_decoded_values) else None

            # Decode value using both encoded previous and decoded previous
            value = _decode_value_with_context(
                values[j + 1], prev_encoded, prev_decoded, field.type
            )

            current_decoded_values.append(value)

            # Unflatten if nested
            _set_nested_value(data, field.name, value)

        # Format timestamp to match input format (always UTC with Z suffix)
        if timestamp.tzinfo is not None:
            # Remove timezone info and use Z suffix
            timestamp_str = timestamp.replace(tzinfo=None).isoformat() + "Z"
        else:
            timestamp_str = timestamp.isoformat() + "Z"
        data_points.append({"timestamp": timestamp_str, "data": data})

        previous_encoded_values = values[1:]
        previous_decoded_values = current_decoded_values

    return data_points


def _parse_header(lines: List[str]) -> Tuple[TSLNSchema, int]:
    """Parse TSLN header and return schema.

    Args:
        lines: Lines from TSLN file

    Returns:
        Tuple of (schema, data_start_line)
    """
    header_lines: List[str] = []
    data_start_line = 0

    for i, line in enumerate(lines):
        line = line.strip()

        if line == "---":
            data_start_line = i + 1
            break

        if line.startswith("#"):
            header_lines.append(line)

    if data_start_line == 0:
        raise ValueError("No data separator (---) found in TSLN")

    schema = parse_schema_header(header_lines)
    return schema, data_start_line


def _decode_timestamp(
    value: str,
    base_time: Optional[datetime],
    mode: str,
    expected_interval: Optional[int],
    index: int,
) -> datetime:
    """Decode timestamp value.

    Args:
        value: Encoded timestamp string
        base_time: Base timestamp
        mode: Timestamp mode (delta/interval/absolute)
        expected_interval: Expected interval in milliseconds
        index: Data point index

    Returns:
        Decoded datetime object
    """
    if not value:
        raise ValueError("Empty timestamp value")

    if mode == "interval":
        if base_time is None:
            raise ValueError("Base timestamp required for interval mode")
        if expected_interval is None:
            raise ValueError("Expected interval required for interval mode")

        # Parse index and deviation
        if "+" in value:
            parts = value.split("+", 1)
            idx = int(parts[0])
            deviation = int(parts[1])
            expected_time = base_time + timedelta(milliseconds=idx * expected_interval)
            return expected_time + timedelta(milliseconds=deviation)
        elif value.count("-") > 0 and value != "0":
            # Find the last - which indicates deviation
            for i in range(len(value) - 1, 0, -1):
                if value[i] == "-":
                    idx = int(value[:i])
                    deviation = int(value[i:])
                    expected_time = base_time + timedelta(milliseconds=idx * expected_interval)
                    return expected_time + timedelta(milliseconds=deviation)

        # Just index
        idx = int(value)
        return base_time + timedelta(milliseconds=idx * expected_interval)

    elif mode == "delta":
        if base_time is None:
            raise ValueError("Base timestamp required for delta mode")

        delta_ms = int(value)
        return base_time + timedelta(milliseconds=delta_ms)

    elif mode == "absolute":
        # Parse absolute timestamp
        return datetime.fromisoformat(value.replace("Z", "+00:00"))

    else:
        raise ValueError(f"Unknown timestamp mode: {mode}")


def _decode_value_with_context(
    value: str, prev_encoded: str, prev_decoded: Any, field_type: TSLNFieldType
) -> Any:
    """Decode a field value with context of both encoded and decoded previous values.

    Args:
        value: Current encoded value string
        prev_encoded: Previous encoded value string
        prev_decoded: Previous decoded value (actual value, not string)
        field_type: Field type

    Returns:
        Decoded value
    """
    # Handle null
    if value == TSLN_NULL or value == "":
        return None

    # Handle repeat marker
    if value == TSLN_REPEAT:
        return prev_decoded

    # Handle boolean
    if field_type == TSLNFieldType.BOOL:
        if value == "1":
            return True
        if value == "0":
            return False
        return bool(value)

    # Handle numeric types
    if field_type in (TSLNFieldType.FLOAT, TSLNFieldType.INT):
        # Check for differential encoding
        if value.startswith(("+", "-")):
            if prev_decoded is None:
                raise ValueError("Differential value without previous value")

            try:
                diff = float(value)
            except ValueError:
                raise ValueError(f"Failed to parse differential: {value}")

            result = float(prev_decoded) + diff
            return int(result) if field_type == TSLNFieldType.INT and result == int(result) else result

        # Absolute value
        try:
            num = float(value)
            return int(num) if field_type == TSLNFieldType.INT and num == int(num) else num
        except ValueError:
            raise ValueError(f"Failed to parse number: {value}")

    # Handle arrays
    if field_type == TSLNFieldType.ARRAY:
        if value.startswith("[") and value.endswith("]"):
            array_content = value[1:-1]
            if not array_content:
                return []
            items = array_content.split(",")
            decoded_items = []
            for item in items:
                item = item.strip()
                if item == TSLN_NULL:
                    decoded_items.append(None)
                elif item == "1" or item.lower() == "true":
                    decoded_items.append(True)
                elif item == "0" or item.lower() == "false":
                    decoded_items.append(False)
                else:
                    try:
                        decoded_items.append(float(item) if "." in item else int(item))
                    except ValueError:
                        decoded_items.append(item)
            return decoded_items
        return []

    # Handle objects
    if field_type == TSLNFieldType.OBJECT:
        try:
            restored = value.replace(TSLN_ESCAPED_SEPARATOR, TSLN_SEPARATOR)
            return json.loads(restored)
        except json.JSONDecodeError:
            return value

    # String types - restore pipe character
    return value.replace(TSLN_ESCAPED_SEPARATOR, TSLN_SEPARATOR)


def _decode_value(
    value: str, previous_value: str, field_type: TSLNFieldType
) -> Any:
    """Decode a field value.

    Args:
        value: Encoded value string
        previous_value: Previous value string
        field_type: Field type

    Returns:
        Decoded value
    """
    # Handle null
    if value == TSLN_NULL or value == "":
        return None

    # Handle repeat marker
    if value == TSLN_REPEAT:
        if not previous_value or previous_value == TSLN_NULL:
            return None
        # Decode previous value recursively
        return _decode_value(previous_value, "", field_type)

    # Handle boolean
    if field_type == TSLNFieldType.BOOL:
        if value == "1":
            return True
        if value == "0":
            return False
        return bool(value)

    # Handle numeric types
    if field_type in (TSLNFieldType.FLOAT, TSLNFieldType.INT):
        # Check for differential encoding
        if value.startswith(("+", "-")):
            if not previous_value:
                raise ValueError("Differential value without previous value")

            try:
                prev_num = float(previous_value)
            except ValueError:
                raise ValueError(f"Failed to parse previous value: {previous_value}")

            try:
                diff = float(value)
            except ValueError:
                raise ValueError(f"Failed to parse differential: {value}")

            result = prev_num + diff
            return int(result) if field_type == TSLNFieldType.INT and result == int(result) else result

        # Absolute value
        try:
            num = float(value)
            return int(num) if field_type == TSLNFieldType.INT and num == int(num) else num
        except ValueError:
            raise ValueError(f"Failed to parse number: {value}")

    # Handle arrays
    if field_type == TSLNFieldType.ARRAY:
        if value.startswith("[") and value.endswith("]"):
            array_content = value[1:-1]
            if not array_content:
                return []
            items = array_content.split(",")
            decoded_items = []
            for item in items:
                item = item.strip()
                if item == TSLN_NULL:
                    decoded_items.append(None)
                elif item == "1" or item.lower() == "true":
                    decoded_items.append(True)
                elif item == "0" or item.lower() == "false":
                    decoded_items.append(False)
                else:
                    try:
                        decoded_items.append(float(item) if "." in item else int(item))
                    except ValueError:
                        decoded_items.append(item)
            return decoded_items
        return []

    # Handle objects
    if field_type == TSLNFieldType.OBJECT:
        try:
            restored = value.replace(TSLN_ESCAPED_SEPARATOR, TSLN_SEPARATOR)
            return json.loads(restored)
        except json.JSONDecodeError:
            return value

    # String types - restore pipe character
    return value.replace(TSLN_ESCAPED_SEPARATOR, TSLN_SEPARATOR)


def _set_nested_value(data: Dict[str, Any], key: str, value: Any) -> None:
    """Set a value in a nested dictionary using dot notation.

    Args:
        data: Dictionary to set value in
        key: Key (potentially with dots for nesting)
        value: Value to set
    """
    if "." not in key:
        data[key] = value
        return

    parts = key.split(".", 1)
    first_key = parts[0]
    rest_key = parts[1]

    if first_key not in data:
        data[first_key] = {}

    if isinstance(data[first_key], dict):
        _set_nested_value(data[first_key], rest_key, value)
    else:
        # If not a dict, overwrite it
        data[first_key] = {}
        _set_nested_value(data[first_key], rest_key, value)
