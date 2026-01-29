import uuid
from datetime import datetime, date
from decimal import Decimal

from biplex_utils_hash import (
    canonical_json,
    uuid5_from_data,
    sha256_from_data,
    normalize,
    DEFAULT_DECIMAL_PLACES,
)


class TestFloatStability:
    def test_float_vs_decimal(self):
        """Float arithmetic issues should produce same result as exact Decimal."""
        data1 = {"price": 0.1 + 0.2}
        data2 = {"price": Decimal("0.3")}

        assert canonical_json(data1) == canonical_json(data2)
        assert uuid5_from_data(data1) == uuid5_from_data(data2)
        assert sha256_from_data(data1) == sha256_from_data(data2)

    def test_float_rounding(self):
        """Floats should be rounded to specified decimal places."""
        data = {"value": 1.123456789}

        result_default = canonical_json(data)
        assert '"1.123457"' in result_default  # rounds to 6 places

        result_custom = canonical_json(data, decimal_places=3)
        assert '"1.123"' in result_custom

    def test_large_float(self):
        """Large floats should be handled correctly."""
        data = {"big": 123456789.123456}
        result = canonical_json(data)
        assert "123456789.123456" in result


class TestDictNormalization:
    def test_sorted_keys(self):
        """Dict keys should be sorted alphabetically."""
        data = {"z": 1, "a": 2, "m": 3}
        result = canonical_json(data)
        assert result == '{"a":2,"m":3,"z":1}'

    def test_nested_dict(self):
        """Nested dicts should be normalized recursively."""
        data = {"outer": {"z": 1, "a": 2}}
        result = canonical_json(data)
        assert result == '{"outer":{"a":2,"z":1}}'

    def test_non_string_keys(self):
        """Non-string keys should be converted to strings."""
        data = {1: "one", 2: "two"}
        result = canonical_json(data)
        assert result == '{"1":"one","2":"two"}'

    def test_empty_dict(self):
        """Empty dict should produce empty JSON object."""
        assert canonical_json({}) == "{}"


class TestListAndTuple:
    def test_list_order_preserved(self):
        """List order should be preserved."""
        data = [3, 1, 2]
        result = canonical_json(data)
        assert result == "[3,1,2]"

    def test_tuple_converted_to_list(self):
        """Tuples should be converted to lists."""
        data = (1, 2, 3)
        result = canonical_json(data)
        assert result == "[1,2,3]"

    def test_nested_list(self):
        """Nested lists should be normalized recursively."""
        data = [[1, 2], [3, 4]]
        result = canonical_json(data)
        assert result == "[[1,2],[3,4]]"

    def test_empty_list(self):
        """Empty list should produce empty JSON array."""
        assert canonical_json([]) == "[]"


class TestSetAndFrozenset:
    def test_set_sorted(self):
        """Sets should be converted to sorted lists."""
        data = {3, 1, 2}
        result = canonical_json(data)
        assert result == "[1,2,3]"

    def test_frozenset_sorted(self):
        """Frozensets should be converted to sorted lists."""
        data = frozenset([3, 1, 2])
        result = canonical_json(data)
        assert result == "[1,2,3]"

    def test_set_with_strings(self):
        """String sets should be sorted alphabetically."""
        data = {"c", "a", "b"}
        result = canonical_json(data)
        assert result == '["a","b","c"]'


class TestDatetime:
    def test_datetime_iso_format(self):
        """Datetime should be converted to ISO format string."""
        dt = datetime(2024, 1, 15, 10, 30, 45)
        data = {"timestamp": dt}
        result = canonical_json(data)
        assert result == '{"timestamp":"2024-01-15T10:30:45"}'

    def test_date_iso_format(self):
        """Date should be converted to ISO format string."""
        d = date(2024, 1, 15)
        data = {"date": d}
        result = canonical_json(data)
        assert result == '{"date":"2024-01-15"}'

    def test_datetime_with_microseconds(self):
        """Datetime with microseconds should preserve them."""
        dt = datetime(2024, 1, 15, 10, 30, 45, 123456)
        data = {"timestamp": dt}
        result = canonical_json(data)
        assert "123456" in result


class TestUUID:
    def test_uuid_to_string(self):
        """UUID should be converted to string."""
        test_uuid = uuid.UUID("12345678-1234-5678-1234-567812345678")
        data = {"id": test_uuid}
        result = canonical_json(data)
        assert result == '{"id":"12345678-1234-5678-1234-567812345678"}'


class TestNoneAndBasicTypes:
    def test_none(self):
        """None should be serialized as null."""
        data = {"value": None}
        result = canonical_json(data)
        assert result == '{"value":null}'

    def test_boolean(self):
        """Booleans should be serialized correctly."""
        data = {"true": True, "false": False}
        result = canonical_json(data)
        assert result == '{"false":false,"true":true}'

    def test_integer(self):
        """Integers should remain as integers."""
        data = {"num": 42}
        result = canonical_json(data)
        assert result == '{"num":42}'

    def test_string(self):
        """Strings should be preserved."""
        data = {"text": "hello"}
        result = canonical_json(data)
        assert result == '{"text":"hello"}'


class TestDecimalPlaces:
    def test_default_decimal_places(self):
        """Default decimal places should be 6."""
        assert DEFAULT_DECIMAL_PLACES == 6

    def test_custom_decimal_places(self):
        """Custom decimal places should be respected."""
        data = {"value": 1.111111111}

        result_2 = canonical_json(data, decimal_places=2)
        assert '"1.11"' in result_2

        result_4 = canonical_json(data, decimal_places=4)
        assert '"1.1111"' in result_4


class TestHashFunctions:
    def test_sha256_deterministic(self):
        """SHA256 should be deterministic."""
        data = {"key": "value"}
        hash1 = sha256_from_data(data)
        hash2 = sha256_from_data(data)
        assert hash1 == hash2
        assert len(hash1) == 64  # SHA256 hex is 64 chars

    def test_uuid5_deterministic(self):
        """UUID5 should be deterministic."""
        data = {"key": "value"}
        uuid1 = uuid5_from_data(data)
        uuid2 = uuid5_from_data(data)
        assert uuid1 == uuid2
        assert isinstance(uuid1, uuid.UUID)

    def test_uuid5_custom_namespace(self):
        """UUID5 should use custom namespace."""
        data = {"key": "value"}
        uuid1 = uuid5_from_data(data, namespace=uuid.NAMESPACE_DNS)
        uuid2 = uuid5_from_data(data, namespace=uuid.NAMESPACE_URL)
        assert uuid1 != uuid2


class TestNormalizeFunction:
    def test_normalize_exported(self):
        """normalize function should be exported."""
        result = normalize({"b": 1, "a": 2})
        assert result == {"a": 2, "b": 1}

    def test_normalize_with_custom_decimal_places(self):
        """normalize should accept decimal_places parameter."""
        result = normalize({"value": 1.23456789}, decimal_places=2)
        assert result == {"value": "1.23"}


class TestComplexStructures:
    def test_deeply_nested(self):
        """Deeply nested structures should be handled."""
        data = {
            "level1": {
                "level2": {
                    "level3": [1, 2, {"level4": "deep"}]
                }
            }
        }
        result = canonical_json(data)
        assert '"level4":"deep"' in result

    def test_mixed_types(self):
        """Mixed types in a structure should all be normalized."""
        data = {
            "float": 0.1 + 0.2,
            "int": 42,
            "string": "test",
            "list": [1, 2, 3],
            "nested": {"a": 1},
            "none": None,
            "bool": True,
        }
        result1 = canonical_json(data)
        result2 = canonical_json(data)
        assert result1 == result2
