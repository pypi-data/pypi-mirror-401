"""TSLN Type Analyzer - Analyzes data patterns to determine optimal encoding strategies."""
import statistics
from datetime import datetime
from typing import Any, Dict, List, Optional, Set, Tuple

from ..types import (
    BufferedDataPoint,
    DatasetAnalysis,
    FieldTypeAnalysis,
    TSLNFieldType,
    TrendType,
)


def analyze_dataset(data_points: List[BufferedDataPoint]) -> DatasetAnalysis:
    """Analyze dataset and recommend optimal TSLN encoding strategies.

    Args:
        data_points: List of timestamped data points to analyze

    Returns:
        DatasetAnalysis with field analyses and timestamp information
    """
    if len(data_points) == 0:
        return DatasetAnalysis(
            total_points=0,
            field_analyses={},
            has_timestamp=False,
            dataset_volatility=0.0,
            compression_potential=0.0,
        )

    # Extract and analyze all fields
    field_data = _extract_field_data(data_points)
    field_analyses: Dict[str, FieldTypeAnalysis] = {}

    for field_name, values in field_data.items():
        field_analyses[field_name] = _analyze_field(field_name, values)

    # Analyze timestamps
    timestamp_info = _analyze_timestamps(data_points)

    # Calculate overall metrics
    numeric_fields = [f for f in field_analyses.values() if f.is_numeric]
    dataset_volatility = 0.0
    if numeric_fields:
        dataset_volatility = sum(f.volatility or 0.0 for f in numeric_fields) / len(numeric_fields)

    # Compression potential based on repeat rates and volatility
    all_fields = list(field_analyses.values())
    avg_repeat_rate = sum(f.repeat_rate for f in all_fields) / len(all_fields) if all_fields else 0.0
    compression_potential = (avg_repeat_rate + (1 - min(dataset_volatility, 1.0))) / 2

    return DatasetAnalysis(
        total_points=len(data_points),
        field_analyses=field_analyses,
        has_timestamp=timestamp_info["has_timestamp"],
        timestamp_field=timestamp_info.get("timestamp_field"),
        timestamp_interval=timestamp_info.get("timestamp_interval"),
        is_regular_interval=timestamp_info.get("is_regular_interval", False),
        base_timestamp=timestamp_info.get("base_timestamp"),
        dataset_volatility=dataset_volatility,
        compression_potential=compression_potential,
    )


def _extract_field_data(data_points: List[BufferedDataPoint]) -> Dict[str, List[Any]]:
    """Extract all field values from dataset.

    Args:
        data_points: List of data points

    Returns:
        Dictionary mapping field names to lists of values
    """
    field_data: Dict[str, List[Any]] = {}

    for point in data_points:
        flattened = _flatten_object(point.data)

        for key, value in flattened.items():
            if key not in field_data:
                field_data[key] = []
            field_data[key].append(value)

    return field_data


def _analyze_field(field_name: str, values: List[Any]) -> FieldTypeAnalysis:
    """Analyze a single field to determine optimal type and encoding.

    Args:
        field_name: Name of the field
        values: List of field values

    Returns:
        FieldTypeAnalysis with type detection and encoding recommendations
    """
    total_count = len(values)
    non_null_values = [v for v in values if v is not None]

    # Count unique values
    unique_values: Set[Any] = set()
    for v in non_null_values:
        # Handle unhashable types
        if isinstance(v, (list, dict)):
            unique_values.add(str(v))
        else:
            unique_values.add(v)

    unique_value_count = len(unique_values)
    repeat_rate = 1.0 - (unique_value_count / total_count) if total_count > 0 else 0.0

    # Determine base type
    sample_value = non_null_values[0] if non_null_values else None
    field_type: TSLNFieldType
    is_numeric = False
    is_integer: Optional[bool] = None
    volatility: Optional[float] = None
    trend: Optional[TrendType] = None
    top_values: Optional[List[Dict[str, Any]]] = None

    # Type detection
    if isinstance(sample_value, bool):
        field_type = TSLNFieldType.BOOL
    elif isinstance(sample_value, (int, float)):
        is_numeric = True
        numeric_values = [v for v in non_null_values if isinstance(v, (int, float))]
        is_integer = all(isinstance(v, int) or v == int(v) for v in numeric_values)
        field_type = TSLNFieldType.INT if is_integer else TSLNFieldType.FLOAT

        # Calculate volatility (coefficient of variation)
        volatility = _calculate_volatility(numeric_values)
        trend = _detect_trend(numeric_values)
    elif isinstance(sample_value, str):
        # Distinguish between symbols (short, high repeat) and general strings
        str_values = [str(v) for v in non_null_values]
        avg_length = sum(len(s) for s in str_values) / len(str_values) if str_values else 0
        is_symbol_like = avg_length < 15 and repeat_rate > 0.3
        field_type = TSLNFieldType.SYMBOL if is_symbol_like else TSLNFieldType.STRING
    elif isinstance(sample_value, list):
        field_type = TSLNFieldType.ARRAY
    elif isinstance(sample_value, dict):
        field_type = TSLNFieldType.OBJECT
    else:
        field_type = TSLNFieldType.STRING  # Fallback

    # Get top values for categorical data
    if unique_value_count < 20 and not is_numeric:
        value_counts: Dict[Any, int] = {}
        for value in non_null_values:
            # Convert unhashable types to strings for counting
            key = str(value) if isinstance(value, (list, dict)) else value
            value_counts[key] = value_counts.get(key, 0) + 1

        top_values = [
            {"value": value, "count": count} for value, count in value_counts.items()
        ]
        top_values.sort(key=lambda x: x["count"], reverse=True)
        top_values = top_values[:10]

    # Encoding recommendations
    use_differential = is_numeric and volatility is not None and volatility < 0.5
    use_repeat_markers = repeat_rate > 0.4
    use_run_length = _detect_run_length(values) > 3

    return FieldTypeAnalysis(
        field_name=field_name,
        type=field_type,
        unique_value_count=unique_value_count,
        total_count=total_count,
        repeat_rate=repeat_rate,
        is_numeric=is_numeric,
        is_integer=is_integer,
        volatility=volatility,
        trend=trend,
        top_values=top_values,
        use_differential=use_differential,
        use_repeat_markers=use_repeat_markers,
        use_run_length=use_run_length,
    )


