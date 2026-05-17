from llm_decision_spec.expressions import Const


def test_const_ignores_event():
    assert Const(42).eval({}) == 42
    assert Const("x").eval({"other": 1}) == "x"
