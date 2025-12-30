"""Basic usage examples for Trix SDK."""

from trix import Trix, MemoryType, RelationshipType, SearchMode

# Initialize client
client = Trix(api_key="your_api_key")

try:
    # Create a memory
    print("Creating a memory...")
    memory = client.memories.create(
        content="Python is a high-level programming language",
        type=MemoryType.TEXT,
        tags=["programming", "python"],
        metadata={"category": "education"},
        priority=5,
    )
    print(f"Created memory: {memory.id}")

    # Create another related memory
    memory2 = client.memories.create(
        content="Python was created by Guido van Rossum",
        tags=["python", "history"],
    )
    print(f"Created memory: {memory2.id}")

    # Create a relationship
    print("\nCreating a relationship...")
    relationship = client.relationships.create(
        source_id=memory.id,
        target_id=memory2.id,
        relationship_type=RelationshipType.RELATED_TO,
        description="Both memories are about Python",
        weight=1.5,
    )
    print(f"Created relationship: {relationship.id}")

    # Search for memories
    print("\nSearching for memories...")
    results = client.memories.list(q="Python", mode=SearchMode.HYBRID, limit=10)
    print(f"Found {len(results.data)} memories:")
    for result in results.data:
        print(f"  - {result.content[:50]}...")

    # Create a cluster
    print("\nCreating a cluster...")
    cluster = client.clusters.create(
        name="Python Knowledge",
        description="All memories about Python programming",
        color="#3776AB",  # Python blue
    )
    print(f"Created cluster: {cluster.id}")

    # Add memories to cluster
    print("\nAdding memories to cluster...")
    client.clusters.add_memory(cluster.id, memory.id, confidence=0.95)
    client.clusters.add_memory(cluster.id, memory2.id, confidence=0.90)
    print("Memories added to cluster")

    # Traverse the graph
    print("\nTraversing the graph...")
    from trix import Direction

    graph = client.graph.traverse(start_ids=[memory.id], depth=2, direction=Direction.BOTH)
    print(f"Found {graph.total_nodes} nodes in graph traversal")

    # Find similar memories
    print("\nFinding similar memories...")
    similar = client.search.similar(memory.id, limit=5, threshold=0.5)
    print(f"Found {len(similar.data)} similar memories")

    # Create a space
    print("\nCreating a space...")
    space = client.spaces.create(
        name="Programming Knowledge", description="All programming-related memories"
    )
    print(f"Created space: {space.id}")

    # Update memory with space
    print("\nUpdating memory...")
    updated_memory = client.memories.update(memory.id, tags=["programming", "python", "updated"])
    print(f"Updated memory tags: {updated_memory.tags}")

    # Create a highlight
    print("\nCreating a highlight...")
    highlight = client.highlights.create(
        memory_id=memory.id,
        text="high-level programming language",
        note="Key characteristic of Python",
        importance=8,
        color="#FFFF00",
    )
    print(f"Created highlight: {highlight.id}")

    # Submit feedback
    print("\nSubmitting feedback...")
    from trix import FeedbackResult

    feedback = client.feedback.submit(
        query_context="Python programming language",
        results=[
            FeedbackResult(memory_id=memory.id, score=0.95, rank=1),
            FeedbackResult(memory_id=memory2.id, score=0.85, rank=2),
        ],
        create_relationships=True,
    )
    print(f"Created {feedback.relationships_created} relationships from feedback")

    # List all spaces
    print("\nListing all spaces...")
    spaces = client.spaces.list()
    print(f"Total spaces: {len(spaces.data)}")

    # Iterate through memories
    print("\nIterating through memories (first 5)...")
    count = 0
    for mem in client.memories.iter(page_size=10):
        print(f"  - {mem.content[:40]}...")
        count += 1
        if count >= 5:
            break

    print("\n✓ All operations completed successfully!")

except Exception as e:
    print(f"Error: {e}")

finally:
    # Clean up
    client.close()
