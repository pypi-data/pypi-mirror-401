from types import MappingProxyType
from typing import Dict, Mapping, TypeAlias, Union, cast

# Recursive type alias for JSON-safe values
# Note: mypy has trouble with recursive aliases, so we simplify slightly or use Any if needed,
# but for documentation and runtime enforcement this is the goal.
JsonValue: TypeAlias = Union[str, int, bool, None, "JsonSequence", "JsonMapping"]
JsonSequence: TypeAlias = tuple["JsonValue", ...]
JsonMapping: TypeAlias = Mapping[str, "JsonValue"]

def deep_freeze(value: object, path: str) -> JsonValue:
    """
    recursively strict-validates and deep-freezes the input.
    
    Returns an immutable copy of the data:
    - Lists -> tuples
    - Dicts -> MappingProxyType (wrapping a frozen dict)
    
    Invariants:
    - No floats.
    - No sets, objects, etc.
    - Keys must be strings.
    """
    if value is None:
        return None
        
    if isinstance(value, str):
        return value
        
    if isinstance(value, bool):
        return value
        
    if isinstance(value, int):
        return value
        
    if isinstance(value, float):
        raise TypeError(f"Floats are not allowed in admission records at {path}: {value}")
        
    if isinstance(value, Mapping):
        # We construct a new dict to ensure no reference to original mutable dict remains,
        # then wrap it in MappingProxyType
        frozen_dict: Dict[str, JsonValue] = {}
        for k, v in value.items():
            if not isinstance(k, str):
                 raise TypeError(f"Dictionary keys must be strings at {path}: {k}")
            frozen_dict[k] = deep_freeze(v, f"{path}.{k}")
        return cast(JsonValue, MappingProxyType(frozen_dict))
        
    if isinstance(value, list):
        # Convert list to tuple
        return tuple(deep_freeze(item, f"{path}[{i}]") for i, item in enumerate(value))

    # Reject everything else
    raise TypeError(f"Invalid type at {path}: {type(value)}")

def validate_json_safe(value: object, path: str) -> None:
    """
    Legacy validator wrapper for backward compatibility if needed, 
    but for hardening we prefer deep_freeze.
    """
    deep_freeze(value, path)

