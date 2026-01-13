"""Round-trip tests for TSLN encoding and decoding."""
import pytest
from datetime import datetime, timedelta

from tsln import BufferedDataPoint, convert_to_tsln, decode_tsln, TSLNOptions


def generate_crypto_data(count: int) -> list:
    """Generate sample crypto data for testing."""
    base_time = datetime(2025, 12, 27, 10, 0, 0)
    data_points = []

    for i in range(count):
        timestamp = (base_time + timedelta(seconds=i)).isoformat() + "Z"
        data_points.append(
            BufferedDataPoint(
                timestamp=timestamp,
                data={
                    "symbol": "BTC",
                    "price": 50000.00 + (i * 125.5),
                    "volume": 1234567 + (i * 12340),
                },
            )
        )

    return data_points


def generate_iot_data(count: int) -> list:
    """Generate sample IoT sensor data for testing."""
    base_time = datetime(2025, 12, 27, 0, 0, 0)
    data_points = []

    for i in range(count):
        timestamp = (base_time + timedelta(minutes=i * 5)).isoformat() + "Z"
        data_points.append(
            BufferedDataPoint(
                timestamp=timestamp,
                data={
                    "device_id": "sensor-001",
                    "temperature": 22.5 + (i % 5) * 0.2,
                    "humidity": 45.0 + (i % 3) * 0.5,
                    "battery": 95 - (i // 10),
                },
            )
        )

    return data_points


class TestRoundTrip:
    """Test encoding and decoding produce identical results."""

    def test_basic_roundtrip(self):
        """Test basic round-trip encoding/decoding."""
        data_points = generate_crypto_data(5)

        # Encode
        result = convert_to_tsln(data_points)
        assert result.tsln is not None
        assert len(result.tsln) > 0

        # Decode
        decoded = decode_tsln(result.tsln)
        assert len(decoded) == len(data_points)

        # Verify data matches
        for original, recovered in zip(data_points, decoded):
            assert original.timestamp == recovered["timestamp"]
            assert original.data == recovered["data"]

    def test_roundtrip_with_differential(self):
        """Test round-trip with differential encoding enabled."""
        data_points = generate_crypto_data(10)

        options = TSLNOptions(enable_differential=True, precision=2)
        result = convert_to_tsln(data_points, options)
        decoded = decode_tsln(result.tsln)

        assert len(decoded) == len(data_points)

        for original, recovered in zip(data_points, decoded):
            assert original.timestamp == recovered["timestamp"]
            # Check prices match (with small floating point tolerance)
            assert abs(original.data["price"] - recovered["data"]["price"]) < 0.01

    def test_roundtrip_with_repeat_markers(self):
        """Test round-trip with repeat markers."""
        data_points = generate_iot_data(20)

        options = TSLNOptions(enable_repeat_markers=True)
        result = convert_to_tsln(data_points, options)
        decoded = decode_tsln(result.tsln)

        assert len(decoded) == len(data_points)

        for original, recovered in zip(data_points, decoded):
            assert original.data["device_id"] == recovered["data"]["device_id"]

    def test_roundtrip_interval_mode(self):
        """Test round-trip with interval timestamp mode."""
        data_points = generate_iot_data(10)

        options = TSLNOptions(timestamp_mode="interval")
        result = convert_to_tsln(data_points, options)

        # Verify interval mode was used
        assert result.schema.timestamp_mode == "interval"
        assert result.schema.expected_interval is not None

        decoded = decode_tsln(result.tsln)
        assert len(decoded) == len(data_points)

    def test_roundtrip_with_nulls(self):
        """Test round-trip with null values."""
        base_time = datetime(2025, 12, 27, 10, 0, 0)
        data_points = [
            BufferedDataPoint(
                timestamp=base_time.isoformat() + "Z",
                data={"value": 100, "label": "A"},
            ),
            BufferedDataPoint(
                timestamp=(base_time + timedelta(seconds=1)).isoformat() + "Z",
                data={"value": None, "label": "B"},
            ),
            BufferedDataPoint(
                timestamp=(base_time + timedelta(seconds=2)).isoformat() + "Z",
                data={"value": 200, "label": None},
            ),
        ]

        result = convert_to_tsln(data_points)
        decoded = decode_tsln(result.tsln)

        assert len(decoded) == 3
        assert decoded[1]["data"]["value"] is None
        assert decoded[2]["data"]["label"] is None

    def test_roundtrip_nested_objects(self):
        """Test round-trip with nested objects."""
        base_time = datetime(2025, 12, 27, 10, 0, 0)
        data_points = [
            BufferedDataPoint(
                timestamp=base_time.isoformat() + "Z",
                data={"user": {"name": "Alice", "age": 30}, "score": 95},
            ),
            BufferedDataPoint(
                timestamp=(base_time + timedelta(seconds=1)).isoformat() + "Z",
                data={"user": {"name": "Bob", "age": 25}, "score": 87},
            ),
        ]

        result = convert_to_tsln(data_points)
        decoded = decode_tsln(result.tsln)

        assert len(decoded) == 2
        assert decoded[0]["data"]["user"]["name"] == "Alice"
        assert decoded[1]["data"]["user"]["age"] == 25

    def test_empty_dataset(self):
        """Test encoding empty dataset."""
        data_points = []

        result = convert_to_tsln(data_points)
        assert "No data" in result.tsln

        decoded = decode_tsln(result.tsln) if "---" in result.tsln else []
        assert len(decoded) == 0

    def test_single_data_point(self):
        """Test encoding single data point."""
        data_points = generate_crypto_data(1)

        result = convert_to_tsln(data_points)
        decoded = decode_tsln(result.tsln)

        assert len(decoded) == 1
        assert data_points[0].timestamp == decoded[0]["timestamp"]

    def test_large_dataset(self):
        """Test encoding larger dataset for performance."""
        data_points = generate_crypto_data(100)

        result = convert_to_tsln(data_points)
        decoded = decode_tsln(result.tsln)

        assert len(decoded) == 100
        assert result.statistics.compression_ratio > 0.5  # At least 50% compression


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
