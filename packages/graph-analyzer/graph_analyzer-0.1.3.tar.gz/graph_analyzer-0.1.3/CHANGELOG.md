# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.3] - 2026-01-14

### Changed
- Updated author email to mujadid2001@gmail.com
- Removed non-existent website links from documentation
- Updated contact information across all documentation
- Cleaned repository structure (removed temporary test files)
- Improved MANIFEST.in to exclude development files

### Fixed
- Removed placeholder "your-username" from contributing guide
- Removed "once published" note from installation instructions

## [0.1.2] - 2026-01-13

### Changed
- Cleaned repository structure for professional presentation
- Removed internal documentation and build artifacts
- Reorganized documentation (SETUP_GUIDE.md → DEVELOPMENT.md)
- Enhanced .gitignore for better repository hygiene
- Improved code formatting and documentation consistency

### Fixed
- All code style issues resolved (0 flake8 warnings)
- Repository now follows best practices of popular pip packages

## [0.1.1] - 2026-01-13

### Improved
- Enhanced node detection parameters for better accuracy
- Improved Hough Circle Transform sensitivity (minRadius: 8, param2: 25)
- Better handling of hand-drawn graph variations
- Updated example to demonstrate multiple edges detection
- Fixed test image generation for more reliable demonstrations

### Fixed
- Improved node detection reliability
- Better circle detection for various drawing styles
- Enhanced example scripts for clearer demonstrations

## [0.1.0] - 2026-01-13

### Added
- Initial release of Graph Analyzer
- Core functionality for analyzing hand-drawn graphs from images
- Graph detection using computer vision (OpenCV)
  - Node detection via Hough Circle Transform and contour analysis
  - Edge detection via Hough Line Transform and connectivity analysis
- Simple graph validation
  - Self-loop detection
  - Multiple edge detection
  - Connectivity analysis
- Comprehensive error handling
  - InvalidImageError for invalid image files
  - NoGraphDetectedError when no graph is found
  - GraphValidationError for validation failures
- Detailed analysis results
  - Confidence scoring
  - Graph properties (connectivity, degree, etc.)
  - Issue reporting
- Visualization capabilities
  - Visualize detected nodes and edges
  - Save visualization to file
- Complete documentation
  - README with usage examples
  - API reference
  - Contributing guidelines
  - Code of conduct
- Example scripts
  - Basic usage example
  - Batch processing example
  - Test image generator
- Comprehensive test suite
  - Unit tests for all major components
  - Integration tests
  - Test fixtures and utilities
- Standard Python packaging
  - setup.py for pip installation
  - pyproject.toml for modern build system
  - requirements.txt for dependencies
  - MANIFEST.in for package data

### Dependencies
- numpy >= 1.21.0
- opencv-python >= 4.5.0
- Pillow >= 8.0.0

[0.1.1]: https://github.com/mujadid2001/graph-analyzer/releases/tag/v0.1.1
[0.1.0]: https://github.com/mujadid2001/graph-analyzer/releases/tag/v0.1.0
