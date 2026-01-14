"""
Module with a set datastructure over a given FO(·) domain.
"""

from ...._fodot.collections.set import *
from ...._fodot.collections import set
from ...._all_utils import filter__all__, rename_module

__all__ = filter__all__(set.__all__)

# patch __module__ of everything to this module
rename_module(__all__, locals(), __name__)

