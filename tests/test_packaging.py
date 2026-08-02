"""Packaging invariants (GitHub issue #9).

The SDK version used to be duplicated across five places (pyproject.toml,
``trix.__version__``, package.json, .release-please-manifest.json, and the built
dist) and they disagreed. ``py.typed`` also lived only at the repo root and was
never packaged, so ``trix`` shipped without its PEP 561 marker.

The version is now single-sourced from the installed distribution metadata
(populated by setuptools from ``[project] version`` in pyproject.toml), and
``src/trix/py.typed`` is declared as package data so it lands in the wheel.
"""

import importlib.resources
from importlib.metadata import version

import trix


def test_version_is_single_sourced_from_distribution():
    """trix.__version__ must equal the installed distribution version."""
    assert trix.__version__ == version("trixdb")


def test_version_is_not_the_stale_placeholder():
    """Guard against __init__ pinning a hardcoded version that drifts from dist."""
    assert trix.__version__ != "0.1.1"
    assert trix.__version__[0].isdigit()  # a real release, not the uninstalled sentinel


def test_py_typed_marker_is_packaged():
    """The PEP 561 marker must ship inside the trix package."""
    marker = importlib.resources.files("trix") / "py.typed"
    assert marker.is_file()
