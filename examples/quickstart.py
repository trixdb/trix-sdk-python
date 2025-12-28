#!/usr/bin/env python3
"""
Trix Python SDK Quick Start

This script demonstrates the most common operations with Trix.
Replace 'your_api_key' with your actual API key from https://trixdb.com
"""

from trix import Trix, MemoryType, RelationshipType, SearchMode


def main():
    """Run quick start examples."""
    # Initialize the client
    print("=" * 60)
    print("Trix Python SDK - Quick Start")
    print("=" * 60)

    # Replace with your actual API key
    API_KEY = "your_api_key"

    # You can also use environment variable:
    # import os
    # API_KEY = os.getenv("TRIX_API_KEY")

    client = Trix(api_key=API_KEY)

    try:
        # 1. Create memories
        print("\n1. Creating memories...")
        memories = []

        memory1 = client.memories.create(
            content="The Python programming language was created by Guido van Rossum",
            tags=["python", "history"],
            metadata={"category": "programming", "year": "1991"},
        )
        memories.append(memory1)
        print(f"   ✓ Created memory 1: {memory1.id}")

        memory2 = client.memories.create(
            content="Python emphasizes code readability with significant whitespace",
            tags=["python", "syntax"],
        )
        memories.append(memory2)
        print(f"   ✓ Created memory 2: {memory2.id}")

        memory3 = client.memories.create(
            content="Python is widely used in data science and machine learning",
            tags=["python", "data-science", "ml"],
        )
        memories.append(memory3)
        print(f"   ✓ Created memory 3: {memory3.id}")

        # 2. Create relationships
        print("\n2. Creating relationships...")
        rel = client.relationships.create(
            source_id=memory1.id,
            target_id=memory2.id,
            relationship_type=RelationshipType.RELATED_TO,
            description="Both describe Python characteristics",
        )
        print(f"   ✓ Created relationship: {rel.id}")

        # 3. Search memories
        print("\n3. Searching memories...")
        results = client.memories.list(q="Python", mode=SearchMode.HYBRID, limit=5)
        print(f"   ✓ Found {len(results.data)} memories matching 'Python'")
        for i, mem in enumerate(results.data[:3], 1):
            print(f"      {i}. {mem.content[:60]}...")

        # 4. Create a cluster
        print("\n4. Creating a cluster...")
        cluster = client.clusters.create(
            name="Python Programming",
            description="Memories about Python programming language",
            color="#3776AB",  # Python's official color
        )
        print(f"   ✓ Created cluster: {cluster.id}")

        # 5. Add memories to cluster
        print("\n5. Adding memories to cluster...")
        for memory in memories:
            client.clusters.add_memory(cluster.id, memory.id, confidence=0.9)
        print(f"   ✓ Added {len(memories)} memories to cluster")

        # 6. Create a space
        print("\n6. Creating a space...")
        space = client.spaces.create(
            name="Programming Knowledge", description="All programming-related memories"
        )
        print(f"   ✓ Created space: {space.id}")

        # 7. Find similar memories
        print("\n7. Finding similar memories...")
        similar = client.search.similar(memory1.id, limit=3, threshold=0.5)
        print(f"   ✓ Found {len(similar.data)} similar memories")
        for i, result in enumerate(similar.data, 1):
            print(f"      {i}. (score: {result.score:.2f}) {result.memory.content[:50]}...")

        # 8. Traverse the graph
        print("\n8. Traversing the memory graph...")
        from trix import Direction

        graph = client.graph.traverse(start_ids=[memory1.id], depth=2, direction=Direction.BOTH)
        print(f"   ✓ Graph traversal found {graph.total_nodes} connected nodes")

        # 9. Get a memory
        print("\n9. Retrieving a specific memory...")
        retrieved = client.memories.get(memory1.id)
        print(f"   ✓ Retrieved: {retrieved.content[:60]}...")
        print(f"      Tags: {', '.join(retrieved.tags)}")
        print(f"      Created: {retrieved.created_at}")

        # 10. Update a memory
        print("\n10. Updating a memory...")
        updated = client.memories.update(memory1.id, tags=["python", "history", "updated"])
        print(f"   ✓ Updated tags: {', '.join(updated.tags)}")

        # Success!
        print("\n" + "=" * 60)
        print("✓ Quick start completed successfully!")
        print("=" * 60)
        print("\nNext steps:")
        print("1. Check out examples/basic_usage.py for more examples")
        print("2. Read the full documentation in README.md")
        print("3. Explore the API at https://docs.trixdb.com")
        print("\nCreated resources (you may want to clean these up):")
        print(f"  - {len(memories)} memories")
        print(f"  - 1 cluster: {cluster.id}")
        print(f"  - 1 space: {space.id}")

    except Exception as e:
        print(f"\n✗ Error: {e}")
        print("\nTroubleshooting:")
        print("1. Make sure you've set your API key correctly")
        print("2. Check your internet connection")
        print("3. Verify your API key is valid at https://trixdb.com")
        import traceback

        traceback.print_exc()

    finally:
        # Always close the client
        client.close()
        print("\n✓ Client closed")


if __name__ == "__main__":
    main()
