"""Async usage examples for Trix SDK."""

import asyncio
from trix import AsyncTrix, MemoryType, RelationshipType


async def main():
    """Main async example function."""
    # Use async context manager for automatic cleanup
    async with AsyncTrix(api_key="your_api_key") as client:
        # Create multiple memories concurrently
        print("Creating memories concurrently...")
        memories = await asyncio.gather(
            client.memories.create(
                content="Async/await makes concurrent programming easier",
                tags=["python", "async"],
            ),
            client.memories.create(
                content="asyncio is Python's built-in async framework",
                tags=["python", "async", "asyncio"],
            ),
            client.memories.create(
                content="Context managers help manage resources properly",
                tags=["python", "best-practices"],
            ),
        )
        print(f"Created {len(memories)} memories")

        # Create relationships between memories
        print("\nCreating relationships...")
        relationships = await asyncio.gather(
            client.relationships.create(
                source_id=memories[0].id,
                target_id=memories[1].id,
                relationship_type=RelationshipType.RELATED_TO,
            ),
            client.relationships.create(
                source_id=memories[1].id,
                target_id=memories[2].id,
                relationship_type=RelationshipType.SUPPORTS,
            ),
        )
        print(f"Created {len(relationships)} relationships")

        # Search for memories
        print("\nSearching for async-related memories...")
        results = await client.memories.list(q="async", limit=10)
        print(f"Found {len(results.data)} memories")

        # Create a cluster
        print("\nCreating a cluster...")
        cluster = await client.clusters.create(
            name="Python Async",
            description="Memories about Python async programming",
        )

        # Add memories to cluster concurrently
        print("\nAdding memories to cluster...")
        await asyncio.gather(
            *[
                client.clusters.add_memory(cluster.id, memory.id, confidence=0.9)
                for memory in memories
            ]
        )
        print("All memories added to cluster")

        # Traverse graph
        print("\nTraversing memory graph...")
        from trix import Direction

        graph = await client.graph.traverse(
            start_ids=[memories[0].id], depth=2, direction=Direction.BOTH
        )
        print(f"Graph contains {graph.total_nodes} nodes")

        # Find context for a query
        print("\nGetting context for query...")
        context = await client.graph.get_context(
            query="Python async programming patterns", depth=2, semantic_limit=5
        )
        print(f"Found {len(context.memories)} relevant memories")

        # Use async iteration
        print("\nIterating through memories asynchronously...")
        count = 0
        async for memory in await client.memories.iter(page_size=10):
            print(f"  - {memory.content[:40]}...")
            count += 1
            if count >= 5:
                break

        # Create agent session
        print("\nCreating agent session...")
        session = await client.agent.create_session(
            session_id="async_demo_session", metadata={"demo": True}
        )

        # Add session memories
        print("\nAdding memories to session...")
        await asyncio.gather(
            client.agent.add_session_memory(
                session_id=session.session_id,
                content="User asked about async programming",
                role="user",
                importance=0.8,
            ),
            client.agent.add_session_memory(
                session_id=session.session_id,
                content="Explained async/await syntax",
                role="assistant",
                importance=0.7,
            ),
        )

        # Get session context
        print("\nGetting session context...")
        session_context = await client.agent.get_context(
            query="What did we discuss?", session_id=session.session_id
        )
        print(f"Session has {len(session_context.session_memories)} memories")

        # End session
        print("\nEnding session...")
        await client.agent.end_session(
            session_id=session.session_id,
            summary="Discussed Python async programming basics",
        )

        # Check job stats
        print("\nChecking job statistics...")
        stats = await client.jobs.get_stats()
        for queue_stats in stats:
            print(
                f"  Queue '{queue_stats.queue}': "
                f"{queue_stats.waiting} waiting, {queue_stats.active} active"
            )

        print("\n✓ All async operations completed successfully!")


if __name__ == "__main__":
    # Run the async main function
    asyncio.run(main())
