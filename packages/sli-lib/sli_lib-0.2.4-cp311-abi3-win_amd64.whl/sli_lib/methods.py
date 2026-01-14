from .fodot.knowledge_base import LogicalBlock
from .fodot.structure import GlobModel, Model, Structure
from .fodot import Inferenceable
from .solver import Z3Solver, SatResult
from sys import stdout
from typing import overload, Literal, IO, Any, TypeVar, Generic, Self
from collections.abc import Iterator


def model_check(*blocks: LogicalBlock) -> SatResult:
    """
    Returns the satisfiability of the given blocks.

    Merges all given blocks into an `sli_lib.fodot.knowledge_base.Inferenceable` using
    `sli_lib.fodot.knowledge_base.Inferenceable.from_blocks`.
    """
    return Z3Solver(Inferenceable.from_blocks(*blocks)).check()


@overload
def model_expand(
    *blocks: LogicalBlock,
    max: int | None = 10,
    complete: Literal[True] = ...,
) -> Iterator[Model]: ...
@overload
def model_expand(
    *blocks: LogicalBlock,
    max: int | None = 10,
    complete: Literal[False],
) -> Iterator[GlobModel]: ...
def model_expand(
    *blocks: LogicalBlock,
    max: int | None = 10,
    complete: bool = False,
) -> Iterator[Model | GlobModel]:
    """
    Returns the model expansion of the given blocks as an iterator.

    Merges all given blocks into an `sli_lib.fodot.knowledge_base.Inferenceable` using
    `sli_lib.fodot.knowledge_base.Inferenceable.from_blocks`,

    `max`: maximum amount of models that the returned iterator will yield, only positive integers and None are allowed.

    `complete`: if `complete` is true then the iterator will return `sli_lib.fodot.structure.Model` instead of `sli_lib.fodot.structure.GlobModel`.
    """
    solver = Z3Solver(Inferenceable.from_blocks(*blocks))
    if complete:
        return _ModelExpandIter(
            solver.iter_models(),
            max=max,
        )
    else:
        return _ModelExpandIter(
            solver.iter_glob_models(),
            max=max,
        )


T = TypeVar("T", Model, GlobModel)

class _ModelExpandIter(Generic[T]):
    _inner_iter: Iterator[T]
    _max: int | None
    _cur: int = 0
    def __init__(
        self,
        inner_iter: Iterator[T],
        max: int | None,
    ) -> None:
        if max is not None and max <= 0:
            raise ValueError("max has to be either None or larger than 0")
        self._inner_iter = inner_iter
        self._cur = 0
        self._max = max

    def __next__(self) -> T:
        if self._max is None:
            return next(self._inner_iter)
        elif self._max is not None and self._max > self._cur:
            self._cur += 1
            return next(self._inner_iter)
        else:
            raise StopIteration()

    def __iter__(self) -> Self:
        return self


def model_propagate(*blocks: LogicalBlock) -> Structure | None:
    """
    Returns all **new** assignments that are true in any model as a `sli_lib.fodot.structure.Structure`, or `None` if the given blocks are inconsistent.

    Merges all given blocks into an `sli_lib.fodot.knowledge_base.Inferenceable` using
    `sli_lib.fodot.knowledge_base.Inferenceable.from_blocks`.
    """
    return Z3Solver(Inferenceable.from_blocks(*blocks)).propagate_diff()


def pretty_print(object: Any, /, *, file: IO[str] | None=None, flush: bool=False) -> None:
    """
    Prints a single python object, has special logic for pretty printing some `sli_lib` classes.
    """
    ffile: IO[str] = file if file is not None else stdout
    if isinstance(object, _ModelExpandIter):
        mx_iter = object
        model_count = 1
        template = "=== Model {} ==="
        for rest in mx_iter:
            print(template.format(model_count), file=ffile)
            print(rest, file=ffile)
            model_count += 1
        if model_count == 1:
            print("Theory is unsatisfiable.", file=ffile)
        elif mx_iter._max is None or mx_iter._cur < mx_iter._max:
            print("No more models.", file=ffile)
        else:
            print("More models may be available.", file=ffile)
    elif isinstance(object, SatResult):
        print(object.value, file=ffile)
    elif isinstance(object, Structure):
        if object.completed_domain():
            print(object._str_pfuncs(), file=ffile) # type: ignore[attr-defined]
        else:
            print(object, file=ffile)
    else:
        print(object, file=ffile)
    if flush:
        ffile.flush()

__all__ = [
    "model_expand",
    "model_propagate",
    "model_check",
    "pretty_print",
]
