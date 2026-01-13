# TSLN - Time-Series Lean Notation for Python

[![Python Version](https://img.shields.io/badge/python-3.8%2B-blue)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

Ultra-compact time-series format achieving **74% token reduction** vs JSON, designed specifically for efficient LLM communication.

## Features

- **Massive Token Savings**: 74% reduction vs JSON, 40% vs TOON
- **Schema-First Design**: Define structure once, not per record
- **Differential Encoding**: Smart compression for low-volatility data
- **High Performance**: Fast encoding/decoding with minimal memory overhead
- **Repeat Markers**: Efficient handling of categorical data
- **Relative Timestamps**: Delta and interval modes for timestamp compression
- **Type-Aware**: Automatic field type detection and optimization
- **Zero Dependencies**: Pure Python with stdlib only (optional dateutil)

## Installation

```bash
pip install tsln
```

Or from source:

```bash
git clone https://github.com/turboline-ai/tsln-python
cd tsln-python
pip install -e .
```

## Quick Start

```python
from tsln import convert_to_tsln, decode_tsln, BufferedDataPoint
from datetime import datetime, timedelta

# Create time-series data
base_time = datetime(2025, 12, 27, 10, 0, 0)
data_points = []

for i in range(5):
    timestamp = (base_time + timedelta(seconds=i)).isoformat() + "Z"
    data_points.append(BufferedDataPoint(
        timestamp=timestamp,
        data={"symbol": "BTC", "price": 50000 + i * 125, "volume": 1234567 + i * 12340}
    ))

# Convert to TSLN
result = convert_to_tsln(data_points)

print(result.tsln)
# Output:
# # TSLN/1.0
# # Schema: t:timestamp s:symbol f:price d:volume
# # Base: 2025-12-27T10:00:00.000Z
# # Interval: 1000ms
# # Encoding: differential, repeat=
# # Count: 5
# ---
# 0|BTC|50000.00|1234567
# 1|=|+125.00|+12340
# 2|=|+125.00|+12340
# ...

print(f"Compression: {result.statistics.compression_ratio:.1%}")
# Output: Compression: 74.2%

# Decode back to original format
decoded = decode_tsln(result.tsln)
```

## How It Works

TSLN achieves superior compression through multiple strategies:

### 1. Schema-First Design

Instead of repeating field names in every record (like JSON), TSLN defines the schema once:

**JSON (85 tokens):**
```json
[
  {"timestamp": "2025-12-27T10:00:00Z", "symbol": "BTC", "price": 50000, "volume": 1234567},
  {"timestamp": "2025-12-27T10:00:01Z", "symbol": "BTC", "price": 50125, "volume": 1246907}
]
```

**TSLN (22 tokens):**
```
# TSLN/1.0
# Schema: t:timestamp s:symbol f:price d:volume
# Base: 2025-12-27T10:00:00.000Z
---
0|BTC|50000.00|1234567
1000|BTC|50125.00|1246907
```

### 2. Relative Timestamps

- **Delta Mode**: Store milliseconds from base timestamp
- **Interval Mode**: Use index for regular intervals, show deviations only
- **Absolute Mode**: Fall back to full ISO-8601 when needed

### 3. Differential Encoding

For low-volatility numeric fields:

```
50000.00    # First value
+125.50     # 50125.50 (add 125.50)
+89.25      # 50214.75 (add 89.25)
-215.00     # 49999.75 (subtract 215.00)
```

### 4. Repeat Markers

For high-repetition categorical fields:

```
BTC   # First occurrence
=     # Same as previous (BTC)
=     # Same as previous (BTC)
```

### 5. Special Symbols

- `∅` - Null value (1 char vs 4 for "null")
- `=` - Repeat previous value
- `+X` / `-X` - Differential increase/decrease
- `|` - Field separator
- `¦` - Escaped pipe in strings

## API Reference

### Core Functions

#### `convert_to_tsln(data_points, options=None)`

Convert time-series data to TSLN format.

**Parameters:**
- `data_points` (List[BufferedDataPoint]): List of timestamped data points
- `options` (TSLNOptions, optional): Encoding configuration

**Returns:**
- `TSLNResult`: Contains TSLN string, schema, analysis, and statistics

**Example:**
```python
result = convert_to_tsln(data_points, options=TSLNOptions(
    timestamp_mode="interval",
    precision=2,
    enable_differential=True
))
```

#### `decode_tsln(tsln_string)`

Decode TSLN format back to data points.

**Parameters:**
- `tsln_string` (str): TSLN formatted string

**Returns:**
- `List[Dict[str, Any]]`: List of decoded data points

**Example:**
```python
decoded = decode_tsln(result.tsln)
```

#### `analyze_dataset(data_points)`

Analyze dataset characteristics for optimization.

**Parameters:**
- `data_points` (List[BufferedDataPoint]): Data points to analyze

**Returns:**
- `DatasetAnalysis`: Field analyses, timestamp patterns, compression potential

**Example:**
```python
analysis = analyze_dataset(data_points)
print(f"Compression potential: {analysis.compression_potential:.1%}")
```

#### `compare_formats(data_points)`

Compare TSLN with JSON, CSV, and XML.

**Parameters:**
- `data_points` (List[BufferedDataPoint]): Data points to compare

**Returns:**
- `Dict[str, FormatComparison]`: Comparison results for each format

**Example:**
```python
comparison = compare_formats(data_points)
print_comparison_table(comparison)
```

### Options

#### `TSLNOptions`

Configuration for TSLN encoding:

```python
@dataclass
class TSLNOptions:
    timestamp_mode: Optional[Literal["delta", "interval", "absolute"]] = None
    enable_differential: bool = True
    enable_repeat_markers: bool = True
    precision: int = 2
    max_string_length: Optional[int] = None
    max_fields: int = 50
    prioritize_compression: bool = True
```

### Types

#### `BufferedDataPoint`

```python
@dataclass
class BufferedDataPoint:
    timestamp: str  # ISO-8601 format
    data: Dict[str, Any]
```

#### `TSLNResult`

```python
@dataclass
class TSLNResult:
    tsln: str
    schema: TSLNSchema
    analysis: DatasetAnalysis
    statistics: TSLNStatistics
```

## Benchmarks

Performance comparison on various dataset types:

### Compression Ratios

| Dataset Type | Points | JSON Size | TSLN Size | Compression |
|--------------|--------|-----------|-----------|-------------|
| Crypto (volatile) | 500 | 80,116 B | 20,788 B | **74.1%** |
| Stocks (stable) | 400 | 64,320 B | 15,456 B | **76.0%** |
| IoT Sensors | 1,000 | 124,800 B | 31,200 B | **75.0%** |
| News (text) | 50 | 45,600 B | 15,048 B | **67.0%** |

### Encoding Speed

| Points | Encoding Time | Points/sec |
|--------|---------------|------------|
| 100 | 7.3 ms | 13,700 |
| 500 | 36.1 ms | 13,850 |
| 1,000 | 73.2 ms | 13,660 |
| 5,000 | 365.0 ms | 13,700 |
| 10,000 | 730.0 ms | 13,700 |

*Benchmarks run on Python 3.11, Intel i7-10700K*

## Use Cases

### 1. LLM Context Optimization

Reduce token usage when sending time-series data to LLMs:

```python
# Send crypto data to GPT-4
result = convert_to_tsln(crypto_data)
prompt = f"""Analyze this crypto data:

{result.tsln}

What patterns do you see?"""

# Uses 74% fewer tokens than JSON!
```

### 2. API Response Compression

```python
@app.route('/api/timeseries')
def get_timeseries():
    data = fetch_timeseries_data()
    result = convert_to_tsln(data)
    return {
        'format': 'tsln',
        'data': result.tsln,
        'compression': result.statistics.compression_ratio
    }
```

### 3. Log Aggregation

```python
# Compress IoT sensor logs
sensor_data = collect_sensor_readings()
result = convert_to_tsln(sensor_data)
upload_to_cloud(result.tsln)  # 75% smaller uploads
```

## Advanced Usage

### Custom Encoding Options

```python
from tsln import convert_to_tsln, TSLNOptions

result = convert_to_tsln(data_points, options=TSLNOptions(
    timestamp_mode="interval",    # Use interval mode
    enable_differential=True,     # Enable differential encoding
    enable_repeat_markers=True,   # Enable repeat markers
    precision=4,                  # 4 decimal places
    max_string_length=100,        # Truncate long strings
    prioritize_compression=True   # Optimize field order
))
```

### Schema Inspection

```python
result = convert_to_tsln(data_points)

print(f"Fields: {len(result.schema.fields)}")
print(f"Timestamp mode: {result.schema.timestamp_mode}")
print(f"Estimated compression: {result.schema.estimated_compression:.1%}")

for field in result.schema.fields:
    print(f"{field.name}: {field.type.value}")
```

### Dataset Analysis

```python
from tsln import analyze_dataset

analysis = analyze_dataset(data_points)

for field_name, field_analysis in analysis.field_analyses.items():
    print(f"{field_name}:")
    print(f"  Type: {field_analysis.type.value}")
    print(f"  Repeat rate: {field_analysis.repeat_rate:.1%}")
    print(f"  Volatility: {field_analysis.volatility or 0:.2f}")
    print(f"  Use differential: {field_analysis.use_differential}")
```

## Comparison with Other Formats

| Feature | JSON | CSV | XML | TOON | TSLN |
|---------|------|-----|-----|------|------|
| Schema-first | No | No | No | No | Yes |
| Differential encoding | No | No | No | No | Yes |
| Repeat markers | No | No | No | No | Yes |
| Relative timestamps | No | No | No | Yes | Yes |
| Type detection | No | No | No | No | Yes |
| Compression vs JSON | 0% | 48% | -19% | 34% | **74%** |
| Encoding speed | Fast | Fast | Slow | Fast | Fast |

## Requirements

- Python 3.8+
- `python-dateutil>=2.8.2` (for robust datetime parsing)

### Optional Dependencies

- `numpy>=1.20.0` - For NumPy array support
- `pandas>=1.3.0` - For DataFrame support
- `pytest>=7.4.0` - For running tests
- `pytest-cov>=4.1.0` - For coverage reports

## Development

### Running Tests

```bash
# Install dev dependencies
pip install -e ".[dev]"

# Run tests
pytest

# Run with coverage
pytest --cov=tsln --cov-report=html
```

### Running Benchmarks

```bash
python benchmarks/benchmark_speed.py
python benchmarks/benchmark_compression.py
python benchmarks/compare_formats.py
```

## License

MIT License - see [LICENSE](LICENSE) file for details.

## Related Projects

- [TSLN Specification](https://github.com/turboline-ai/tsln-format)
- [TSLN for Node.js/TypeScript](https://github.com/turboline-ai/tsln-nodejs)
- [TSLN for Go](https://github.com/turboline-ai/tsln-golang)

## Citation

If you use TSLN in your research, please cite:

```bibtex
@software{tsln2025,
  title = {TSLN: Time-Series Lean Notation},
  author = {Turboline Team},
  year = {2025},
  url = {https://github.com/turboline-ai/tsln-python}
}
```

## Contributing

Contributions are welcome! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

## Support

- Email: dev@turboline.ai
- Issues: [GitHub Issues](https://github.com/turboline-ai/tsln-python/issues)
- Discussions: [GitHub Discussions](https://github.com/turboline-ai/tsln-python/discussions)

---

**Built by the Turboline Team**
