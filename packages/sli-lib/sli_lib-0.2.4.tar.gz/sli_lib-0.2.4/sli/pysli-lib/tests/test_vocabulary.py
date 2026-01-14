from sli_lib.fodot.vocabulary import Vocabulary, BuiltinTypes
from sli_lib.fodot.structure import StrInterp
import pytest

def test_add_type():
    vocab = Vocabulary()
    vocab.add_type("T1")
    vocab.add_type("T2")
    T1 = vocab.parse_type("T1")
    vocab.add_voc_type_interp(T1, StrInterp(["a", "b", "c"]))
    with pytest.raises(ValueError):
        vocab.add_voc_type_interp("T2", StrInterp(["a", "b", "c"]))
    vocab2 = Vocabulary()
    vocab2.add_type("T2")
    T12 = vocab2.parse_type("T2")
    with pytest.raises(ValueError):
        vocab.add_voc_type_interp(T12, StrInterp(["d", "e", "f"]))
    vocab.add_voc_type_interp("T2", StrInterp(["d", "e", "f"]))

def test_add_pfunc():
    vocab = Vocabulary()
    vocab.add_type("T")
    vocab.add_pfunc("p", (), "Bool")
    with pytest.raises(TypeError):
        vocab.add_pfunc(2, (), "Bool") # type: ignore
    with pytest.raises(TypeError):
        vocab.add_pfunc(("ttt", 4), (), "Bool")  # type: ignore
    vocab.add_pfunc((f"p{i}" for i in range(5)), (), "Int")
    vocab.add_pfunc((f"t{i}" for i in range(5)), ("T" for _ in range(3)), "Int")
    T = vocab.parse_type("T")
    vocab.add_pfunc("w", (T, T), BuiltinTypes.INT)
    vocab2 = Vocabulary()
    vocab2.add_type("T")
    T2 = vocab2.parse_type("T")
    with pytest.raises(ValueError):
        vocab.add_pfunc("T", (T2,), "Bool")
    vocab.add_pfunc("o", (), BuiltinTypes.BOOL)

def test_merge():
    vocab1 = Vocabulary()
    vocab1.parse(
        """
        type A
        p: -> Bool
        f: A -> A
        """
    )
    vocab2 = Vocabulary()
    vocab2.parse(
        """
        type B
        j: -> Bool
        r: B -> B
        """
    )
    vocab1.merge(vocab1)
    vocab1.merge(vocab2)
    assert all(
        map(
            lambda x: x.name() in {
                "A", "B", "p",
                "f", "j", "f",
                "r"
            },
            vocab1.iter_symbols()
        )
    )


def test_domain():
    vocab = Vocabulary()
    vocab.parse("""
                type A
                j: A * A * A -> Bool
                """)
    j = vocab.parse_pfunc("j")
    a = vocab.parse_type("A")
    j_dom = j.domain()
    assert len(j_dom) == 3
    for type in iter(j_dom):
        assert type.name() == a.name()

