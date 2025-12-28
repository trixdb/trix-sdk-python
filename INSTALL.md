# Installation Guide

## Quick Install

### From PyPI (Recommended)

Once published, install the latest stable version:

```bash
pip install trixdb
```

### From Source

For the latest development version:

```bash
git clone https://github.com/trixdb/trix-python-sdk.git
cd trix-python-sdk
pip install -e .
```

## Requirements

- **Python**: 3.9 or higher
- **Operating System**: Linux, macOS, or Windows
- **Dependencies**: Automatically installed with pip
  - httpx >= 0.25.0
  - pydantic >= 2.0.0
  - typing-extensions >= 4.5.0

## Installation Methods

### 1. Standard Installation

```bash
pip install trixdb
```

### 2. Development Installation

For contributing or development:

```bash
git clone https://github.com/trixdb/trix-python-sdk.git
cd trix-python-sdk
pip install -e ".[dev]"
```

This installs additional development dependencies:
- pytest
- pytest-asyncio
- pytest-cov
- black
- ruff
- mypy
- respx

### 3. Using Virtual Environment (Recommended)

#### Using venv

```bash
# Create virtual environment
python -m venv venv

# Activate (Linux/macOS)
source venv/bin/activate

# Activate (Windows)
venv\Scripts\activate

# Install TrixDB
pip install trixdb
```

#### Using conda

```bash
# Create conda environment
conda create -n trixdb python=3.11

# Activate environment
conda activate trixdb

# Install TrixDB
pip install trixdb
```

### 4. Using pipx (Isolated Installation)

```bash
pipx install trixdb
```

### 5. Using Poetry

```bash
# Add to your project
poetry add trixdb

# Or for development
poetry add --group dev trixdb
```

## Verify Installation

After installation, verify it works:

```python
python -c "import trixdb; print(f'TrixDB SDK v{trixdb.__version__}')"
```

Or run the test suite:

```bash
# If installed with dev dependencies
pytest
```

## Platform-Specific Notes

### Linux

Standard pip installation should work:

```bash
pip install trixdb
```

### macOS

For best compatibility:

```bash
# Update pip first
pip install --upgrade pip

# Install TrixDB
pip install trixdb
```

### Windows

Use PowerShell or Command Prompt:

```powershell
# Update pip
python -m pip install --upgrade pip

# Install TrixDB
pip install trixdb
```

## Troubleshooting

### Issue: "No module named 'trixdb'"

**Solution**: Make sure you've activated your virtual environment and installed the package:

```bash
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install trixdb
```

### Issue: "ImportError: cannot import name..."

**Solution**: Ensure you have the correct version installed:

```bash
pip install --upgrade trixdb
```

### Issue: Dependency conflicts

**Solution**: Try installing in a fresh virtual environment:

```bash
python -m venv fresh_env
source fresh_env/bin/activate
pip install trixdb
```

### Issue: SSL/Certificate errors

**Solution**: Update certifi:

```bash
pip install --upgrade certifi
```

### Issue: Permission denied

**Solution**: Install for current user only:

```bash
pip install --user trixdb
```

Or use a virtual environment (recommended).

## Upgrading

### Upgrade to Latest Version

```bash
pip install --upgrade trixdb
```

### Upgrade to Specific Version

```bash
pip install trixdb==0.1.0
```

### Check Current Version

```bash
pip show trixdb
```

Or in Python:

```python
import trixdb
print(trixdb.__version__)
```

## Uninstallation

```bash
pip uninstall trixdb
```

## Development Setup

For contributors:

1. Fork and clone the repository:
   ```bash
   git clone https://github.com/YOUR_USERNAME/trix-python-sdk.git
   cd trix-python-sdk
   ```

2. Create virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate
   ```

3. Install in editable mode with dev dependencies:
   ```bash
   pip install -e ".[dev]"
   ```

4. Verify installation:
   ```bash
   pytest
   black --check src/
   ruff check src/
   mypy src/
   ```

## Docker Setup

If you prefer using Docker:

```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

CMD ["python", "your_script.py"]
```

## Next Steps

After installation:

1. **Get API Key**: Sign up at https://trixdb.com and get your API key
2. **Quick Start**: Run `examples/quickstart.py` to test the SDK
3. **Documentation**: Read `README.md` for comprehensive usage guide
4. **Examples**: Explore `examples/` directory for more examples

## Support

If you encounter installation issues:

1. Check the [Troubleshooting](#troubleshooting) section above
2. Open an issue: https://github.com/trixdb/trix-python-sdk/issues
3. Email: support@trixdb.com

## System Requirements Summary

| Component | Requirement |
|-----------|-------------|
| Python | 3.9+ |
| pip | Latest version recommended |
| OS | Linux, macOS, Windows |
| Internet | Required for API calls |
| Disk Space | ~10 MB |
| Memory | ~50 MB runtime |

## Optional Dependencies

For specific features, you may want to install:

```bash
# For Jupyter notebook support
pip install jupyter ipython

# For async REPL
pip install asyncio ipython

# For better tracebacks
pip install rich
```

---

**Need Help?** Visit https://docs.trixdb.com or email support@trixdb.com
