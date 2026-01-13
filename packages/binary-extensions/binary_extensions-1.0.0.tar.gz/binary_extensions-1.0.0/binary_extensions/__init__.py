import os.path
from binary_extensions._data import BINARY_EXTENSIONS, BINARY_EXTENSIONS_LOWER

__all__ = ["BINARY_EXTENSIONS", "BINARY_EXTENSIONS_LOWER", "is_binary_extension", "is_binary_path"]

def is_binary_extension(ext: str) -> bool:
    """
    Return True if the given file extension is known to be binary.

    Examples:
        >>> is_binary_extension("png")
        True
        >>> is_binary_extension(".txt")
        False
    """
    return ext.lower().lstrip(".") in BINARY_EXTENSIONS_LOWER

def is_binary_path(file_path: str) -> bool:
    """
    Return True if the file path has a binary file extension.

    Examples:
        >>> is_binary_path("image.png")
        True
        >>> is_binary_path("document.txt")
        False
        >>> is_binary_path("/path/to/file.JPG")
        True
    """
    basename = os.path.basename(file_path)
    _, ext = os.path.splitext(file_path)
    
    # Handle dotfiles (files starting with a dot that have no extension)
    # e.g., .something where "something" is a binary extension
    if not ext and basename.startswith(".") and len(basename) > 1:
        # Treat the entire filename (without leading dot) as the extension
        ext = basename[1:]
    else:
        ext = ext.lstrip(".")
    
    return ext.lower() in BINARY_EXTENSIONS_LOWER
