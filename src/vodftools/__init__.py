#!/usr/bin/env python3

"""VODF tools."""

from .version import __version__

__all__ = ["__version__", "schema", "models", "vodf_version_id"]


def vodf_version_id():
    """Return VODF version id string, i.e. VODF-x.y.z."""
    return f"VODF-{__version__}"
