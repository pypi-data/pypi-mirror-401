"""TSLN Schema Management - Generates and optimizes schemas for TSLN encoding."""
from typing import Dict, List, Optional

from ..types import (
    DatasetAnalysis,
    FieldTypeAnalysis,
    TSLNFieldType,
    TSLNSchema,
    TSLNSchemaField,
    TimestampMode,
)


def generate_schema(
    analysis: DatasetAnalysis,
    max_fields: int = 50,
    prioritize_compression: bool = True,
) -> TSLNSchema:
    """Generate optimal TSLN schema from dataset analysis.

    Args:
        analysis: Dataset analysis results
        max_fields: Maximum number of fields to include
        prioritize_compression: Whether to optimize field order for compression

    Returns:
        TSLNSchema with optimized field ordering and configuration
    """
    schema_fields: List[TSLNSchemaField] = []
    position = 0

    # Sort fields for optimal ordering
    sorted_fields = _sort_fields_for_schema(
        list(analysis.field_analyses.values()), prioritize_compression
    )

    # Limit fields if necessary
    fields_to_include = sorted_fields[:max_fields]

    for field_analysis in fields_to_include:
        enum_values = None
        if field_analysis.top_values and len(field_analysis.top_values) <= 10:
            enum_values = [tv["value"] for tv in field_analysis.top_values]

        schema_fields.append(
            TSLNSchemaField(
                name=field_analysis.field_name,
                type=field_analysis.type,
                position=position,
                use_differential=field_analysis.use_differential,
                use_repeat_markers=field_analysis.use_repeat_markers,
                repeat_rate=field_analysis.repeat_rate,
                volatility=field_analysis.volatility,
                enum_values=enum_values,
            )
        )
        position += 1

    # Determine timestamp mode
    timestamp_mode: TimestampMode = "delta"
    if analysis.is_regular_interval and analysis.timestamp_interval:
        timestamp_mode = "interval"

    # Calculate overall compression estimate
    compression_estimates = []
    for f in schema_fields:
        estimate = 0.0
        if f.use_differential:
            estimate += 0.3
        if f.use_repeat_markers and f.repeat_rate:
            estimate += f.repeat_rate * 0.4
        compression_estimates.append(estimate)

    estimated_compression = (
        sum(compression_estimates) / len(compression_estimates) if compression_estimates else 0.0
    )

    return TSLNSchema(
        version="TSLN/1.0",
        fields=schema_fields,
        timestamp_mode=timestamp_mode,
        base_timestamp=analysis.base_timestamp,
        expected_interval=analysis.timestamp_interval,
        enable_differential=any(f.use_differential for f in schema_fields),
        enable_repeat_markers=any(f.use_repeat_markers for f in schema_fields),
        enable_run_length=False,
        total_fields=len(schema_fields),
        estimated_compression=estimated_compression,
    )


def _sort_fields_for_schema(
    fields: List[FieldTypeAnalysis], prioritize_compression: bool
) -> List[FieldTypeAnalysis]:
    """Sort fields for optimal schema ordering.

    Strategy: High-repeat fields first for better compression.

    Args:
        fields: List of field analyses
        prioritize_compression: Whether to sort by compression potential

    Returns:
        Sorted list of field analyses
    """
    if not prioritize_compression:
        return sorted(fields, key=lambda f: f.field_name)

    # Sort by compression potential (repeat rate + differential potential)
    return sorted(fields, key=lambda f: _calculate_compression_score(f), reverse=True)


def _calculate_compression_score(field: FieldTypeAnalysis) -> float:
    """Calculate compression score for field ordering.

    Args:
        field: Field analysis

    Returns:
        Compression score (higher is better)
    """
    score = 0.0

    # High repeat rate = better compression
    score += field.repeat_rate * 50

    # Differential encoding potential
    if field.use_differential:
        score += 30

    # Low volatility = better differential compression
    if field.volatility is not None:
        score += (1.0 - min(field.volatility, 1.0)) * 20

    return score


def generate_schema_header(schema: TSLNSchema) -> str:
    """Generate schema header string for TSLN output.

    Args:
        schema: TSLN schema

    Returns:
        Header string with schema definition and metadata
    """
    lines: List[str] = []

    lines.append(f"# {schema.version}")

    # Schema definition
    schema_parts = []
    for f in schema.fields:
        # Format: typeCode:fieldName
        type_code = f.type.value.split(":")[0]  # 't', 'i', 's', 'f', 'd', 'b', 'e', 'a', 'o'
        schema_parts.append(f"{type_code}:{f.name}")

    schema_line = " ".join(schema_parts)
    lines.append(f"# Schema: t:timestamp {schema_line}")

    # Timestamp configuration
    if schema.base_timestamp:
        base_iso = schema.base_timestamp.strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3] + "Z"
        lines.append(f"# Base: {base_iso}")

    if schema.timestamp_mode == "interval" and schema.expected_interval:
        lines.append(f"# Interval: {schema.expected_interval}ms")

    # Encoding strategies
    strategies: List[str] = []
    if schema.enable_differential:
        strategies.append("differential")
    if schema.enable_repeat_markers:
        strategies.append("repeat=")
    if schema.enable_run_length:
        strategies.append("run-length")

    if strategies:
        lines.append(f"# Encoding: {', '.join(strategies)}")

    return "\n".join(lines)


