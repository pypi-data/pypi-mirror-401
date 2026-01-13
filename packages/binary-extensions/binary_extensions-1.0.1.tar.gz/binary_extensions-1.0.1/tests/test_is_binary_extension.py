import pytest
from binary_extensions import is_binary_extension
from ._data import BINARY_EXAMPLES, NON_BINARY_EXAMPLES


@pytest.mark.parametrize("ext", BINARY_EXAMPLES)
def test_binary_extensions_true(ext):
    """Known binary extensions should return True"""
    assert is_binary_extension(ext)
    assert is_binary_extension(f".{ext}")
    assert is_binary_extension(ext.upper())
    assert is_binary_extension(ext.title())


@pytest.mark.parametrize("ext", NON_BINARY_EXAMPLES)
def test_non_binary_extensions_false(ext):
    """Non-binary extensions should return False"""
    assert not is_binary_extension(ext)


@pytest.mark.parametrize("ext", ["", ".", "unknown", "xyz"])
def test_edge_cases_false(ext):
    """Edge cases should return False"""
    assert not is_binary_extension(ext)

