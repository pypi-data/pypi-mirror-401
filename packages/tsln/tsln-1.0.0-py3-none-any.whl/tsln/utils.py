"""Utility functions for TSLN package."""
import csv
import io
import json
import time
import xml.etree.ElementTree as ET
from typing import Any, Dict, List

from .types import BufferedDataPoint, FormatComparison


def compare_formats(data_points: List[BufferedDataPoint]) -> Dict[str, FormatComparison]:
    """Compare TSLN with JSON, CSV, and XML formats.

    Args:
        data_points: List of data points to compare

    Returns:
        Dictionary with comparison results for each format
    """
    if not data_points:
        return {}

    # Import here to avoid circular dependency
    from .core.encoder import convert_to_tsln

    # JSON format
    json_start = time.perf_counter()
    json_data = [{"timestamp": p.timestamp, "data": p.data} for p in data_points]
    json_str = json.dumps(json_data)
    json_time_ms = (time.perf_counter() - json_start) * 1000
    json_size = len(json_str)
    json_tokens = (json_size + 3) // 4

    # CSV format
    csv_start = time.perf_counter()
    csv_str = _convert_to_csv(data_points)
    csv_time_ms = (time.perf_counter() - csv_start) * 1000
    csv_size = len(csv_str)
    csv_tokens = (csv_size + 3) // 4

    # XML format
    xml_start = time.perf_counter()
    xml_str = _convert_to_xml(data_points)
    xml_time_ms = (time.perf_counter() - xml_start) * 1000
    xml_size = len(xml_str)
    xml_tokens = (xml_size + 3) // 4

    # TSLN format
    tsln_result = convert_to_tsln(data_points)
    tsln_size = tsln_result.statistics.tsln_size
    tsln_tokens = tsln_result.statistics.estimated_tokens
    tsln_time_ms = tsln_result.statistics.encoding_time_ms

    # Calculate compression percentages
    json_compression = 0.0
    csv_compression = ((json_size - csv_size) / json_size * 100) if json_size > 0 else 0.0
    xml_compression = ((json_size - xml_size) / json_size * 100) if json_size > 0 else 0.0
    tsln_compression = ((json_size - tsln_size) / json_size * 100) if json_size > 0 else 0.0

    return {
        "json": FormatComparison(
            format_name="JSON",
            size_bytes=json_size,
            estimated_tokens=json_tokens,
            compression_vs_json=json_compression,
            encoding_time_ms=json_time_ms,
        ),
        "csv": FormatComparison(
            format_name="CSV",
            size_bytes=csv_size,
            estimated_tokens=csv_tokens,
            compression_vs_json=csv_compression,
            encoding_time_ms=csv_time_ms,
        ),
        "xml": FormatComparison(
            format_name="XML",
            size_bytes=xml_size,
            estimated_tokens=xml_tokens,
            compression_vs_json=xml_compression,
            encoding_time_ms=xml_time_ms,
        ),
        "tsln": FormatComparison(
            format_name="TSLN",
            size_bytes=tsln_size,
            estimated_tokens=tsln_tokens,
            compression_vs_json=tsln_compression,
            encoding_time_ms=tsln_time_ms,
        ),
    }


def _convert_to_csv(data_points: List[BufferedDataPoint]) -> str:
    """Convert data points to CSV format.

    Args:
        data_points: List of data points

    Returns:
        CSV formatted string
    """
    if not data_points:
        return ""

    output = io.StringIO()
    writer = csv.writer(output)

    # Flatten first point to get headers
    first_flattened = _flatten_dict(data_points[0].data)
    headers = ["timestamp"] + list(first_flattened.keys())
    writer.writerow(headers)

    # Write data rows
    for point in data_points:
        flattened = _flatten_dict(point.data)
        row = [point.timestamp] + [flattened.get(h, "") for h in headers[1:]]
        writer.writerow(row)

    return output.getvalue()


def _convert_to_xml(data_points: List[BufferedDataPoint]) -> str:
    """Convert data points to XML format.

    Args:
        data_points: List of data points

    Returns:
        XML formatted string
    """
    root = ET.Element("data")

    for point in data_points:
        point_elem = ET.SubElement(root, "point")
        point_elem.set("timestamp", point.timestamp)

        _dict_to_xml(point.data, point_elem)

    return ET.tostring(root, encoding="unicode")


def _dict_to_xml(data: Dict[str, Any], parent: ET.Element) -> None:
    """Convert dictionary to XML elements.

    Args:
        data: Dictionary to convert
        parent: Parent XML element
    """
    for key, value in data.items():
        # Sanitize key for XML
        key = key.replace(".", "_").replace(" ", "_")

        if isinstance(value, dict):
            child = ET.SubElement(parent, key)
            _dict_to_xml(value, child)
        elif isinstance(value, list):
            child = ET.SubElement(parent, key)
            for item in value:
                item_elem = ET.SubElement(child, "item")
                item_elem.text = str(item)
        else:
            child = ET.SubElement(parent, key)
            child.text = str(value) if value is not None else ""


def _flatten_dict(d: Dict[str, Any], parent_key: str = "", sep: str = ".") -> Dict[str, Any]:
    """Flatten nested dictionary.

    Args:
        d: Dictionary to flatten
        parent_key: Parent key for nesting
        sep: Separator for nested keys

    Returns:
        Flattened dictionary
    """
    items: List[tuple] = []
    for k, v in d.items():
        new_key = f"{parent_key}{sep}{k}" if parent_key else k
        if isinstance(v, dict):
            items.extend(_flatten_dict(v, new_key, sep=sep).items())
        else:
            items.append((new_key, v))
    return dict(items)


def print_comparison_table(comparison: Dict[str, FormatComparison]) -> None:
    """Print a formatted comparison table.

    Args:
        comparison: Comparison results from compare_formats()
    """
    print("\n+--------+-----------+----------+-----------------+--------------+")
    print("| Format | Size (B)  | Tokens   | vs JSON (%)     | Time (ms)    |")
    print("+--------+-----------+----------+-----------------+--------------+")

    for fmt_name in ["json", "csv", "xml", "tsln"]:
        if fmt_name not in comparison:
            continue

        fmt = comparison[fmt_name]
        print(
            f"| {fmt.format_name:<6} | {fmt.size_bytes:>9} | {fmt.estimated_tokens:>8} | "
            f"{fmt.compression_vs_json:>+14.1f}% | {fmt.encoding_time_ms:>12.2f} |"
        )

    print("+--------+-----------+----------+-----------------+--------------+\n")
