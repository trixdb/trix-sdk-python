"""
Example usage of the Trix Sessions API.

This example demonstrates how to use sessions for managing conversation
and project contexts with lifecycle management.
"""

from trix import Trix, SessionType, SessionStatus, RetentionPolicy


def main():
    # Initialize client
    client = Trix.from_env()

    # 1. Create a new project session
    print("Creating a new project session...")
    session = client.sessions.create(
        name="Q1 Planning",
        description="Sprint planning for Q1 2025",
        type=SessionType.PROJECT,
        tags=["planning", "q1"],
        retention_policy=RetentionPolicy.AUTO_DELETE,
        retention_days=90,
        metadata={"quarter": "Q1", "year": 2025},
    )
    print(f"Created session: {session.id} - {session.name}")
    print(f"Status: {session.status}, Type: {session.type}")

    # 2. List all active sessions
    print("\nListing active sessions...")
    active_sessions = client.sessions.get_active()
    print(f"Found {len(active_sessions.data)} active session(s)")
    for s in active_sessions.data:
        print(f"  - {s.name} ({s.type}): {s.message_count} messages")

    # 3. Update session
    print("\nUpdating session...")
    updated_session = client.sessions.update(
        session.id,
        tags=["planning", "q1", "in-progress"],
        metadata={"quarter": "Q1", "year": 2025, "progress": 0.3},
    )
    print(f"Updated tags: {updated_session.tags}")

    # 4. Get session details
    print("\nGetting session details...")
    session_details = client.sessions.get(session.id)
    print(f"Session: {session_details.name}")
    print(f"  Messages: {session_details.message_count}")
    print(f"  Memories: {session_details.memory_count}")
    print(f"  Last active: {session_details.last_active_at}")

    # 5. Pause session
    print("\nPausing session...")
    paused_session = client.sessions.pause(session.id)
    print(f"Session status: {paused_session.status}")
    print(f"Paused at: {paused_session.paused_at}")

    # 6. Resume session
    print("\nResuming session...")
    resumed_session = client.sessions.resume(session.id)
    print(f"Session status: {resumed_session.status}")

    # 7. Get session statistics
    print("\nGetting session statistics...")
    stats = client.sessions.get_stats()
    print(f"Total sessions: {stats.total}")
    print(f"Active: {stats.active}, Paused: {stats.paused}")
    print(f"Completed: {stats.completed}, Archived: {stats.archived}")
    print(f"By type: {stats.by_type}")
    print(f"Total messages: {stats.total_messages}")

    # 8. List sessions with filters
    print("\nListing project sessions...")
    project_sessions = client.sessions.list(
        type=SessionType.PROJECT,
        status=SessionStatus.ACTIVE,
        limit=10,
    )
    print(f"Found {len(project_sessions.data)} project session(s)")

    # 9. Complete session with summary
    print("\nCompleting session...")
    completed_session = client.sessions.complete(
        session.id,
        summary="Q1 planning completed. All goals defined and sprint backlog created.",
    )
    print(f"Session status: {completed_session.status}")
    print(f"Completed at: {completed_session.completed_at}")
    print(f"Summary: {completed_session.summary}")

    # 10. Get session memories
    print("\nGetting session memories...")
    memories = client.sessions.get_memories(session.id, limit=10)
    print(f"Session has {memories['total']} memories")

    # Cleanup
    print("\nCleaning up...")
    client.sessions.delete(session.id)
    print("Session deleted")

    client.close()
    print("\nExample completed!")


async def async_example():
    """Async example usage."""
    from trix import AsyncTrix

    async with AsyncTrix.from_env() as client:
        # Create session
        session = await client.sessions.create(
            name="Async Session",
            type=SessionType.CONVERSATION,
        )
        print(f"Created async session: {session.id}")

        # Get active sessions
        active = await client.sessions.get_active()
        print(f"Active sessions: {len(active.data)}")

        # Complete and delete
        await client.sessions.complete(session.id, summary="Done!")
        await client.sessions.delete(session.id)
        print("Async session cleaned up")


if __name__ == "__main__":
    # Run sync example
    main()

    # Uncomment to run async example
    # import asyncio
    # asyncio.run(async_example())
