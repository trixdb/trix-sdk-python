# Trix Python SDK Examples

This directory contains example scripts demonstrating various features of the Trix Python SDK.

## Available Examples

### 1. quickstart.py

**Purpose**: Get started with Trix in under 5 minutes

**What it demonstrates**:
- Creating memories
- Creating relationships
- Searching memories
- Creating clusters
- Adding memories to clusters
- Creating spaces
- Finding similar memories
- Graph traversal
- Updating memories

**Run it**:
```bash
python examples/quickstart.py
```

**Note**: Update the `API_KEY` variable before running!

---

### 2. basic_usage.py

**Purpose**: Comprehensive synchronous usage examples

**What it demonstrates**:
- All CRUD operations for memories
- Relationship management
- Cluster operations
- Graph traversal
- Search functionality
- Highlight creation
- Feedback submission
- Iteration patterns

**Run it**:
```bash
python examples/basic_usage.py
```

**Covers**:
- ✓ Memories
- ✓ Relationships
- ✓ Clusters
- ✓ Spaces
- ✓ Graph operations
- ✓ Search
- ✓ Highlights
- ✓ Feedback

---

### 3. async_usage.py

**Purpose**: Demonstrate asynchronous operations

**What it demonstrates**:
- Async client initialization
- Concurrent memory creation
- Async iteration
- Agent sessions
- Parallel operations with `asyncio.gather`
- Context managers with async

**Run it**:
```bash
python examples/async_usage.py
```

**Key features**:
- Uses `AsyncTrix` client
- Shows how to use `async/await`
- Demonstrates concurrent operations
- Async pagination

---

### 4. error_handling.py

**Purpose**: Best practices for error handling

**What it demonstrates**:
- Catching specific exceptions
- Handling rate limits
- Retry logic
- Graceful degradation
- Context manager cleanup
- Custom retry strategies

**Run it**:
```bash
python examples/error_handling.py
```

**Covers**:
- `NotFoundError`
- `ValidationError`
- `AuthenticationError`
- `RateLimitError`
- `ServerError`
- General `TrixError`

---

## Prerequisites

Before running any example:

1. **Install the SDK**:
   ```bash
   pip install trixdb
   ```

2. **Get an API Key**:
   - Sign up at https://trixdb.com
   - Get your API key from the dashboard

3. **Set your API key** in the example:
   - Update `API_KEY = "your_api_key"` in the script, or
   - Set environment variable: `export TRIX_API_KEY=your_key`

## Running Examples

### Basic run:
```bash
python examples/quickstart.py
```

### Using environment variable:
```bash
export TRIX_API_KEY="your_api_key"
python examples/basic_usage.py
```

### With custom base URL:
```python
client = Trix(
    api_key="your_api_key",
    base_url="https://custom.api.url"
)
```

## Example Output

### quickstart.py output:
```
============================================================
Trix Python SDK - Quick Start
============================================================

1. Creating memories...
   ✓ Created memory 1: mem_abc123
   ✓ Created memory 2: mem_def456
   ✓ Created memory 3: mem_ghi789

2. Creating relationships...
   ✓ Created relationship: rel_xyz123

3. Searching memories...
   ✓ Found 3 memories matching 'Python'
      1. The Python programming language was created by Guido...
      2. Python emphasizes code readability with significant...
      3. Python is widely used in data science and machine l...

...
```

## Common Patterns

### Pattern 1: Context Manager (Recommended)
```python
from trix import Trix

with Trix(api_key="your_api_key") as client:
    memory = client.memories.create(content="Hello")
    # Client automatically closed
```

### Pattern 2: Manual Cleanup
```python
from trix import Trix

client = Trix(api_key="your_api_key")
try:
    memory = client.memories.create(content="Hello")
finally:
    client.close()
```

### Pattern 3: Async Context Manager
```python
from trix import AsyncTrix

async with AsyncTrix(api_key="your_api_key") as client:
    memory = await client.memories.create(content="Hello")
    # Client automatically closed
```

### Pattern 4: Error Handling
```python
from trix import Trix, NotFoundError

client = Trix(api_key="your_api_key")
try:
    memory = client.memories.get("invalid_id")
except NotFoundError:
    print("Memory not found!")
```

## Building Your Own Examples

Start with this template:

```python
#!/usr/bin/env python3
"""My Trix Example"""

from trix import Trix

def main():
    # Initialize client
    with Trix(api_key="your_api_key") as client:
        # Your code here
        memory = client.memories.create(
            content="My first memory"
        )
        print(f"Created: {memory.id}")

if __name__ == "__main__":
    main()
```

## Tips

1. **API Keys**: Never commit API keys to version control
2. **Rate Limits**: The SDK automatically retries on rate limits
3. **Pagination**: Use `.iter()` for large datasets
4. **Async**: Use async client for high-throughput applications
5. **Cleanup**: Always close clients or use context managers
6. **Errors**: Catch specific exceptions for better error handling

## More Resources

- **Documentation**: See `../README.md`
- **API Reference**: https://docs.trixdb.com
- **Contributing**: See `../CONTRIBUTING.md`
- **Issues**: https://github.com/trixdb/trix-sdk-python/issues

## Need Help?

- Open an issue on GitHub
- Email: support@trixdb.com
- Documentation: https://docs.trixdb.com

---

Happy coding with Trix!
