# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.3.0] - 2026-01-13

### Changed
- Removed alphabetical sorting of columns in wide CSV tables to preserve natural data order

## [0.2.0] - 2026-01-11

### Added
- Batch processing support with `parse_files_batch()` for significantly faster multi-file processing
- Optimized I/O for wide CSV files to reduce file rewriting overhead

### Changed
- `parse_file()` now returns parsed data dictionary

## [0.1.0] - 2026-01-11

### Added
- Initial release
- Modular parser architecture with base class and subparsers
- `HPCapParser` main parser coordinating multiple subparsers
- `ProductParser` for extracting product metadata
- `ImagesParser` for extracting image data
- `DocumentsParser` for extracting document information
- `LinksParser` for extracting product links and relationships
- `MarketingMessagingParser` for extracting marketing content from features and special_features sections
- `TechSpecsParser` for extracting technical specifications
- Data models: `Product`, `Image`, `Document`, `Link`, `MarketingMessaging`, `TechSpec`
- CSV output for all parsed sections
- Wide CSV format for marketing messaging and tech specs with dynamic column handling
- Append mode for incremental CSV updates
- Comprehensive test suite
- Development sandbox for testing without reinstalls
- GitHub Actions workflow for PyPI publishing
