# Claude Instructions for Trix Python SDK

## Coding Standards

**IMPORTANT**: Before writing or modifying code, review and follow the guidelines in [CODING_STANDARDS.md](./CODING_STANDARDS.md).

Key constraints:
- **File limit**: Keep files under 300 lines (hard limit: 500)
- **Function limit**: Keep functions under 25 lines (hard limit: 40)
- **Scope**: Only make changes directly requested - no speculative improvements
- **Coupling**: If a change touches >3 files, pause and discuss the approach first

## Python-Specific Guidelines

### Code Quality Tools

This project uses the following tools (configured in `pyproject.toml`):

| Tool | Purpose | Config |
|------|---------|--------|
| **black** | Code formatting | line-length=100, target py39 |
| **ruff** | Linting | line-length=100, target py39 |
| **mypy** | Type checking | strict mode enabled |
| **pytest** | Testing | asyncio_mode=auto |

### Style Requirements

- Use type hints for all function signatures
- Follow PEP 8 conventions
- Use `async`/`await` for I/O operations (httpx is async)
- Prefer Pydantic models for data validation
- Keep imports organized (stdlib, third-party, local)

## Project Structure

```
trix-sdk-python/
├── src/
│   └── trix/           # Main package
├── tests/              # Test files
├── examples/           # Usage examples
├── pyproject.toml      # Project config & dependencies
└── Makefile            # Common commands
```

## Common Commands

```bash
# Install for development
pip install -e ".[dev]"

# Or using make
make install-dev

# Run tests
pytest
make test

# Run tests with coverage
pytest --cov=trix --cov-report=html
make test-cov

# Format code
black src/ tests/ examples/
make format

# Lint code
ruff check src/ tests/
make lint

# Type check
mypy src/
make type-check

# Run all quality checks
make quality
```

## Testing Guidelines

- Use `pytest-asyncio` for async tests (auto mode enabled)
- Use `respx` for mocking HTTP requests
- Place tests in `tests/` mirroring `src/` structure
- Test file naming: `test_<module>.py`

## Code Quality Checklist

Before submitting changes:
- [ ] Follows coding standards (file/function size limits)
- [ ] Type hints added for new functions
- [ ] `black` formatting applied
- [ ] `ruff` passes with no errors
- [ ] `mypy` passes with no errors
- [ ] Tests added for new functionality
- [ ] No secrets or sensitive data exposed
