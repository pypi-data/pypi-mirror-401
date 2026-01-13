# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.0] - 2026-01-10

### Added
- Initial release of FeatureExpand
- `FeatureExpander` class for automatic feature engineering via Exactor API
- `LinearModelBooster` for automatic model selection with feature expansion
- Support for both boolean and continuous feature generation
- Scikit-learn compatible transformers
- Neural network guidance utilities
- Comprehensive examples for regression, classification, and forex prediction
- Full documentation with tutorials and API reference
- Unit tests for core functionality
- GitHub Actions CI/CD pipeline
- PyPI packaging configuration

### Features
- Boolean formula simplification using Exactor API
- Automatic discretization of continuous targets
- Caching mechanism for API calls
- MinMax scaling integration
- Cross-validation based model selection
- Support for polynomial and logic-guided regression
- Flexible precision control (deep parameter)
- Environment switching (DEV/PROD)

### Documentation
- Quick start guide
- Installation instructions
- Usage examples for various scenarios
- API reference documentation
- Contributing guidelines
- MIT License

[0.1.0]: https://github.com/jlopezCell/featureexpand/releases/tag/v0.1.0
