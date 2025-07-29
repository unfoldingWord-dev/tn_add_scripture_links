# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2025-07-29

### Added

- Initial release of the Translation Notes Scripture Links Tool
- Automatic detection and linking of Bible references in TN TSV files
- Support for various reference formats:
  - Book names with chapters/verses (e.g., "Gen 1:1", "Psalms 2, 8, 16")
  - Chapter references (e.g., "chapter 5", "chapters 2-8")
  - Verse references (e.g., "verse 12", "verses 5-7")
  - Chapter:verse notation (e.g., "5:12", "1:1–6:7")
- Smart link generation with appropriate relative paths
- Batch processing capabilities for single files, directories, or multiple files
- Change tracking with diff file generation
- In-place modification option
- Comprehensive book name to USFM code mapping
- Special handling for single-chapter books
- Context-aware linking (avoids self-references)
- Support for existing markdown link preservation

### Features

- Command-line interface with argparse
- Robust error handling and logging
- Cross-platform compatibility (Windows, macOS, Linux)
- No external dependencies (uses Python standard library only)
- Detailed documentation and examples

### Documentation

- Comprehensive README with usage examples
- Setup configuration for pip installation
- MIT License
- Changelog for version tracking
- Proper .gitignore for Python projects
