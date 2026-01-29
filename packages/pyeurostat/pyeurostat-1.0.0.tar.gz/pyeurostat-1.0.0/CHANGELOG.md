# Changelog

All notable changes to this project will be documented in this file.

## [1.0.0] - 2026-01-15

### Added
- Initial release of eurostat-improved
- EuroStatExplorer class with enhanced API
- Fixed critical `flags=True` bug from original library
- Automatic retry mechanism with multiple fallback strategies
- Raw SDMX API access for reliable flag downloads
- `download_with_filters()` method with loop support
- `get_available_filters()` for dynamic filter discovery
- `unpivot_data()` for long-format conversion
- Comprehensive documentation and examples
- MIT License

### Fixed
- Column mismatch error when using `flags=True` (270 columns passed, passed data had 269 columns)
- Proper handling of missing/malformed data in flag columns
- Graceful fallback when SDMX data is incomplete

### Improved
- Better error messages and progress indicators
- Verbose mode with detailed download status
- Support for large dataset downloads with looping
- Compatible with Python 3.8+
