"""Memories resource module.

Provides backward-compatible exports for the refactored memories resource.
"""

from .core import AsyncMemoriesResource, MemoriesResource

__all__ = [
    "MemoriesResource",
    "AsyncMemoriesResource",
]
