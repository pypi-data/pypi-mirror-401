# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.1] - 2026-01-09

### Added
- Complete GitHub automation workflows for CI/CD
- Automated PyPI publishing on releases
- GitHub issue and PR templates for better collaboration
- Contributing guidelines and setup documentation
- Release management script for easy version updates

### Fixed
- Improved test reliability by adding pytest-xdist availability checks
- Simplified CI workflows to avoid dependency conflicts
- Better error handling in parallel execution tests

### Changed
- Enhanced README with CI badges and contributing links
- Added .kiro/ to .gitignore to exclude IDE-specific files

## [0.1.0] - 2026-01-08

### Added
- Initial release of pytest-selenium-driver
- WebDriver fixture with automatic setup and cleanup
- Support for Chrome and Firefox browsers
- Headless mode support
- Remote WebDriver execution via Selenium Grid
- Parallel execution support with pytest-xdist
- Comprehensive CLI options for configuration
- Thread-safe WebDriver creation and management
- CI environment detection and optimization
- Property-based testing integration with Hypothesis

### Features
- Zero-boilerplate WebDriver fixture for pytest
- Automatic browser driver management via Selenium Manager
- Configurable browser options with sensible defaults
- Error handling with descriptive messages and troubleshooting guidance
- Logging support for debugging WebDriver operations
- Multiple fixture scopes (function, class, session)
- Worker process isolation for parallel test execution