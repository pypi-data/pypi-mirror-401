from types import MappingProxyType

import pytest

from dbl_ingress import shape_input


def test_immutability_of_lists():
    """Verify that lists are converted to tuples."""
    record = shape_input(
        correlation_id="immut-list",
        deterministic={"list": [1, 2, 3]}
    )
    # The value inside the record should be a tuple
    assert isinstance(record.deterministic["list"], tuple)
    assert record.deterministic["list"] == (1, 2, 3)

def test_immutability_of_dicts():
    """Verify that dicts are wrapped in MappingProxyType."""
    record = shape_input(
        correlation_id="immut-dict",
        deterministic={"data": {"nested": "val"}}
    )
    # The top level deterministic is a MappingProxyType (because deep_freeze wraps dicts)
    assert isinstance(record.deterministic, MappingProxyType)
    
    # Nested dict should also be MappingProxyType
    assert isinstance(record.deterministic["data"], MappingProxyType)
    
    # Attempting to mutate should fail
    with pytest.raises(TypeError):
        record.deterministic["data"]["new"] = 1 # type: ignore

def test_external_mutation_safety():
    """Verify that mutating the input dict does not affect the record."""
    input_data = {"key": "value"}
    record = shape_input(
        correlation_id="safety-test",
        deterministic=input_data
    )
    
    # Mutate external
    input_data["key"] = "changed"
    
    # Record should remain "value"
    assert record.deterministic["key"] == "value"

def test_frozen_dataclass_mutation():
    """Verify that the dataclass itself is frozen."""
    record = shape_input(correlation_id="frozen", deterministic={})
    with pytest.raises(AttributeError): # FrozenInstanceError is AttributeError subclass
        record.correlation_id = "new-id" 

def test_tuple_conversion_deep():
    """Verify recursive list-to-tuple conversion."""
    record = shape_input(
        correlation_id="deep-tuple",
        deterministic={"matrix": [[1, 2], [3, 4]]}
    )
    matrix = record.deterministic["matrix"]
    assert isinstance(matrix, tuple)
    assert isinstance(matrix[0], tuple)
    assert matrix[0] == (1, 2)
