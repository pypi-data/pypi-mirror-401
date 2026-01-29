import pytest

from dbl_ingress import InvalidInputError, shape_input


class CustomObj:
    def to_dict(self):
        return {"a": 1}

def test_deep_validation_rejection():
    """Verify that validation fails deeply inside a structure."""
    with pytest.raises(InvalidInputError, match="Floats are not allowed"):
        shape_input(
            correlation_id="deep-test",
            deterministic={
                "level1": {
                    "level2": [
                        {"level3": 1.1}
                    ]
                }
            }
        )

def test_observational_is_validated():
    """Verify that observational data is strictly validated just like deterministic."""
    with pytest.raises(InvalidInputError, match="Floats are not allowed"):
        shape_input(
            correlation_id="obs-test",
            deterministic={"ok": 1},
            observational={"bad": 1.1}
        )

def test_reject_sets():
    """Verify that sets are rejected (JSON requires lists)."""
    with pytest.raises(InvalidInputError, match="Invalid type"):
        shape_input(
            correlation_id="set-test",
            deterministic={"bad": {1, 2, 3}}
        )

def test_reject_tuples():
    """Verify that tuples are rejected (should use lists)."""
    with pytest.raises(InvalidInputError, match="Invalid type"):
        shape_input(
            correlation_id="tuple-test",
            deterministic={"bad": (1, 2)}
        )

def test_reject_custom_objects():
    """Verify that custom objects are rejected, even with to_dict."""
    obj = CustomObj()
    with pytest.raises(InvalidInputError, match="Invalid type"):
        shape_input(
            correlation_id="obj-test",
            deterministic={"bad": obj}
        )
