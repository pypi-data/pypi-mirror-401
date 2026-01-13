# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.1]

### Added
- PyPI version and downloads badges to README
- Changelog section link in README
- Changelog and Discussions URLs to project metadata in pyproject.toml

### Changed
- Improved package description in README and pyproject.toml - reordered text to prioritize main functionality description


## [1.0.0]

### Added
- Initial release of binary-extensions Python package
- `is_binary_extension()` function to check if a file extension is binary
- `is_binary_path()` function to check if a file path has a binary extension
- `BINARY_EXTENSIONS` frozenset containing 250+ known binary file extensions
- `BINARY_EXTENSIONS_LOWER` constant containing all binary extensions in lowercase for optimized case-insensitive lookups
- Support for case-insensitive extension checks
- Dot-aware extension handling (supports both "png" and ".png" formats)
- Dotfile support in `is_binary_path()` function - now handles files like `.DS_Store` where the entire filename (without leading dot) is treated as the extension
- Comprehensive test suite with unit and integration tests
- Type hints for better IDE support and type checking
- Zero dependencies for minimal overhead

### Features
- Immutable collection of hundreds of known binary file extensions
- Fast membership checks using `frozenset`
- Support for images, videos, archives, executables, documents, fonts, and more
- Python 3.8+ compatibility

[1.0.1]: https://github.com/ysskrishna/binary-extensions/compare/v1.0.0...v1.0.1
[1.0.0]: https://github.com/ysskrishna/binary-extensions/releases/tag/v1.0.0