def parse_schema_header(header_lines: List[str]) -> TSLNSchema:
    """Parse TSLN schema from header (for decoding).

    Args:
        header_lines: List of header lines from TSLN file

    Returns:
        Parsed TSLNSchema
    """
    schema = TSLNSchema(
        version="TSLN/1.0",
        fields=[],
        timestamp_mode="delta",
        enable_differential=False,
        enable_repeat_markers=False,
        enable_run_length=False,
        total_fields=0,
        estimated_compression=0.0,
    )

    for line in header_lines:
        if not line.startswith("#"):
            continue

        content = line[1:].strip()

        if content.startswith("TSLN/"):
            schema.version = content
        elif content.startswith("Schema:"):
            schema_str = content[len("Schema:") :].strip()
            field_defs = schema_str.split()

            position = 0
            for field_def in field_defs:
                if ":" not in field_def:
                    continue

                parts = field_def.split(":", 1)
                if len(parts) != 2:
                    continue

                type_code, name = parts

                # Skip timestamp (handled separately)
                if name == "timestamp":
                    continue

                # Map type code to full type
                type_map: Dict[str, TSLNFieldType] = {
                    "t": TSLNFieldType.TIMESTAMP_DELTA,
                    "i": TSLNFieldType.STRING,
                    "s": TSLNFieldType.SYMBOL,
                    "f": TSLNFieldType.FLOAT,
                    "d": TSLNFieldType.INT,
                    "b": TSLNFieldType.BOOL,
                    "e": TSLNFieldType.ENUM,
                    "a": TSLNFieldType.ARRAY,
                    "o": TSLNFieldType.OBJECT,
                }

                field_type = type_map.get(type_code, TSLNFieldType.STRING)

                schema.fields.append(
                    TSLNSchemaField(
                        name=name,
                        type=field_type,
                        position=position,
                    )
                )
                position += 1

        elif content.startswith("Base:"):
            from datetime import datetime

            base_str = content[len("Base:") :].strip()
            # Handle ISO-8601 format
            try:
                schema.base_timestamp = datetime.fromisoformat(base_str.replace("Z", "+00:00"))
            except ValueError:
                pass

        elif content.startswith("Interval:"):
            interval_str = content[len("Interval:") :].strip()
            try:
                schema.expected_interval = int(interval_str.replace("ms", ""))
                schema.timestamp_mode = "interval"
            except ValueError:
                pass

        elif content.startswith("Encoding:"):
            encoding_str = content[len("Encoding:") :].strip()
            schema.enable_differential = "differential" in encoding_str
            schema.enable_repeat_markers = "repeat=" in encoding_str
            schema.enable_run_length = "run-length" in encoding_str

    schema.total_fields = len(schema.fields)

    return schema


def get_tsln_explanation(schema: TSLNSchema) -> str:
    """Get TSLN format explanation for AI.

    Args:
        schema: TSLN schema

    Returns:
        Human-readable explanation of the TSLN format
    """
    strategies: List[str] = []
    if schema.enable_differential:
        strategies.append("differential encoding (±values)")
    if schema.enable_repeat_markers:
        strategies.append("repeat markers (=)")
    if schema.enable_run_length:
        strategies.append("run-length (*N)")

    base_ts = "N/A"
    if schema.base_timestamp:
        base_ts = schema.base_timestamp.strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3] + "Z"

    strategies_str = ", ".join(strategies) if strategies else "standard"

    return f"""Data Format: TSLN (Time-Series Lean Notation)
Version: {schema.version}
Structure: Schema-first, pipe-delimited positional values
Timestamp Mode: {schema.timestamp_mode} (base: {base_ts})
Fields: {len(schema.fields)} columns
Encoding: {strategies_str}
Symbols: ∅=null, 1/0=boolean, +=increase, -=decrease, ==repeat
Benefits: ~75% more compact than JSON, ~40% more compact than TOON
Estimated Compression: {round(schema.estimated_compression * 100)}%"""


def optimize_schema(schema: TSLNSchema) -> TSLNSchema:
    """Optimize schema by reordering fields.

    Args:
        schema: Original schema

    Returns:
        Optimized schema with fields reordered for better compression
    """
    # Sort fields by compression score
    sorted_fields = sorted(
        schema.fields,
        key=lambda f: (f.repeat_rate or 0.0) * 50 + (30 if f.use_differential else 0),
        reverse=True,
    )

    # Update positions
    for index, field in enumerate(sorted_fields):
        field.position = index

    # Create new schema with sorted fields
    return TSLNSchema(
        version=schema.version,
        fields=sorted_fields,
        timestamp_mode=schema.timestamp_mode,
        base_timestamp=schema.base_timestamp,
        expected_interval=schema.expected_interval,
        enable_differential=schema.enable_differential,
        enable_repeat_markers=schema.enable_repeat_markers,
        enable_run_length=schema.enable_run_length,
        total_fields=schema.total_fields,
        estimated_compression=schema.estimated_compression,
    )
