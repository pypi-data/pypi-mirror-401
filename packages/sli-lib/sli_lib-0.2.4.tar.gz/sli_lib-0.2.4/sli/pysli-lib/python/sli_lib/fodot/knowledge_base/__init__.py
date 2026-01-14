from ..._fodot.knowledge_base import *
from ..._fodot import knowledge_base

from ._pure import *
from . import _pure
from ..._all_utils import filter__all__, merge__all__, rename_module

__all__ = merge__all__(
    filter__all__(knowledge_base.__all__),
    _pure.__all__,
)

# patch __module__ of everything to this module
rename_module(__all__, locals(), __name__)
