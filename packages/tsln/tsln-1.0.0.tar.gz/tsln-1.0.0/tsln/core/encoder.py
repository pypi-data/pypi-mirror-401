"""TSLN Encoder - Convert data points to TSLN format."""
import json
import time
from datetime import datetime
from typing import Any, Dict, List, Optional

from ..types import (
    TSLN_ESCAPED_SEPARATOR,
    TSLN_NULL,
    TSLN_REPEAT,
    TSLN_SEPARATOR,
    BufferedDataPoint,
    TSLNOptions,
    TSLNResult,
    TSLNSchema,
    TSLNSchemaField,
    TSLNStatistics,
)
from .analyzer import analyze_dataset
from .schema import generate_schema, generate_schema_header


def convert_to_tsln(
    data_points: List[BufferedDataPoint], options: Optional[TSLNOptions] = None
) -> TSLNResult:
    """Convert data points to TSLN format.

    Args:
        data_points: List of timestamped data points
        options: Encoding options

    Returns:
        TSLNResult with encoded string, schema, analysis, and statistics
    """
    if options is None:
        options = TSLNOptions()

    start_time = time.perf_counter()

    if len(data_points) == 0:
        empty_result = "# TSLN: No data\n"
        from .analyzer import DatasetAnalysis

        return TSLNResult(
            tsln=empty_result,
            schema=TSLNSchema(),
            analysis=DatasetAnalysis(
                total_points=0,
                field_analyses={},
                has_timestamp=False,
                dataset_volatility=0.0,
                compression_potential=0.0,
            ),
            statistics=TSLNStatistics(
                original_size=0,
                tsln_size=len(empty_result),
                compression_ratio=0.0,
                estimated_tokens=0,
                estimated_token_savings=0,
                encoding_time_ms=0.0,
            ),
        )

    # Analyze dataset
    analysis = analyze_dataset(data_points)

    # Generate schema
    schema = generate_schema(
        analysis,
        max_fields=options.max_fields,
        prioritize_compression=options.prioritize_compression,
    )

    # Override schema settings with options
    if options.timestamp_mode:
        schema.timestamp_mode = options.timestamp_mode
    if options.base_timestamp:
        schema.base_timestamp = options.base_timestamp
    schema.enable_differential = options.enable_differential
    schema.enable_repeat_markers = options.enable_repeat_markers
    schema.enable_run_length = options.enable_run_length

    # Convert to TSLN string
    lines: List[str] = []

    # Header
    lines.append(generate_schema_header(schema))
    lines.append(f"# Count: {len(data_points)}")
    lines.append("---")

    # Determine base timestamp
    if schema.base_timestamp:
        base_time_dt = schema.base_timestamp
    else:
        base_time_dt = datetime.fromisoformat(data_points[0].timestamp.replace("Z", "+00:00"))

    base_time_ms = int(base_time_dt.timestamp() * 1000)

    previous_values: Dict[str, Any] = {}

    # Data rows
    for i, point in enumerate(data_points):
        current_time_dt = datetime.fromisoformat(point.timestamp.replace("Z", "+00:00"))
        current_time_ms = int(current_time_dt.timestamp() * 1000)
        flattened = _flatten_object(point.data)

        row_values: List[str] = []

        # Timestamp encoding
        timestamp_value = _encode_timestamp(
            current_time_ms,
            base_time_ms,
            schema.timestamp_mode,
            schema.expected_interval,
            i,
        )
        row_values.append(timestamp_value)

        # Field values
        for field in schema.fields:
            current_value = flattened.get(field.name)
            previous_value = previous_values.get(field.name)

            encoded_value = _encode_value(
                current_value,
                previous_value,
                field,
                precision=options.precision,
                max_string_length=options.max_string_length,
                enable_differential=options.enable_differential,
                enable_repeat_markers=options.enable_repeat_markers,
            )

            row_values.append(encoded_value)

            # Update previous values
            previous_values[field.name] = current_value

        lines.append(TSLN_SEPARATOR.join(row_values))

    tsln_string = "\n".join(lines)

    # Calculate statistics
    original_size = len(json.dumps([{"timestamp": p.timestamp, "data": p.data} for p in data_points]))
    tsln_size = len(tsln_string)
    compression_ratio = (original_size - tsln_size) / original_size if original_size > 0 else 0.0
    estimated_tokens = (tsln_size + 3) // 4  # Rough estimation: 1 token ≈ 4 characters
    original_tokens = (original_size + 3) // 4
    estimated_token_savings = original_tokens - estimated_tokens

    encoding_time_ms = (time.perf_counter() - start_time) * 1000

    return TSLNResult(
        tsln=tsln_string,
        schema=schema,
        analysis=analysis,
        statistics=TSLNStatistics(
            original_size=original_size,
            tsln_size=tsln_size,
            compression_ratio=compression_ratio,
            estimated_tokens=estimated_tokens,
            estimated_token_savings=estimated_token_savings,
            encoding_time_ms=encoding_time_ms,
            field_count=len(schema.fields),
            point_count=len(data_points),
        ),
    )


