"""lfem - Finite Element Mesh library."""

from lfem.mesh import ELEMENT_TYPES, Mesh

__all__ = ["Mesh", "ELEMENT_TYPES"]
__version__ = "0.1.0"


def hello() -> str:
    """Return greeting message."""
    return "Hello from lfem!"
