# Contributing to Graph Analyzer

Thank you for your interest in contributing to Graph Analyzer! This document provides guidelines and instructions for contributing.

## Code of Conduct

- Be respectful and inclusive
- Provide constructive feedback
- Focus on what is best for the community
- Show empathy towards other community members

## How to Contribute

### Reporting Bugs

If you find a bug, please create an issue with:

1. A clear, descriptive title
2. Steps to reproduce the problem
3. Expected behavior
4. Actual behavior
5. Screenshots (if applicable)
6. Your environment (OS, Python version, package version)

### Suggesting Enhancements

Enhancement suggestions are tracked as GitHub issues. When creating an enhancement suggestion, please include:

1. A clear, descriptive title
2. Detailed description of the proposed feature
3. Explain why this enhancement would be useful
4. Possible implementation approach (optional)

### Pull Requests

1. **Fork the repository** and create your branch from `main`
2. **Install development dependencies**: `pip install -e ".[dev]"`
3. **Make your changes**:
   - Write clear, commented code
   - Follow the existing code style
   - Add tests for new functionality
   - Update documentation as needed
4. **Test your changes**:
   - Run the test suite: `pytest`
   - Ensure all tests pass
   - Check code coverage: `pytest --cov=graph_analyzer`
5. **Format your code**:
   - Run Black: `black graph_analyzer/`
   - Run Flake8: `flake8 graph_analyzer/`
6. **Commit your changes**:
   - Use clear, descriptive commit messages
   - Reference any related issues
7. **Push to your fork** and submit a pull request

## Development Setup

```bash
# Clone your fork
git clone https://github.com/mujadid2001/graph-analyzer.git
cd graph-analyzer

# Create a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install in development mode with dev dependencies
pip install -e ".[dev]"

# Run tests
pytest

# Format code
black graph_analyzer/

# Check code style
flake8 graph_analyzer/
```

## Code Style

- Follow PEP 8 guidelines
- Use Black for code formatting (line length: 100)
- Use type hints where appropriate
- Write descriptive docstrings for all public functions and classes
- Keep functions focused and modular

### Docstring Format

```python
def function_name(param1: Type1, param2: Type2) -> ReturnType:
    """
    Brief description of what the function does.
    
    More detailed description if needed, explaining the function's
    purpose and behavior.
    
    Args:
        param1: Description of param1
        param2: Description of param2
    
    Returns:
        Description of return value
    
    Raises:
        ExceptionType: Description of when this exception is raised
    """
    pass
```

## Testing Guidelines

- Write tests for all new functionality
- Aim for high code coverage (>80%)
- Use descriptive test names: `test_should_do_something_when_condition`
- Use fixtures for reusable test data
- Test both success and failure cases
- Test edge cases

### Test Structure

```python
def test_feature_name():
    """Test that feature works correctly."""
    # Arrange - Set up test data
    analyzer = GraphAnalyzer()
    
    # Act - Perform the action
    result = analyzer.some_method()
    
    # Assert - Verify the result
    assert result == expected_value
```

## Commit Message Guidelines

- Use the present tense ("Add feature" not "Added feature")
- Use the imperative mood ("Move cursor to..." not "Moves cursor to...")
- Limit the first line to 72 characters or less
- Reference issues and pull requests after the first line

### Examples

```
Add support for PNG image format

- Implement PNG loader in image processor
- Add tests for PNG handling
- Update documentation

Fixes #123
```

## Documentation

- Update README.md for user-facing changes
- Update docstrings for code changes
- Add examples for new features
- Keep documentation clear and concise

## Review Process

1. All submissions require review before merging
2. Maintainers will review your PR and may request changes
3. Make requested changes and push to your branch
4. Once approved, a maintainer will merge your PR

## Questions?

Feel free to create an issue with the "question" label if you have any questions about contributing!

Issue Tracker: https://github.com/mujadid2001/graph-analyzer/issues

## License

By contributing, you agree that your contributions will be licensed under the MIT License.
