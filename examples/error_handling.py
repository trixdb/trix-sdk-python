"""Error handling examples for Trix SDK."""

import time
from trix import (
    Trix,
    TrixError,
    AuthenticationError,
    NotFoundError,
    ValidationError,
    RateLimitError,
    ServerError,
)


def main():
    """Demonstrate error handling."""
    client = Trix(api_key="your_api_key")

    # Example 1: Handle not found errors
    print("Example 1: Handling NotFoundError")
    try:
        memory = client.memories.get("invalid_memory_id")
    except NotFoundError as e:
        print(f"  ✗ Memory not found: {e.message}")
        print(f"    Status code: {e.status_code}")

    # Example 2: Handle validation errors
    print("\nExample 2: Handling ValidationError")
    try:
        # This should fail validation
        memory = client.memories.create(content="")  # Empty content
    except ValidationError as e:
        print(f"  ✗ Validation failed: {e.message}")
        if e.response:
            print(f"    Details: {e.response}")

    # Example 3: Handle authentication errors
    print("\nExample 3: Handling AuthenticationError")
    try:
        invalid_client = Trix(api_key="invalid_key")
        memory = invalid_client.memories.list()
    except AuthenticationError as e:
        print(f"  ✗ Authentication failed: {e.message}")
        print(f"    Status code: {e.status_code}")

    # Example 4: Handle rate limiting with retry
    print("\nExample 4: Handling RateLimitError")
    try:
        # Simulate rapid requests that might trigger rate limiting
        for i in range(100):
            client.memories.list(limit=1)
    except RateLimitError as e:
        print(f"  ✗ Rate limited: {e.message}")
        if e.retry_after:
            print(f"    Retry after: {e.retry_after} seconds")
            print("    Waiting before retry...")
            time.sleep(e.retry_after)
            print("    ✓ Retry completed")

    # Example 5: Catch all Trix errors
    print("\nExample 5: Catching all Trix errors")
    try:
        # Some operation that might fail
        memory = client.memories.get("some_id")
    except TrixError as e:
        print(f"  ✗ Trix error: {e.message}")
        print(f"    Error type: {type(e).__name__}")
        if e.status_code:
            print(f"    Status code: {e.status_code}")

    # Example 6: Graceful error handling with fallback
    print("\nExample 6: Graceful error handling with fallback")

    def get_memory_with_fallback(memory_id, fallback_content="Default content"):
        """Get memory with fallback on error."""
        try:
            return client.memories.get(memory_id)
        except NotFoundError:
            print(f"  ! Memory {memory_id} not found, creating new one")
            return client.memories.create(content=fallback_content)
        except TrixError as e:
            print(f"  ! Error retrieving memory: {e.message}")
            return None

    memory = get_memory_with_fallback("maybe_invalid_id", "Fallback content")
    if memory:
        print(f"  ✓ Got or created memory: {memory.id}")

    # Example 7: Custom retry logic
    print("\nExample 7: Custom retry logic for transient errors")

    def retry_on_server_error(func, max_retries=3, delay=1.0):
        """Retry function on server errors."""
        for attempt in range(max_retries):
            try:
                return func()
            except ServerError:
                if attempt < max_retries - 1:
                    print(f"  ! Server error on attempt {attempt + 1}, retrying...")
                    time.sleep(delay * (2**attempt))  # Exponential backoff
                else:
                    print(f"  ✗ Failed after {max_retries} attempts")
                    raise

    try:
        result = retry_on_server_error(lambda: client.memories.list(limit=10))
        print(f"  ✓ Successfully retrieved {len(result.data)} memories")
    except ServerError as e:
        print(f"  ✗ Server error persisted: {e.message}")

    # Example 8: Context manager ensures cleanup even on errors
    print("\nExample 8: Context manager with error handling")
    try:
        with Trix(api_key="your_api_key") as client:
            # Do some work
            memory = client.memories.create(content="Test")
            # Simulate an error
            raise ValueError("Simulated error")
    except ValueError as e:
        print(f"  ! Error occurred: {e}")
        print("  ✓ Client was still properly closed")

    print("\n✓ Error handling examples completed!")

    client.close()


if __name__ == "__main__":
    main()
