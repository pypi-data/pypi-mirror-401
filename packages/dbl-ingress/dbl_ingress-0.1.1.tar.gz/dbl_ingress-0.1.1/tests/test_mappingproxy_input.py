from types import MappingProxyType

from dbl_ingress.shaping.shape import shape_input


def test_accepts_mappingproxy_input():
    data = MappingProxyType({"a": 1})
    record = shape_input(correlation_id="mp", deterministic=data)
    assert record.deterministic["a"] == 1
