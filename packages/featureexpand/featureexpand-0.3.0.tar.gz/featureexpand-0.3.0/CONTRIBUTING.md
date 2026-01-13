# Contributing to FeatureExpand

Thank you for your interest in contributing to FeatureExpand! This document provides guidelines and instructions for contributing.

## Code of Conduct

Be respectful and constructive in all interactions with the community.

## How to Contribute

### Reporting Bugs

If you find a bug, please create an issue with:
- A clear, descriptive title
- Steps to reproduce the issue
- Expected behavior vs actual behavior
- Your environment (Python version, OS, package versions)
- Minimal code example demonstrating the issue

### Suggesting Enhancements

Feature requests are welcome! Please create an issue describing:
- The use case and problem you're trying to solve
- Your proposed solution
- Any alternatives you've considered

### Pull Requests

1. **Fork the repository** and create your branch from `main`
2. **Set up development environment**:
   ```bash
   git clone https://github.com/yourusername/featureexpand.git
   cd featureexpand
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -e ".[dev]"
   ```

3. **Make your changes**:
   - Write clear, readable code following PEP 8
   - Add docstrings for all public functions/classes
   - Include type hints where appropriate
   - Update documentation if needed

4. **Add tests**:
   - Write tests for new functionality
   - Ensure all tests pass: `pytest tests/`
   - Maintain or improve code coverage

5. **Format your code**:
   ```bash
   black featureexpand/
   flake8 featureexpand/
   ```

6. **Commit your changes**:
   - Use clear, descriptive commit messages
   - Reference issues in commits (e.g., "Fix bug in FeatureExpander #123")

7. **Push to your fork** and submit a pull request

8. **Wait for review**:
   - Address any feedback from maintainers
   - Make requested changes promptly

## Development Guidelines

### Code Style

- Follow [PEP 8](https://www.python.org/dev/peps/pep-0008/)
- Use Black for formatting (line length: 100)
- Use meaningful variable and function names
- Keep functions focused and modular

### Documentation

- All public APIs must have docstrings
- Use Google-style docstrings
- Update README.md for user-facing changes
- Add examples for new features

### Testing

- Write tests for all new functionality
- Use pytest for testing
- Aim for high code coverage (>80%)
- Test edge cases and error conditions

Example test:
```python
def test_feature_expander_basic():
    from featureexpand import FeatureExpander
    import numpy as np
    
    X = np.array([[0.1, 0.2], [0.3, 0.4]])
    y = np.array([0, 1])
    
    expander = FeatureExpander(token="test_token", environment="DEV")
    # Test assertions here
```

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=featureexpand --cov-report=html

# Run specific test file
pytest tests/test_feature_expander.py

# Run with verbose output
pytest -v
```

### Building Documentation

```bash
cd docs
mkdocs serve
# Visit http://127.0.0.1:8000
```

## Release Process

(For maintainers)

1. Update version in `pyproject.toml` and `featureexpand/__init__.py`
2. Update `CHANGELOG.md` with release notes
3. Create a git tag: `git tag -a v0.1.0 -m "Release v0.1.0"`
4. Push tag: `git push origin v0.1.0`
5. Build package: `python -m build`
6. Upload to PyPI: `twine upload dist/*`

## Questions?

Feel free to open an issue for any questions or concerns.

## License

By contributing, you agree that your contributions will be licensed under the MIT License.
