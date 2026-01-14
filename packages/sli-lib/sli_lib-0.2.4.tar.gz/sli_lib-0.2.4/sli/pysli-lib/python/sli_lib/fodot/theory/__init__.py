from ..._fodot.theory import *
from ..._fodot import theory
from ..._all_utils import filter__all__, rename_module, merge__all__
from ..knowledge_base import Inferenceable as Inferenceable

__re_exports__ = [
    "Inferenceable"
]

__all__ = merge__all__(
    filter__all__(theory.__all__),
    __re_exports__
)

# patch __module__ of everything to this module
rename_module(set(__all__) - { "Inferenceable" }, locals(), __name__)
