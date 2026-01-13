"""Type definitions for TSLN (Time-Series Lean Notation)."""
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Literal, Optional, Union


class TSLNFieldType(str, Enum):
    """TSLN field type enumeration."""

    TIMESTAMP_DELTA = "t:delta"
    TIMESTAMP_INTERVAL = "t:interval"
    TIMESTAMP_ABSOLUTE = "t:absolute"
    FLOAT = "f:float"
    INT = "d:int"
    SYMBOL = "s:symbol"
    STRING = "i:string"
    BOOL = "b:bool"
    ENUM = "e:enum"
    ARRAY = "a:array"
    OBJECT = "o:object"


TimestampMode = Literal["delta", "interval", "absolute"]
TrendType = Literal["increasing", "decreasing", "stable"]


@dataclass
class BufferedDataPoint:
    """Single time-series data point.

    Attributes:
        timestamp: ISO-8601 formatted timestamp string
        data: Dictionary containing the data fields
    """

    timestamp: str
    data: Dict[str, Any]


@dataclass
class FieldTypeAnalysis:
    """Analysis results for a single field.

    Attributes:
        field_name: Name of the field
        type: Detected TSLN field type
        unique_value_count: Number of unique values
        total_count: Total number of values
        repeat_rate: Proportion of repeated values (0-1)
        is_numeric: Whether field contains numeric data
        is_integer: Whether numeric values are all integers
        volatility: Coefficient of variation for numeric fields
        trend: Detected trend direction for numeric fields
        top_values: Most frequent values for categorical fields
        use_differential: Whether to use differential encoding
        use_repeat_markers: Whether to use repeat markers
        use_run_length: Whether to use run-length encoding
    """

    field_name: str
    type: TSLNFieldType
    unique_value_count: int
    total_count: int
    repeat_rate: float
    is_numeric: bool = False
    is_integer: Optional[bool] = None
    volatility: Optional[float] = None
    trend: Optional[TrendType] = None
    top_values: Optional[List[Dict[str, Any]]] = None
    use_differential: bool = False
    use_repeat_markers: bool = False
    use_run_length: bool = False


@dataclass
class DatasetAnalysis:
    """Complete dataset analysis results.

    Attributes:
        total_points: Total number of data points
        field_analyses: Analysis for each field
        has_timestamp: Whether dataset has timestamp field
        timestamp_field: Name of the timestamp field
        timestamp_interval: Detected interval in milliseconds
        is_regular_interval: Whether timestamps are regularly spaced
        base_timestamp: Base timestamp for encoding
        dataset_volatility: Overall dataset volatility
        compression_potential: Estimated compression potential (0-1)
    """

    total_points: int
    field_analyses: Dict[str, FieldTypeAnalysis]
    has_timestamp: bool = False
    timestamp_field: Optional[str] = None
    timestamp_interval: Optional[int] = None
    is_regular_interval: bool = False
    base_timestamp: Optional[datetime] = None
    dataset_volatility: float = 0.0
    compression_potential: float = 0.0


@dataclass
class TSLNSchemaField:
    """Single field in TSLN schema.

    Attributes:
        name: Field name
        type: TSLN field type
        position: Position in schema (0-indexed)
        use_differential: Whether differential encoding is enabled
        use_repeat_markers: Whether repeat markers are enabled
        enum_values: Enum value mappings for enum fields
        repeat_rate: Repeat rate for compression estimation
        volatility: Volatility for compression estimation
    """

    name: str
    type: TSLNFieldType
    position: int
    use_differential: bool = False
    use_repeat_markers: bool = False
    enum_values: Optional[List[Any]] = None
    repeat_rate: Optional[float] = None
    volatility: Optional[float] = None


@dataclass
class TSLNSchema:
    """Complete TSLN schema definition.

    Attributes:
        version: TSLN version string
        fields: List of schema fields
        timestamp_mode: Timestamp encoding mode
        base_timestamp: Base timestamp for delta/interval modes
        expected_interval: Expected interval in milliseconds
        enable_differential: Whether differential encoding is enabled
        enable_repeat_markers: Whether repeat markers are enabled
        enable_run_length: Whether run-length encoding is enabled
        total_fields: Total number of fields
        estimated_compression: Estimated compression ratio
    """

    version: str = "TSLN/1.0"
    fields: List[TSLNSchemaField] = field(default_factory=list)
    timestamp_mode: TimestampMode = "delta"
    base_timestamp: Optional[datetime] = None
    expected_interval: Optional[int] = None
    enable_differential: bool = True
    enable_repeat_markers: bool = True
    enable_run_length: bool = False
    total_fields: int = 0
    estimated_compression: float = 0.0


@dataclass
class TSLNOptions:
    """Configuration options for TSLN encoding.

    Attributes:
        timestamp_mode: Override timestamp encoding mode
        base_timestamp: Override base timestamp
        enable_differential: Enable differential encoding
        enable_repeat_markers: Enable repeat markers
        enable_run_length: Enable run-length encoding
        precision: Decimal precision for floats
        max_string_length: Maximum string length (for truncation)
        max_fields: Maximum number of fields
        prioritize_compression: Prioritize compression over speed
        min_repeat_for_rle: Minimum repeats for run-length encoding
    """

    timestamp_mode: Optional[TimestampMode] = None
    base_timestamp: Optional[datetime] = None
    enable_differential: bool = True
    enable_repeat_markers: bool = True
    enable_run_length: bool = False
    precision: int = 2
    max_string_length: Optional[int] = None
    max_fields: int = 50
    prioritize_compression: bool = True
    min_repeat_for_rle: int = 3


@dataclass
class TSLNStatistics:
    """Compression and encoding statistics.

    Attributes:
        original_size: Original data size in bytes (JSON)
        tsln_size: TSLN output size in bytes
        compression_ratio: Compression ratio (0-1, higher is better)
        estimated_tokens: Estimated LLM tokens for TSLN
        estimated_token_savings: Token savings vs JSON
        encoding_time_ms: Encoding time in milliseconds
        field_count: Number of fields encoded
        point_count: Number of data points encoded
    """

    original_size: int
    tsln_size: int
    compression_ratio: float
    estimated_tokens: int
    estimated_token_savings: int
    encoding_time_ms: float = 0.0
    field_count: int = 0
    point_count: int = 0


@dataclass
class TSLNResult:
    """Complete TSLN encoding result.

    Attributes:
        tsln: Encoded TSLN string
        schema: Schema used for encoding
        analysis: Dataset analysis results
        statistics: Compression statistics
    """

    tsln: str
    schema: TSLNSchema
    analysis: DatasetAnalysis
    statistics: TSLNStatistics


@dataclass
class FormatComparison:
    """Comparison results between different formats.

    Attributes:
        format_name: Name of the format (JSON, CSV, XML, TSLN)
        size_bytes: Size in bytes
        estimated_tokens: Estimated LLM tokens
        compression_vs_json: Compression ratio vs JSON (percentage)
        encoding_time_ms: Time to encode in milliseconds
    """

    format_name: str
    size_bytes: int
    estimated_tokens: int
    compression_vs_json: float
    encoding_time_ms: float = 0.0


# Special TSLN symbols
TSLN_NULL = "∅"
TSLN_REPEAT = "="
TSLN_SEPARATOR = "|"
TSLN_ESCAPED_SEPARATOR = "¦"
