"""Import smoke tests.

Guard against modules that reference a symbol they never imported (e.g. a
Pydantic ``Field`` used without ``from pydantic import Field``). Such a bug
raises ``NameError`` at import time and makes the whole package unusable, yet
passes every mock-based unit test that never imports the offending module.

Regression guard for #2 (``github_types.py`` used ``Field`` without importing
it, breaking ``from trix import Trix``).
"""

import importlib
import pkgutil

import trix.resources


def test_top_level_import() -> None:
    """The public entrypoint must import without error."""
    from trix import AsyncTrix, Trix

    assert Trix is not None
    assert AsyncTrix is not None


def test_github_types_imports() -> None:
    """github_types must import (regression: missing ``Field`` import, #2)."""
    module = importlib.import_module("trix.resources.github_types")

    assert module is not None


def _resource_module_names() -> list:
    """Every importable submodule under ``trix.resources``."""
    package = trix.resources
    return [name for _, name, _ in pkgutil.walk_packages(package.__path__, f"{package.__name__}.")]


def test_all_resource_modules_import() -> None:
    """Importing every resource module catches any missing-import NameError."""
    for name in _resource_module_names():
        importlib.import_module(name)
