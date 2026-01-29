# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.2.3] - 2025-01-15

### Fixed
- Corrected author email address in package metadata.
- Fixed repository URLs pointing to correct GitHub location.

## [0.2.2] - 2025-01-15

### Fixed
- Removed 'index' command, only 'idx' is now valid for the index column mode.

## [0.2.1] - 2025-12-26

### Added
- Index column support: New `index` or `idx` mode to dedicate the first column to an index column with auto-numbering or custom labels.
- No index border option: New `-nib` parameter to remove the separator between index column and data columns.

### Changed
- Renamed internal references from CliTable to Tuible for consistency.

### Fixed
- Removed unused `-cc` parameter.
- Fixed index column width calculation.

## [0.1.1] - 2024-XX-XX

### Added
- Initial release with basic table formatting features.