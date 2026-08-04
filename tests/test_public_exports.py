"""Regression tests for the public export surface of the ``trix`` package.

Guards against re-export drift: every type published by ``trix.types`` must be
importable straight from ``trix`` (``from trix import Task``), and the package
``__all__`` must be internally consistent. This previously regressed — a
hand-curated re-export list left 170+ public types importable from
``trix.types`` but not from the package root.
"""

import importlib

import trix
import trix.types


def test_every_public_type_is_importable_from_package_root() -> None:
    """Every name in ``trix.types.__all__`` is reachable as ``trix.<name>``."""
    missing = sorted(name for name in trix.types.__all__ if not hasattr(trix, name))
    assert missing == [], f"types published by trix.types but missing from trix: {missing}"


def test_public_types_are_in_package_all() -> None:
    """The type names are advertised in ``trix.__all__``, not just importable."""
    exported = set(trix.__all__)
    missing = sorted(name for name in trix.types.__all__ if name not in exported)
    assert missing == [], f"types missing from trix.__all__: {missing}"


def test_package_all_has_no_duplicates() -> None:
    all_names = trix.__all__
    dupes = sorted({n for n in all_names if all_names.count(n) > 1})
    assert dupes == [], f"duplicate names in trix.__all__: {dupes}"


def test_every_name_in_all_resolves() -> None:
    """Nothing in ``__all__`` is a dangling name that would break ``import *``."""
    unresolved = sorted(name for name in trix.__all__ if not hasattr(trix, name))
    assert unresolved == [], f"names in trix.__all__ that do not resolve: {unresolved}"


def test_core_types_import_by_name() -> None:
    """Spot-check high-value core types that regressed before."""
    from trix import (  # noqa: F401
        Bot,
        EnrichmentOperation,
        Entity,
        Fact,
        Goal,
        Invite,
        Note,
        Persona,
        PingResult,
        Resource,
        Skill,
        Task,
        Workflow,
    )


def test_clients_and_exceptions_not_shadowed_by_type_starexport() -> None:
    """The type star-export must not clobber the client / exception exports."""
    from trix import APIError, AsyncTrix, RateLimitError, RetryConfig, Trix, TrixError

    assert Trix.__name__ == "Trix"
    assert AsyncTrix.__name__ == "AsyncTrix"
    assert issubclass(RateLimitError, TrixError)
    assert issubclass(APIError, TrixError)
    assert RetryConfig().max_retries >= 0


def test_star_import_from_trix_exposes_types() -> None:
    """``from trix import *`` honours ``__all__`` and includes the types."""
    module = importlib.import_module("trix")
    namespace: dict = {}
    exec("from trix import *", namespace)  # noqa: S102 - controlled import in test
    for name in ("Task", "Bot", "PingResult", "Trix"):
        assert name in namespace, f"{name} not exposed by `from trix import *`"
        assert namespace[name] is getattr(module, name)
