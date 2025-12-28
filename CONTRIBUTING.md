# Contributing to TrixDB Python SDK

Thank you for your interest in contributing to the TrixDB Python SDK! This document provides guidelines and instructions for contributing.

## Development Setup

### Prerequisites

- Python 3.9 or higher
- Git

### Setting Up Your Development Environment

1. Fork the repository on GitHub

2. Clone your fork locally:
   ```bash
   git clone https://github.com/YOUR_USERNAME/trix-python-sdk.git
   cd trix-python-sdk
   ```

3. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

4. Install the package in development mode with dev dependencies:
   ```bash
   pip install -e ".[dev]"
   ```

5. Create a new branch for your changes:
   ```bash
   git checkout -b feature/your-feature-name
   ```

## Code Quality Standards

### Code Style

We use the following tools to maintain code quality:

- **Black** for code formatting
- **Ruff** for linting
- **MyPy** for type checking

Before submitting a PR, ensure your code passes all checks:

```bash
# Format code
black src/ tests/

# Lint code
ruff check src/ tests/

# Type check
mypy src/
```

### Type Hints

All code must include comprehensive type hints. We follow PEP 484 and use Python 3.9+ type hint syntax.

```python
# Good
def process_memory(memory_id: str, priority: Optional[int] = None) -> Memory:
    ...

# Bad
def process_memory(memory_id, priority=None):
    ...
```

### Docstrings

All public functions, classes, and methods must have docstrings following Google style:

```python
def create_memory(
    content: str,
    tags: Optional[List[str]] = None,
) -> Memory:
    """
    Create a new memory.

    Args:
        content: The memory content
        tags: Optional list of tags

    Returns:
        Created memory object

    Raises:
        ValidationError: If content is empty

    Example:
        >>> memory = create_memory("Hello", tags=["greeting"])
    """
```

## Testing

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=trixdb --cov-report=html

# Run specific test file
pytest tests/test_memories.py

# Run specific test
pytest tests/test_memories.py::test_create_memory
```

### Writing Tests

- Place tests in the `tests/` directory
- Test files should be named `test_*.py`
- Test functions should be named `test_*`
- Use fixtures from `conftest.py` when appropriate
- Aim for high test coverage (>80%)

Example test:

```python
def test_create_memory(sync_client, mock_memory_response, respx_mock):
    """Test memory creation."""
    # Mock the API response
    respx_mock.post("/memories").mock(return_value=httpx.Response(
        200, json=mock_memory_response
    ))

    # Test the function
    memory = sync_client.memories.create(content="Test")

    # Assert the results
    assert memory.id == "mem_123"
    assert memory.content == "Test memory content"
```

## Pull Request Process

1. **Update Documentation**: Update README.md and docstrings as needed

2. **Add Tests**: Ensure your changes are covered by tests

3. **Update Changelog**: Add a note about your changes to the CHANGELOG.md

4. **Run Quality Checks**:
   ```bash
   black src/ tests/
   ruff check src/ tests/
   mypy src/
   pytest
   ```

5. **Commit Your Changes**:
   ```bash
   git add .
   git commit -m "feat: add new feature"
   ```

   Use conventional commit messages:
   - `feat:` for new features
   - `fix:` for bug fixes
   - `docs:` for documentation changes
   - `test:` for test additions/changes
   - `refactor:` for code refactoring
   - `chore:` for maintenance tasks

6. **Push to Your Fork**:
   ```bash
   git push origin feature/your-feature-name
   ```

7. **Create a Pull Request**: Go to GitHub and create a PR from your fork

## Adding New Features

When adding new API endpoints or features:

1. **Add Type Models** to `src/trixdb/types.py`:
   ```python
   class NewFeature(BaseResponse):
       """Description of the feature."""
       id: str
       name: str
       created_at: datetime
   ```

2. **Create Resource Class** in `src/trixdb/resources/`:
   ```python
   class NewFeatureResource:
       """Resource for managing new features."""

       def create(self, name: str) -> NewFeature:
           """Create a new feature."""
           ...
   ```

3. **Add to Client** in `src/trixdb/client.py`:
   ```python
   self.new_feature = NewFeatureResource(self)
   ```

4. **Write Tests** in `tests/test_new_feature.py`

5. **Update Documentation** in README.md

6. **Export Types** in `src/trixdb/__init__.py`

## Reporting Issues

When reporting issues, please include:

- Python version
- SDK version
- Minimal code to reproduce the issue
- Expected behavior
- Actual behavior
- Error messages and stack traces

## Code of Conduct

- Be respectful and inclusive
- Focus on constructive feedback
- Help others learn and grow
- Follow the project's coding standards

## Questions?

If you have questions, feel free to:

- Open an issue on GitHub
- Email us at support@trixdb.com
- Check the documentation at https://docs.trixdb.com

Thank you for contributing to TrixDB Python SDK!
