from typing import TypeAlias, Any, Self, ParamSpec, TypeVar, Generic, cast
from ..vocabulary import Vocabulary
from ..theory import Theory
from ..structure import Structure
from ..knowledge_base import _KnowledgeBase
from collections.abc import Callable, Iterator
import ast
import types
from enum import StrEnum
from dataclasses import dataclass, field


class ProcedureLang(StrEnum):
    PYTHON = "Python"


P = ParamSpec('P')
T = TypeVar('T')

@dataclass(frozen=True)
class Procedure(Generic[P, T]):
    lang: ProcedureLang
    name: str
    args: list[str]
    content: str
    knowledge_base: "KnowledgeBase"
    _func: Callable[P, T] = field(init=False, hash=False, repr=False, compare=False)

    def __call__(self, *args: Any, **kwargs: Any) -> Any:
        "@public"
        return self.func(*args, **kwargs)

    @property
    def func(self) -> Callable[P, T]:
        """
        Returns this procedure as a Python function
        """
        if hasattr(self, "_func"):
            return self._func
        object.__setattr__(self, "_func", self.compile()) 
        return self._func

    def compile(self) -> Callable[P, T]:
        if self.lang != ProcedureLang.PYTHON:
            raise RuntimeError(f"unable to compile procedure for language '{self.lang}'")
        to_compile =(
            f"def {self.name}({', '.join(self.args)}):\n"\
            f"{self.content}"
        )
        ast_of_to_compile = ast.parse(to_compile)
        if len(ast_of_to_compile.body) != 1:
            raise RuntimeError(f"Procedure '{self.name}' has escaped content, check if indentation is consistent")
        # TODO: fix source code name once sli has source code metadata and this is available in
        # python
        compiled = self.knowledge_base.compile_func(ast_of_to_compile, "<unknown>", "exec")
        globals = self.knowledge_base.globals
        exec(compiled, globals, None)
        func = cast(Callable[P, T], globals[self.name])
        return func


LogicalBlock: TypeAlias = Vocabulary | Theory | Structure

Block: TypeAlias = LogicalBlock | Procedure[..., Any]

class KnowledgeBase:
    """
    A mapping of names to FO(·) blocks and environment for procedures.

    The compile function and globals used for procedures can be changed using the 
    `compile_func` property and the `global` property respectively.
    """
    _kb: _KnowledgeBase
    _proc_cache: dict[str, Procedure[..., Any]]
    compile_func: Callable[[str | ast.Module, str, str], types.CodeType]
    "function to compile procedures with"
    _globals: "_LazyDict"

    def __new__(cls) -> Self:
        raise TypeError(f"cannot create '{cls.__module__}.{cls.__name__}' instances")
    
    @classmethod
    def _construct(
        cls,
        kb: _KnowledgeBase,
        globals: dict[str, Any],
        compile_func: Callable[[str | ast.Module, str, str], types.CodeType]
    ) -> Self:
        this = super(KnowledgeBase, cls).__new__(cls)
        this._kb = kb
        this._proc_cache = dict()
        this.globals = globals
        this.compile_func = compile_func
        return this

    @classmethod
    def from_str(cls, knowledge_base: str) -> Self:
        return cls._construct(
            _KnowledgeBase.from_str(knowledge_base),
            cls.default_globals(),
            compile
        )

    @property
    def globals(self) -> dict[str, Any]:
        """
        Dictionary that procedure use as globals().

        See documentation of exec to see how this dictionary behaves.
        """
        return self._globals

    @globals.setter
    def globals(self, value: dict[str, Any]) -> None:
        self._globals = _LazyDict(value, kb=self)


    @classmethod
    def add_default_imports(cls, globals: dict[str, Any]) -> None:
        import sli_lib.fodot as fodot
        import sli_lib.methods as methods
        for thing in fodot.__all__:
            globals[thing] = getattr(fodot, thing)
        for thing in methods.__all__:
            globals[thing] = getattr(methods, thing)

    @classmethod
    def default_globals(cls) -> dict[str, Any]:
        globals: dict[str, Any] = {}
        cls.add_default_imports(globals)
        return globals

    def __getitem__(self, name: str) -> Block:
        "@public"
        if (proc := self._proc_cache.get(name)) is not None:
            return proc
        value = self._kb[name]
        if isinstance(value, Procedure):
            # patch knowledge_base
            object.__setattr__(value, "knowledge_base", self)
            self._proc_cache[name] = value
        return value

    def __repr__(self) -> str:
        return f"KnowledgeBase.from_str(\"\"\"\n{str(self._kb)}\"\"\")"

    def __len__(self) -> int:
        return len(self._kb)

    def __iter__(self) -> Iterator[tuple[str, Block]]:
        "@public"
        return iter(self._kb)

    def __str__(self) -> str:
        return str(self._kb)


class _LazyDict(dict[Any, Any]):
    _kb: KnowledgeBase
    def __init__(self, mapping: dict[Any, Any], /, **kwargs: Any) -> None:
        self._kb = kwargs['kb']
        del kwargs['kb']
        super().__init__(mapping, **kwargs)
    
    def knowledge_base(self) -> KnowledgeBase:
        return self._kb

    def __getitem__(self, key: Any) -> Any:
        try:
            return super().__getitem__(key)
        except KeyError:
            pass
        value = self._kb[key]
        self[key] = value
        return value


__all__ = [
    "ProcedureLang",
    "Procedure",
    "KnowledgeBase",
    "LogicalBlock",
    "Block",
]
