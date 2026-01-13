import pytest
from binary_extensions import is_binary_path
from ._data import BINARY_PATHS, NON_BINARY_PATHS, HIDDEN_BINARY_PATHS, HIDDEN_NON_BINARY_PATHS


@pytest.mark.parametrize("path", BINARY_PATHS + HIDDEN_BINARY_PATHS)
def test_binary_paths_true(path):
    """Paths with known binary extensions should return True"""
    assert is_binary_path(path)


@pytest.mark.parametrize("path", NON_BINARY_PATHS + HIDDEN_NON_BINARY_PATHS)
def test_non_binary_paths_false(path):
    """Paths without known binary extensions should return False"""
    assert not is_binary_path(path)


@pytest.mark.parametrize("path", ["", ".", "..", "file", "path/to/file", "file.name.txt"])
def test_paths_without_extension_false(path):
    """Paths without extensions or with non-binary extensions should return False"""
    assert not is_binary_path(path)


@pytest.mark.parametrize(
    "path,expected",
    [
        ("file.backup.zip", True),
        ("archive.tar.gz", True),
        ("file.name.txt", False),
        ("C:\\Users\\file.pdf", True),
        ("/path/to/document.txt", False),
        ("IMAGE.PNG", True),
        ("Photo.JPG", True),
        ("Document.PDF", True),
        ("file.TXT", False),
        ("/path/to/image.png", True),
        ("folder/subfolder/file.jpg", True),
        ("file.", False),
    ]
)
def test_paths_various(path, expected):
    """Edge cases: multiple dots, OS paths, case insensitivity, directories"""
    assert is_binary_path(path) == expected

