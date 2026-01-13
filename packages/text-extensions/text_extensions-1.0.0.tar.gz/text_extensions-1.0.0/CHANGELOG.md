# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0]

### Added
- Initial release of text-extensions Python package
- `is_text_extension()` function to check if a file extension is text
- `is_text_path()` function to check if a file path has a text extension
- `TEXT_EXTENSIONS` frozenset containing 300+ known text file extensions
- `TEXT_EXTENSIONS_LOWER` constant containing all text extensions in lowercase for optimized case-insensitive lookups
- Support for case-insensitive extension checks
- Dot-aware extension handling (supports both "txt" and ".txt" formats)
- Dotfile support in `is_text_path()` function - now handles files like `.gitignore` where the entire filename (without leading dot) is treated as the extension
- Comprehensive test suite with unit and integration tests
- Type hints for better IDE support and type checking
- Zero dependencies for minimal overhead

### Features
- Immutable collection of hundreds of known text file extensions
- Fast membership checks using `frozenset`
- Support for source code, markup, data formats, configuration files, and more
- Python 3.8+ compatibility

[1.0.0]: https://github.com/ysskrishna/text-extensions/releases/tag/v1.0.0

