# Trix Python SDK

Official Python SDK for [Trix](https://trixdb.com) - a powerful memory and knowledge management API.

[![PyPI version](https://badge.fury.io/py/trixdb.svg)](https://pypi.org/project/trixdb/)
[![Version](https://img.shields.io/badge/version-0.6.0-blue.svg)](https://github.com/trixdb/trix-sdk-python/releases)
[![Python Support](https://img.shields.io/pypi/pyversions/trixdb.svg)](https://pypi.org/project/trixdb/)
[![License: Apache 2.0](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)

## Features

- **Async-first design** with full sync support — `Trix` and `AsyncTrix`
- **Type-safe** — every request and response is a Pydantic model, and the package ships `py.typed`
- **Automatic retries** with exponential backoff and jitter, honoring `Retry-After`
- **Automatic idempotency** keys on every mutating request, so a safe retry never double-writes
- **Auto-pagination** helpers that yield typed models (`iter()` / `async for`)
- **SSE streaming** for bot runs (`bots.run_stream`)
- **Inbound webhook signature verification** — HMAC-SHA256, constant-time, replay-protected
- **Multipart file uploads** and signed binary downloads
- **Testing utilities** — `MockTrix` / `MockAsyncTrix` with call tracking
- **Broad API coverage** — memories, relationships, clusters, graph, search, agents/bots, facts, entities, webhooks, and more

## Installation

```bash
pip install trixdb
```

For development:

```bash
pip install "trixdb[dev]"
```

> **Package name vs. import name:** the distribution is published as **`trixdb`**
> on PyPI (`pip install trixdb`), but the import package is **`trix`**
> (`from trix import Trix`). This is intentional.

## Quick Start

### Synchronous

```python
from trix import Trix

client = Trix(api_key="your_api_key")

# Create a memory
memory = client.memories.create(
    content="Important information to remember",
    tags=["important", "note"],
    metadata={"source": "user_input"},
)
print(f"Created memory: {memory.id}")

# Search memories (hybrid = semantic + full-text)
results = client.memories.list(q="important", mode="hybrid", limit=10)
for result in results.data:
    print(f"- {result.content}")

client.close()
```

### Asynchronous

```python
import asyncio
from trix import AsyncTrix


async def main():
    async with AsyncTrix(api_key="your_api_key") as client:
        memory = await client.memories.create(content="Async memory", tags=["async"])

        # Auto-paginate. Note: `async for`, no `await`, and each item is a typed Memory.
        async for mem in client.memories.iter(page_size=50):
            print(mem.content)


asyncio.run(main())
```

### Context managers

```python
# Sync
with Trix(api_key="your_api_key") as client:
    memory = client.memories.create(content="Hello, Trix!")

# Async
async with AsyncTrix(api_key="your_api_key") as client:
    memory = await client.memories.create(content="Hello, Trix!")
```

## Authentication

Provide credentials via the constructor, or load them from the environment.

```python
from trix import Trix

# API key
client = Trix(api_key="your_api_key")

# JWT token
client = Trix(jwt_token="your_jwt_token")

# From the environment (recommended): reads TRIX_API_KEY (and optional TRIX_BASE_URL)
client = Trix.from_env()  # env_var defaults to "TRIX_API_KEY"
```

`AsyncTrix` accepts the same arguments and also exposes `AsyncTrix.from_env()`.

## Configuration

```python
from trix import Trix, PoolConfig
from trix.utils import RetryConfig

client = Trix(
    api_key="your_api_key",
    base_url="https://api.trixdb.com",   # default
    timeout=30.0,                         # request timeout in seconds (default)
    max_retries=3,                        # default
    retry_config=RetryConfig(max_retries=5),
    pool_config=PoolConfig(max_connections=100, max_keepalive_connections=20),
)
```

Request/response/error interceptors can also be passed to the constructor
(`request_interceptors`, `response_interceptors`, `error_interceptors`) to
observe or mutate traffic (for example, to inject custom headers).

## Core Resources

### Memories

Manage memories — the core unit of knowledge in Trix.

```python
from trix import MemoryCreate

# Create a memory
memory = client.memories.create(
    content="Machine learning is a subset of AI",
    type="text",
    tags=["ml", "ai"],
    metadata={"category": "education"},
    priority=5,
)

# Get / update / delete
memory = client.memories.get("mem_123")
updated = client.memories.update("mem_123", tags=["ml", "ai", "updated"], priority=10)
client.memories.delete("mem_123")

# List with filters
results = client.memories.list(q="machine learning", mode="hybrid", tags=["ml"], limit=20)

# Iterate through everything (auto-pagination, typed items)
for mem in client.memories.iter(page_size=100):
    print(mem.content)

# Bulk create
result = client.memories.bulk_create([
    MemoryCreate(content="First memory"),
    MemoryCreate(content="Second memory"),
])

# Audio memories
transcript = client.memories.transcribe("mem_audio_123", language="en")
audio_bytes = client.memories.stream_audio("mem_audio_123")
```

### Relationships

Create and manage relationships between memories.

```python
from trix import RelationshipType

rel = client.relationships.create(
    source_id="mem_123",
    target_id="mem_456",
    relationship_type=RelationshipType.SUPPORTS,
    description="This memory supports the other",
    weight=1.5,
    bidirectional=False,
)

incoming = client.relationships.get_incoming("mem_123")
outgoing = client.relationships.get_outgoing("mem_123")

rel = client.relationships.update("rel_123", weight=2.0, description="Stronger connection")
rel = client.relationships.reinforce("rel_123", boost=0.5)
client.relationships.delete("rel_123")
```

### Clusters

Group related memories together.

```python
from trix import ClusterCreate

cluster = client.clusters.create(
    name="ML Research",
    description="Machine learning research papers",
    color="#FF5733",
)

clusters = client.clusters.list(q="research", limit=50)

membership = client.clusters.add_memory(
    cluster_id="cluster_123", memory_id="mem_456", confidence=0.95
)
client.clusters.remove_memory("cluster_123", "mem_456")

# Suggest similar memories to expand the cluster
suggestions = client.clusters.expand("cluster_123", limit=20, threshold=0.7)

clusters = client.clusters.bulk_create([
    ClusterCreate(name="Cluster 1"),
    ClusterCreate(name="Cluster 2"),
])
```

### Spaces

Organize memories into separate workspaces.

```python
space = client.spaces.create(name="Personal", description="Personal memories and notes")
spaces = client.spaces.list()
space = client.spaces.get("space_123")
space = client.spaces.update("space_123", name="Personal (Updated)")
client.spaces.delete("space_123")
```

### Graph

Traverse and analyze the memory graph.

```python
from trix import Direction, RelationshipType

result = client.graph.traverse(
    start_ids=["mem_123", "mem_456"],
    depth=3,
    relationship_types=[RelationshipType.RELATED_TO],
    direction=Direction.OUTGOING,
)
for node in result.nodes:
    print(f"Memory: {node.memory.content}, Depth: {node.depth}")

# Semantic context around a query
context = client.graph.get_context(query="machine learning concepts", depth=2, semantic_limit=10)

# Shortest path between two memories
path = client.graph.shortest_path(source_id="mem_123", target_id="mem_456", max_hops=5)
if path:
    print(f"Path length: {path.distance}")
```

### Search

Semantic and keyword search capabilities.

```python
# Memories similar to a given one
results = client.search.similar(memory_id="mem_123", limit=20, threshold=0.7)
for result in results.data:
    print(f"{result.memory.content} (score: {result.score})")

# Generate embeddings for specific memories, or backfill everything
embeddings = client.search.embed(["mem_123", "mem_456"])
result = client.search.embed_all(batch_size=500)
print(f"Processed {result.total_processed} memories")

# Inspect server-side search configuration
config = client.search.get_config()
print(f"Max limit: {config.max_limit}")
```

### Agent Sessions

Manage conversational agent sessions.

```python
# Create a session
session = client.agent.create_session(session_id="chat_123", metadata={"user_id": "user_456"})

# Add memories to it
memory = client.agent.add_session_memory(
    session_id="chat_123", content="User asked about Python", role="user", importance=0.8
)

# Pull session-aware context
context = client.agent.get_context(
    query="What did we discuss about Python?", session_id="chat_123", limit=10
)

# List sessions, then end one with a summary
sessions = client.agent.list_sessions(limit=20)
session = client.agent.end_session(
    session_id="chat_123",
    summary="Discussed Python best practices",
    key_insights=["Use type hints", "Follow PEP 8"],
)
```

### Feedback

Improve search results with feedback.

```python
from trix import FeedbackResult

response = client.feedback.submit(
    query_context="machine learning",
    results=[
        FeedbackResult(memory_id="mem_123", score=0.9, rank=1),
        FeedbackResult(memory_id="mem_456", score=0.8, rank=2),
    ],
    boost_amount=0.5,
    create_relationships=True,
)

# Quick and batch variants
client.feedback.quick(memory_id="mem_123", useful=True, source_memory_id="mem_456")
client.feedback.batch(useful_ids=["mem_123", "mem_456"], not_useful_ids=["mem_789"])
```

### Highlights

Highlight and extract the important parts of memories.

```python
from trix import ExtractionType

highlight = client.highlights.create(
    memory_id="mem_123",
    text="This is the key insight",
    note="Important for later",
    importance=10,
    tags=["key-insight"],
    color="#FFFF00",
)

highlights = client.highlights.list("mem_123")
highlight = client.highlights.update("highlight_123", importance=5)
client.highlights.delete("highlight_123")

# Auto-extract highlights
extractions = client.highlights.extract(
    memory_id="mem_123",
    extraction_types=[ExtractionType.KEY_POINTS, ExtractionType.ENTITIES, ExtractionType.QUOTES],
    limit=10,
)
for extraction in extractions:
    print(f"Type: {extraction.extraction_type}")
```

### Facts

Read facts from the knowledge graph and attach new ones to memories.

```python
# List facts across the account, with optional filters
facts = client.facts.list(subject="Einstein", min_confidence=0.9, limit=20)
for fact in facts.data:
    print(f"{fact.subject} {fact.predicate} {fact.object} ({fact.confidence})")

# Read the facts attached to a specific memory
memory_facts = client.facts.list_for_memory("mem_123")

# Attach a new fact to a memory
fact = client.facts.create_for_memory(
    "mem_123",
    content="Project deadline is Friday",
    importance=8,
)
```

### Entities

Read named entities and merge duplicates.

```python
# List entities (optionally by type)
entities = client.entities.list(entity_type="person", limit=10)
for entity in entities.data:
    print(f"{entity.name} ({entity.type})")

# Convenience filter and single-entity read
people = client.entities.find_by_type("person")
entity = client.entities.get("ent_123")

# Facts about an entity
entity_facts = client.entities.get_facts("ent_123")
for fact in entity_facts.facts:
    print(f"{fact.subject} {fact.predicate} {fact.object}")

# Merge a duplicate into a canonical entity (source is deleted)
merged = client.entities.merge(target_id="ent_canonical", source_id="ent_duplicate")
print(f"Merged into: {merged.merged_entity.name}")
```

## Pagination

Every list endpoint has an `iter()` helper that transparently walks pages and
yields **typed models** (not raw dicts).

```python
# Sync: a plain iterator
for memory in client.memories.iter(page_size=100, max_items=1000):
    print(memory.content)

# Async: `async for`, no `await` on the iterator, still typed items
async for memory in client.memories.iter(page_size=100):
    print(memory.content)

# Manual pagination if you prefer to drive it yourself
offset = 0
limit = 100
while True:
    results = client.memories.list(limit=limit, offset=offset)
    for memory in results.data:
        print(memory.content)
    if len(results.data) < limit:
        break
    offset += limit
```

## Streaming

Bot runs can stream Server-Sent Events. `bots.run_stream` yields typed
`BotRunStep` events as they arrive.

```python
# Sync
for step in client.bots.run_stream("bot_123", message="Summarize my notes"):
    print(step.event, step.message or "")
```

```python
# Async — `async for`, no `await` on the iterator
async with AsyncTrix(api_key="your_api_key") as client:
    async for step in client.bots.run_stream("bot_123", message="Summarize my notes"):
        print(step.event, step.message or "")
```

Each `BotRunStep` carries an `event` plus optional `tool`, `args`, `result`,
`message`, `status`, and `error` fields.

## File Uploads

Upload files with multipart form data and fetch signed download URLs.

```python
# Upload from an open file handle...
with open("photo.jpg", "rb") as f:
    file = client.files.upload(f, filename="photo.jpg", conversation_id="conv_123")

# ...or straight from a path
file = client.files.upload("report.pdf")

# Signed download URL (1h TTL)
info = client.files.get_download_url(file.id)
print(info.url)

# List files in a conversation and check your storage quota
files = client.files.list("conv_123", type="image")
quota = client.files.get_quota()

# Base64 upload is also available
file = client.files.upload_base64(
    filename="note.txt", content_base64="aGVsbG8=", content_type="text/plain"
)
```

## Idempotency

There is nothing to configure. Every mutating request (`POST`, `PUT`, `PATCH`,
`DELETE`) automatically carries a unique `Idempotency-Key`, generated **once**
per logical call and reused across the SDK's automatic retries. If a write
succeeds server-side but the response is lost, the retry is de-duplicated
instead of creating a duplicate. `GET` requests are never keyed.

```python
# Safe to retry — the server replays the first result rather than re-executing.
memory = client.memories.create(content="Created exactly once, even if retried")
```

A caller-supplied `Idempotency-Key` header (for example, set via a request
interceptor) is always preserved so you can correlate a logical operation
across processes.

## Webhooks

### Managing webhooks

```python
from trix import WebhookEvent

webhook = client.webhooks.create(
    name="Memory Updates",
    url="https://example.com/webhook",
    events=[WebhookEvent.MEMORY_CREATED, WebhookEvent.MEMORY_UPDATED, WebhookEvent.MEMORY_DELETED],
    headers={"X-Custom-Header": "value"},
)

webhooks = client.webhooks.list()
webhook = client.webhooks.update("webhook_123", active=False)
result = client.webhooks.test("webhook_123")
deliveries = client.webhooks.get_deliveries("webhook_123", limit=50)
delivery = client.webhooks.retry_delivery("webhook_123", "delivery_456")
client.webhooks.delete("webhook_123")
```

### Verifying inbound webhooks

Trix signs every delivery with **HMAC-SHA256** over `"{timestamp}.{raw_body}"`
and sends it in the `X-Webhook-Signature: t=<unix_seconds>,v1=<hex>` header.
Verify it before trusting a payload. Verification is a **local CPU operation**
(no network call), so these methods are synchronous on both `Trix` and
`AsyncTrix` — no `await`.

```python
from trix import Trix, WebhookVerificationError

client = Trix(api_key="your_api_key")
SIGNING_SECRET = "whsec_..."  # the endpoint's signing secret

# Inside your HTTP handler. Pass the RAW request body exactly as received —
# never re-serialized JSON, since any whitespace/key-order change breaks the HMAC.
raw_body = request.get_data()                        # bytes
signature = request.headers["X-Webhook-Signature"]   # "t=<unix>,v1=<hex>"

# Option 1 — boolean check. Fails closed: returns False (never raises) on a
# missing/malformed header, wrong secret, tampered body, or expired timestamp.
if not client.webhooks.verify_signature(raw_body, signature, SIGNING_SECRET):
    abort(400, "invalid signature")

# Option 2 — verify and JSON-decode in one step. Raises WebhookVerificationError
# on failure and returns the parsed event dict on success.
try:
    event = client.webhooks.unwrap(raw_body, signature, SIGNING_SECRET)
except WebhookVerificationError:
    abort(400, "invalid signature")

print(event["event"])  # e.g. "memory.created"
```

Details:

- **Constant-time** comparison via `hmac.compare_digest` (no timing side channel).
- **Replay protection**: deliveries whose timestamp is more than
  `tolerance_seconds` (default **300**) from now are rejected. Override with
  `verify_signature(..., tolerance_seconds=600)`.
- **Fails closed**: `verify_signature` returns `False` on any problem;
  `unwrap` raises `WebhookVerificationError`.
- Both methods accept the raw body as `str` or `bytes`.

## Error Handling

The SDK raises a typed exception for every failure. Catching `TrixError`
catches them all.

```python
from trix import (
    Trix,
    TrixError,
    AuthenticationError,
    NotFoundError,
    RateLimitError,
    ValidationError,
)

client = Trix(api_key="your_api_key")

try:
    memory = client.memories.get("invalid_id")
except NotFoundError as e:
    print(f"Memory not found: {e}")
except AuthenticationError as e:
    print(f"Authentication failed: {e}")
except RateLimitError as e:
    print(f"Rate limited. Retry after {e.retry_after} seconds")
except ValidationError as e:
    print(f"Validation error: {e}")
except TrixError as e:
    print(f"API error: {e}")
```

### Exception hierarchy

All exceptions derive from `TrixError`:

- `TrixError` — base class for every SDK error
  - `AuthenticationError` — 401 authentication failures
  - `PermissionError` — 403 permission denied
  - `NotFoundError` — 404 resource not found
  - `ConflictError` — 409 conflict
  - `ValidationError` — 422 validation errors
  - `RateLimitError` — 429 rate limit exceeded (exposes `retry_after`)
  - `ServerError` — 5xx server errors
  - `APIError` — other non-2xx responses
  - `ConnectionError` — network connection errors
  - `TimeoutError` — request timeouts
  - `APIVersionMismatchError` — SDK/API version incompatibility
  - `WebhookVerificationError` — raised by `webhooks.unwrap` on an invalid signature

## Automatic Retries

Transient failures (429 and 5xx) are retried automatically with exponential
backoff and jitter, honoring the `Retry-After` header.

```python
from trix import Trix
from trix.utils import RetryConfig

retry_config = RetryConfig(
    max_retries=5,
    initial_delay=2.0,
    max_delay=120.0,
    exponential_base=2.0,
    jitter=True,
)

client = Trix(api_key="your_api_key", retry_config=retry_config)
```

By default, `RateLimitError` and `ServerError` are retryable. Combined with the
automatic idempotency keys above, retried writes are safe.

## Testing

The SDK ships `MockTrix` and `MockAsyncTrix` — drop-in mock clients that record
calls and return configured responses, with no network access.

```python
from trix.testing import MockTrix, create_mock_memory


def test_my_service():
    client = MockTrix()

    # Configure the response the mock should return
    client.memories.mock_create(create_mock_memory(content="Test"))

    memory = client.memories.create(content="Test")
    assert memory.content == "Test"

    # Calls are recorded for assertions
    assert len(client.memories.create_calls) == 1
```

Use `MockAsyncTrix` for async code. Factory helpers —
`create_mock_memory`, `create_mock_cluster`, `create_mock_entity`,
`create_mock_fact`, `create_mock_relationship` — build valid typed objects for
your assertions.

## Type Safety

All request and response objects are fully typed with Pydantic models, and the
package ships a `py.typed` marker so type checkers (mypy, Pyright) see the types.

```python
from trix import MemoryCreate, MemoryType

memory_data = MemoryCreate(
    content="Type-safe memory",
    type=MemoryType.TEXT,
    tags=["typed"],
    metadata={"key": "value"},
)
memory = client.memories.create(**memory_data.model_dump())

print(memory.id)          # str
print(memory.created_at)  # datetime
print(memory.tags)        # List[str]
```

## Requirements

- Python 3.9+
- httpx >= 0.25.0
- pydantic >= 2.0.0
- typing-extensions >= 4.5.0

## Development

```bash
# Clone and install with dev extras
git clone https://github.com/trixdb/trix-sdk-python.git
cd trix-sdk-python
python -m venv venv
source venv/bin/activate      # Windows: venv\Scripts\activate
pip install -e ".[dev]"

# Tests
pytest
pytest --cov=trix --cov-report=html

# Lint, format, type-check
ruff check .
black --check .
mypy src/
```

## Contributing

Contributions are welcome! Please open an issue or pull request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## Related SDKs

Trix maintains client libraries for several ecosystems — all track the same API:

| Language | Package | Repository |
|----------|---------|------------|
| TypeScript / JavaScript | npm `@trixdb/client` | [trix-sdk-typescript](https://github.com/trixdb/trix-sdk-typescript) |
| Go (streaming-focused client) | `github.com/trixdb/trix-sdk-go` | [trix-sdk-go](https://github.com/trixdb/trix-sdk-go) |
| C# / .NET | NuGet `Trix.Client` | [trix-sdk-csharp](https://github.com/trixdb/trix-sdk-csharp) |

## License

This project is licensed under the Apache License 2.0 - see the [LICENSE](LICENSE) file for details.

## Support

- Documentation: [https://docs.trixdb.com](https://docs.trixdb.com)
- Issues: [https://github.com/trixdb/trix-sdk-python/issues](https://github.com/trixdb/trix-sdk-python/issues)
- Email: support@trixdb.com
