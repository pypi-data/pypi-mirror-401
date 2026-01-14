from sli_lib.fodot import Inferenceable
from sli_lib.solver import Z3Solver
import pytest

def test_z3_solver():
    inferenceable  = Inferenceable.from_specification("""
vocabulary {
    type T := { 0, 1 }
    p: T -> Bool
    t: T -> T
}
theory {
    !x in T: p(x) => t(x) = x.
}
structure {}
""")
    solver = Z3Solver(inferenceable)
    assert solver.check()
    solver_iter = solver.iter_models()
    solver_iter.disable_skip_infinite()
    solver_iter.enable_skip_infinite()
    next(solver_iter)
    solver.check()
    with pytest.raises(RuntimeError):
        next(solver_iter)
    solver_iter = solver.iter_glob_models()
    for _ in solver_iter:
        pass
    assert not solver.check()

def test_get_range():
    inferenceable  = Inferenceable.from_specification("""
vocabulary {
    type T := { 1..3 }
    t: T -> T
}
theory {
    t(1) ~= 2.
}
structure {}
""")
    solver = Z3Solver(inferenceable)
    t_1_range = solver.get_range("t", (1,))
    assert t_1_range is not None
    assert len(t_1_range) == 2
    assert (1,) in t_1_range
    assert (3,) in t_1_range
    # Test that t_1_range is iterable
    for _ in t_1_range:
        pass
    t_1_range.negate()
    value = ~t_1_range
