# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.1.0] - 2026-01-10

### Added
- Recursive page discovery to find nested pages and child databases
- Automatic detection of `child_page` and `child_database` block types
- PageDiscoveryTracker class to prevent duplicate discoveries and infinite loops
- `--no-recursive` CLI flag to disable recursive discovery (opt-out)

### Changed
- Default behavior now includes recursive discovery of all nested content
- Discovery phase now scans page blocks for child references
- Progress messages updated to show "Discovering nested pages and databases..."

### Fixed
- Pages nested under other pages are now discovered and exported
- Pages in subfolders below database pages are now found
- Child databases are now properly discovered during export

## [1.0.0] - 2025-06-18

### Added
- GitHub Actions workflows for automated testing and PyPI publishing
- Continuous integration with Python 3.13 testing
- Automated release process with trusted PyPI publishing
- Production-ready distribution via PyPI

### Changed
- Improved code organization and linting compliance
- Enhanced documentation for release process

### Removed
- PUBLISHING.md (consolidated into RELEASING.md)

## [0.1.0] - 2025-06-15

### Added
- Initial release with full Notion workspace export functionality
- Export pages and databases to organized JSON files
- Rate limiting to respect Notion API limits (3 requests/second)
- Automatic retry with exponential backoff for transient failures
- Progress tracking with Rich terminal UI
- Search and discovery of all workspace content
- Individual page/database retrieval via CLI
- Comprehensive filtering options:
  - Filter by type (page/database)
  - Include/exclude patterns (regex)
  - Modified after date filtering
- Logging system with verbose/quiet modes
- Export manifest with metadata and statistics
- Support for nested page content (blocks)
- Sanitized filenames for cross-platform compatibility
- Environment variable support for API key
- Full test coverage with pytest
- Compatible with `uv` and `uvx` for easy execution

### Security
- API keys are never logged or exposed
- Secure handling of authentication tokens