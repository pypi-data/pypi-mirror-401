import pytest
from binary_extensions import BINARY_EXTENSIONS, is_binary_extension, is_binary_path
from ._data import BINARY_EXAMPLES, BINARY_PATHS


@pytest.mark.parametrize("ext,path,expected", [
    ("png", "file.png", True),
    ("jpg", "image.jpg", True),
    ("txt", "readme.txt", False),
    ("pdf", "document.pdf", True),
    ("py", "script.py", False),
])
def test_consistency_between_functions(ext, path, expected):
    """Both functions return consistent results"""
    assert is_binary_extension(ext) == expected
    assert is_binary_path(path) == expected


def test_all_extensions_in_set():
    """Ensure all extensions in BINARY_EXTENSIONS are recognized"""
    for ext in BINARY_EXTENSIONS:
        assert is_binary_extension(ext) is True
        assert is_binary_path(f"file.{ext}") is True

