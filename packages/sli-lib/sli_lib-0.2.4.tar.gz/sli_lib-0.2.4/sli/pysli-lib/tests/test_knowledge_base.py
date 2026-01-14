import pytest
from sli_lib.fodot import KnowledgeBase
from sli_lib.fodot.knowledge_base import Procedure


def test_escaped_procedure():
    kb = KnowledgeBase.from_str("""
procedure main() {
    print("bla")
print("escaped!!!")
}
    """)
    main = kb["main"]
    assert isinstance(main, Procedure)
    with pytest.raises(RuntimeError):
        _ = main.compile()
