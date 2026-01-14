"""
Module containing methods and data structures for representing FO(·).
"""

from . import theory as theory
from . import structure as structure
from . import vocabulary as vocabulary
from . import knowledge_base as knowledge_base
from . import collections as collections

from .vocabulary import Vocabulary as Vocabulary
from .structure import Structure as Structure
from .theory import Theory as Theory, Inferenceable as Inferenceable
from .knowledge_base import KnowledgeBase as KnowledgeBase

__re_exports__ = [
    "Vocabulary",
    "Structure",
    "Theory",
    "Inferenceable",
    "KnowledgeBase",
]

__all__ = [
    "collections",
    "theory",
    "structure",
    "vocabulary",
    "knowledge_base",
] + __re_exports__