def _analyze_timestamps(
    data_points: List[BufferedDataPoint],
) -> Dict[str, Any]:
    """Analyze timestamp patterns.

    Args:
        data_points: List of data points

    Returns:
        Dictionary with timestamp analysis results
    """
    if len(data_points) == 0:
        return {"has_timestamp": False}

    # Check if points have timestamp field
    has_timestamp = all(hasattr(p, "timestamp") and p.timestamp for p in data_points)
    if not has_timestamp:
        return {"has_timestamp": False}

    try:
        timestamps = [datetime.fromisoformat(p.timestamp.replace("Z", "+00:00")) for p in data_points]
        timestamps_ms = [int(t.timestamp() * 1000) for t in timestamps]
    except (ValueError, AttributeError):
        return {"has_timestamp": False}

    base_timestamp = timestamps[0]

    # Calculate intervals
    intervals: List[int] = []
    for i in range(1, len(timestamps_ms)):
        intervals.append(timestamps_ms[i] - timestamps_ms[i - 1])

    if len(intervals) == 0:
        return {
            "has_timestamp": True,
            "timestamp_field": "timestamp",
            "base_timestamp": base_timestamp,
            "is_regular_interval": True,
            "timestamp_interval": 0,
        }

    avg_interval = sum(intervals) / len(intervals)

    # Check if intervals are regular (within 10% variance)
    interval_variance = sum(abs(val - avg_interval) for val in intervals) / len(intervals)
    is_regular_interval = interval_variance < avg_interval * 0.1

    return {
        "has_timestamp": True,
        "timestamp_field": "timestamp",
        "timestamp_interval": round(avg_interval),
        "is_regular_interval": is_regular_interval,
        "base_timestamp": base_timestamp,
    }


def _calculate_volatility(values: List[float]) -> float:
    """Calculate coefficient of variation for numeric data.

    Args:
        values: List of numeric values

    Returns:
        Coefficient of variation (0 = no variation, higher = more volatile)
    """
    if len(values) == 0:
        return 0.0

    mean_val = statistics.mean(values)
    if mean_val == 0:
        return 0.0

    try:
        std_dev = statistics.stdev(values)
        return std_dev / abs(mean_val)
    except statistics.StatisticsError:
        return 0.0


def _detect_trend(values: List[float]) -> TrendType:
    """Detect trend in numeric sequence.

    Args:
        values: List of numeric values

    Returns:
        'increasing', 'decreasing', or 'stable'
    """
    if len(values) < 2:
        return "stable"

    increases = 0
    decreases = 0

    for i in range(1, len(values)):
        if values[i] > values[i - 1]:
            increases += 1
        elif values[i] < values[i - 1]:
            decreases += 1

    total_transitions = len(values) - 1
    increase_rate = increases / total_transitions
    decrease_rate = decreases / total_transitions

    if increase_rate > 0.6:
        return "increasing"
    if decrease_rate > 0.6:
        return "decreasing"
    return "stable"


def _detect_run_length(values: List[Any]) -> int:
    """Detect longest run of identical values.

    Args:
        values: List of values

    Returns:
        Length of longest run
    """
    if len(values) == 0:
        return 0

    max_run = 1
    current_run = 1

    for i in range(1, len(values)):
        if values[i] == values[i - 1]:
            current_run += 1
            max_run = max(max_run, current_run)
        else:
            current_run = 1

    return max_run


def _flatten_object(obj: Any, prefix: str = "") -> Dict[str, Any]:
    """Flatten nested objects with dot notation.

    Args:
        obj: Object to flatten
        prefix: Prefix for nested keys

    Returns:
        Flattened dictionary with dot notation keys
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


def recommend_encoding_strategy(
    analysis: FieldTypeAnalysis,
) -> Tuple[str, List[str], float]:
    """Recommend best encoding strategy for a field.

    Args:
        analysis: Field analysis results

    Returns:
        Tuple of (primary_strategy, secondary_strategies, estimated_compression)
    """
    strategies: List[str] = []
    compression = 0.0

    if analysis.use_differential:
        strategies.append("differential")
        compression += 0.4

    if analysis.use_repeat_markers:
        strategies.append("repeat-markers")
        compression += analysis.repeat_rate * 0.5

    if analysis.use_run_length:
        strategies.append("run-length")
        compression += 0.3

    primary_strategy = strategies[0] if strategies else "none"
    secondary_strategies = strategies[1:] if len(strategies) > 1 else []

    return primary_strategy, secondary_strategies, min(compression, 0.9)
