import pytest
from humanize import naturalsize, i18n

@pytest.mark.parametrize("value,kwargs,expected", [
 (300, {}, "300 Bytes"), (1, {}, "1 Byte"), (3000000, {}, "3.0 MB"),
 (3000, {"binary": True}, "2.9 KiB"), (-4096, {"binary": True}, "-4.0 KiB"),
 (3000, {"gnu": True}, "2.9K"), (3000, {"gnu": True, "format": "%.3f"}, "2.930K"),
 (0, {}, "0 Bytes"), (1000000, {}, "1.0 MB"),
])
def test_existing_naturalsize_behavior(value, kwargs, expected):
 i18n.deactivate()
 assert naturalsize(value, **kwargs) == expected
