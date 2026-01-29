import pytest

from dbl_ingress import AdmissionError, AdmissionRecord, InvalidInputError, __version__, shape_input


def test_imports():
    """Verify that expected symbols are exported."""
    assert __version__ == "0.1.0"
    assert AdmissionRecord
    assert AdmissionError
    assert InvalidInputError
    assert shape_input

def test_valid_admission_record():
    """Verify creation of a valid AdmissionRecord."""
    record = shape_input(
        correlation_id="test-123",
        deterministic={"key": "value", "num": 123, "bool": True, "none": None},
        observational={"obs": "data"}
    )
    assert record.correlation_id == "test-123"
    assert record.deterministic["num"] == 123
    assert record.observational["obs"] == "data"

def test_invalid_correlation_id():
    """Verify rejection of invalid correlation_id."""
    with pytest.raises(InvalidInputError, match="non-empty string"):
        shape_input(correlation_id="", deterministic={})

def test_reject_floats_deterministic():
    """Verify that floats are rejected in deterministic data."""
    with pytest.raises(InvalidInputError, match="Floats are not allowed"):
        shape_input(
            correlation_id="test-float",
            deterministic={"bad": 1.5}
        )

def test_reject_floats_observational():
    """Verify that floats are rejected in observational data."""
    with pytest.raises(InvalidInputError, match="Floats are not allowed"):
        shape_input(
            correlation_id="test-float-obs",
            deterministic={},
            observational={"bad": 3.14}
        )

def test_reject_non_string_keys():
    """Verify that dictionary keys must be strings."""
    with pytest.raises(InvalidInputError, match="keys must be strings"):
        shape_input(
            correlation_id="test-keys",
            deterministic={1: "bad_key"} # type: ignore
        )

def test_nested_validation():
    """Verify validation recurses into lists and nested dicts."""
    with pytest.raises(InvalidInputError, match="Floats are not allowed"):
        shape_input(
            correlation_id="test-nested",
            deterministic={"list": [1, 2, {"nested": 1.1}]}
        )
