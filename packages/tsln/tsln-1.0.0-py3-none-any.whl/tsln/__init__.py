"""TSLN - Time-Series Lean Notation for Python.

Ultra-compact time-series format achieving 74% token reduction vs JSON.

Example:
    >>> from tsln import convert_to_tsln, decode_tsln
    >>> data = [
    ...     {"timestamp": "2025-12-27T10:00:00Z", "data": {"price": 50000}},
    ...     {"timestamp": "2025-12-27T10:00:01Z", "data": {"price": 50125}}
    ... ]
    >>> result = convert_to_tsln(data)
    >>> print(f"Compression: {result.statistics.compression_ratio:.1%}")
    >>> decoded = decode_tsln(result.tsln)
"""

__version__ = "1.0.0"
__author__ = "Turboline Team"
__license__ = "MIT"

from .core.analyzer import analyze_dataset, recommend_encoding_strategy
from .core.decoder import decode_tsln
from .core.encoder import convert_to_tsln, estimate_tsln_tokens
from .core.schema import (
    generate_schema,
    generate_schema_header,
    get_tsln_explanation,
    optimize_schema,
    parse_schema_header,
)
from .types import (
    BufferedDataPoint,
    DatasetAnalysis,
    FieldTypeAnalysis,
    FormatComparison,
    TSLNFieldType,
    TSLNOptions,
    TSLNResult,
    TSLNSchema,
    TSLNSchemaField,
    TSLNStatistics,
    TimestampMode,
    TrendType,
)
from .utils import compare_formats, print_comparison_table

__all__ = [
    # Main API
    "convert_to_tsln",
    "decode_tsln",
    "analyze_dataset",
    "compare_formats",
    # Schema functions
    "generate_schema",
    "generate_schema_header",
    "parse_schema_header",
    "get_tsln_explanation",
    "optimize_schema",
    # Types
    "BufferedDataPoint",
    "TSLNOptions",
    "TSLNResult",
    "TSLNSchema",
    "TSLNSchemaField",
    "TSLNStatistics",
    "TSLNFieldType",
    "TimestampMode",
    "TrendType",
    "DatasetAnalysis",
    "FieldTypeAnalysis",
    "FormatComparison",
    # Utilities
    "estimate_tsln_tokens",
    "recommend_encoding_strategy",
    "print_comparison_table",
]
