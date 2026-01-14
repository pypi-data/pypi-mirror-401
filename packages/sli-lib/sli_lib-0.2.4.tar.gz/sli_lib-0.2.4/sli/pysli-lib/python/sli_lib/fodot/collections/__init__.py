"""
Efficient datastructures for FO(·) interpretations.
"""

from . import set as set

from .set import Set as Set

__re_exports__ = [
    "Set",
]

__all__ = [
    "set"
] + __re_exports__
