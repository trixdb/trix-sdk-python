"""
Re-exports of Trix API types for the public SDK interface.

This module is imported by ``trix/__init__.py`` to keep the main entry point
lean. Every type is originally defined in a ``trix.types`` submodule; here we
re-export the *entire* public surface that ``trix.types`` publishes (its
``__all__``) so any documented model is importable straight from the package
root — e.g. ``from trix import Task, Bot, PingResult``.

Previously this module hand-maintained a curated import list, which drifted out
of sync with ``trix.types`` and left 170+ public types (Task, Bot, Note, Goal,
Persona, Fact, Entity, Skill, Workflow, Invite, Resource, PingResult, …)
importable from ``trix.types`` but *not* from ``trix``. Sourcing the names
directly from ``trix.types.__all__`` keeps the two in lockstep automatically.
"""

from . import types as _types

# Deliberate star import: re-export the full public type surface that
# ``trix.types`` publishes (it defines ``__all__``), so the two stay in lockstep.
from .types import *

# Single source of truth: whatever ``trix.types`` publishes is what ``trix``
# re-exports at the top level, so ``trix.__all__`` stays complete without any
# manual curation drift.
TYPE_NAMES = list(_types.__all__)

__all__ = TYPE_NAMES
