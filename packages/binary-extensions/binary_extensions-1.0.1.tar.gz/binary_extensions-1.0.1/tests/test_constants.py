import pytest
from binary_extensions import BINARY_EXTENSIONS
from ._data import BINARY_EXAMPLES


def test_binary_extensions_type_and_content():
    """Check BINARY_EXTENSIONS is a non-empty frozenset"""
    assert isinstance(BINARY_EXTENSIONS, frozenset)
    assert len(BINARY_EXTENSIONS) > 0


@pytest.mark.parametrize("ext", BINARY_EXAMPLES)
def test_common_binary_extensions_present(ext):
    """Check that common binary extensions are present in BINARY_EXTENSIONS"""
    assert ext in BINARY_EXTENSIONS