def _encode_timestamp(
    current_time_ms: int,
    base_time_ms: int,
    mode: str,
    expected_interval: Optional[int],
    index: int,
) -> str:
    """Encode timestamp based on mode.

    Args:
        current_time_ms: Current timestamp in milliseconds
        base_time_ms: Base timestamp in milliseconds
        mode: Timestamp encoding mode (delta/interval/absolute)
        expected_interval: Expected interval in milliseconds
        index: Data point index

    Returns:
        Encoded timestamp string
    """
    if mode == "interval":
        # Just use index if regular interval
        if expected_interval is not None:
            expected_time_ms = base_time_ms + (index * expected_interval)
            deviation = current_time_ms - expected_time_ms

            # If within 5% of expected, just use index
            if abs(deviation) < expected_interval * 0.05:
                return str(index)

            # Otherwise, show deviation: index+deviation or index-deviation
            if deviation > 0:
                return f"{index}+{deviation:.0f}"
            else:
                return f"{index}{deviation:.0f}"

        return str(index)

    elif mode == "delta":
        # Time since base (in ms)
        delta = current_time_ms - base_time_ms
        return str(delta)

    else:  # absolute
        # Full ISO timestamp
        return datetime.fromtimestamp(current_time_ms / 1000).isoformat() + "Z"


def _encode_value(
    current_value: Any,
    previous_value: Any,
    field: TSLNSchemaField,
    precision: int,
    max_string_length: Optional[int],
    enable_differential: bool,
    enable_repeat_markers: bool,
) -> str:
    """Encode a field value based on type and previous value.

    Args:
        current_value: Current field value
        previous_value: Previous field value
        field: Schema field definition
        precision: Decimal precision for floats
        max_string_length: Maximum string length
        enable_differential: Whether differential encoding is enabled
        enable_repeat_markers: Whether repeat markers are enabled

    Returns:
        Encoded value string
    """
    # Null/undefined
    if current_value is None:
        return TSLN_NULL

    # Repeat marker (if enabled and value unchanged)
    if (
        enable_repeat_markers
        and current_value == previous_value
        and previous_value is not None
    ):
        return TSLN_REPEAT

    # Boolean
    if isinstance(current_value, bool):
        return "1" if current_value else "0"

    # Number
    if isinstance(current_value, (int, float)):
        # Differential encoding for numeric values
        if (
            enable_differential
            and field.use_differential
            and isinstance(previous_value, (int, float))
        ):
            diff = current_value - previous_value

            # If difference is small, use differential
            if abs(diff) < abs(current_value) * 0.5:
                if diff == 0:
                    return TSLN_REPEAT
                elif diff > 0:
                    return f"+{_format_number(diff, precision)}"
                else:
                    return _format_number(diff, precision)  # Negative sign included

        # Otherwise, full value
        return _format_number(current_value, precision)

    # String
    if isinstance(current_value, str):
        str_val = current_value
        if max_string_length and len(str_val) > max_string_length:
            str_val = str_val[:max_string_length] + "…"
        # Escape pipe character
        return str_val.replace(TSLN_SEPARATOR, TSLN_ESCAPED_SEPARATOR)

    # Array
    if isinstance(current_value, list):
        encoded_items = [_encode_simple_value(v, precision) for v in current_value]
        return "[" + ",".join(encoded_items) + "]"

    # Object/Dict
    if isinstance(current_value, dict):
        return json.dumps(current_value).replace(TSLN_SEPARATOR, TSLN_ESCAPED_SEPARATOR)

    return str(current_value)


def _format_number(value: float, precision: int) -> str:
    """Format number with appropriate precision.

    Args:
        value: Numeric value
        precision: Decimal precision

    Returns:
        Formatted number string
    """
    if isinstance(value, int) or value == int(value):
        return str(int(value))
    return f"{value:.{precision}f}"


def _encode_simple_value(value: Any, precision: int) -> str:
    """Encode simple value for arrays.

    Args:
        value: Value to encode
        precision: Decimal precision

    Returns:
        Encoded value string
    """
    if value is None:
        return TSLN_NULL
    if isinstance(value, bool):
        return "1" if value else "0"
    if isinstance(value, (int, float)):
        return _format_number(value, precision)
    if isinstance(value, str):
        # Remove problematic characters for CSV-like arrays
        return value.replace(",", "").replace("[", "").replace("]", "")
    return str(value)


def _flatten_object(obj: Any, prefix: str = "") -> Dict[str, Any]:
    """Flatten nested objects with dot notation.

    Args:
        obj: Object to flatten
        prefix: Prefix for nested keys

    Returns:
        Flattened dictionary
    """
    flattened: Dict[str, Any] = {}

    if not isinstance(obj, dict):
        return {prefix: obj} if prefix else {}

    for key, value in obj.items():
        new_key = f"{prefix}.{key}" if prefix else key

        if value is None:
            flattened[new_key] = value
        elif isinstance(value, list):
            flattened[new_key] = value  # Keep arrays intact
        elif isinstance(value, dict):
            flattened.update(_flatten_object(value, new_key))
        else:
            flattened[new_key] = value

    return flattened


def estimate_tsln_tokens(tsln_string: str) -> int:
    """Estimate token count for TSLN format.

    Args:
        tsln_string: TSLN formatted string

    Returns:
        Estimated number of LLM tokens
    """
    # Rough estimation: 1 token ≈ 4 characters
    return (len(tsln_string) + 3) // 4
