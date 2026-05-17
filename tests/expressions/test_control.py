import pytest
from llm_decision_spec.expressions.control import Coalesce, FillNA
from llm_decision_spec.filters.comparison import Gt
from llm_decision_spec.expressions.fields import Field
from llm_decision_spec.operators.logical import And
from llm_decision_spec.expressions import Const


def test_coalesce_requires_at_least_two_exprs():
    with pytest.raises(TypeError, match="requires at least 2 Exprs"):
        Coalesce(Field("x"))


def test_coalesce_returns_first_non_none_value():
    event = {"a": 1, "b": "2", "c": True}
    assert Coalesce(Field("a"), Field("b"), Field("c")).eval(event) == 1
    event = {"a": None, "b": "2", "c": True}
    assert Coalesce(Field("a"), Field("b"), Field("c")).eval(event) == "2"
    event = {"a": None, "b": None, "c": True}
    assert Coalesce(Field("a"), Field("b"), Field("c")).eval(event) is True
    event = {"a": None, "b": None, "c": None}
    assert Coalesce(Field("a"), Field("b"), Field("c")).eval(event) is None


def test_coalesce_rejects_non_exprs():
    with pytest.raises(TypeError, match="must be Expr, got Operator"):
        Coalesce(Field("a"), And(Gt(Field("b"), Const(1))))


def test_coalesce_rejects_non_expr_literal():
    with pytest.raises(TypeError, match="must be Expr"):
        Coalesce(Field("a"), 123)


def test_coalesce_with_missing_key():
    event = {"a": 1}
    assert Coalesce(Field("a"), Field("b")).eval(event) == 1


def test_fillna():
    event = {"a": 1}
    assert FillNA(Field("a"), Field("b")).eval(event) == 1

    event = {"a": None}
    assert FillNA(Field("a"), Const(0)).eval(event) == 0

    event = {"a": None, "b": 3}
    assert FillNA(Field("a"), Const(99)).eval(event) == 99


def test_fillna_rejects_non_exprs():
    with pytest.raises(TypeError, match="must be Expr"):
        FillNA(Field("a"), 123)


def test_fillna_rejects_non_expr_literal():
    with pytest.raises(TypeError, match="must be Expr"):
        FillNA(Field("a"), Gt(Field("b"), Const(1)))


def test_fillna_preserves_falsy_values():
    assert FillNA(Field("a"), Const(99)).eval({"a": 0}) == 0
    assert FillNA(Field("a"), Const(True)).eval({"a": False}) is False
    assert FillNA(Field("a"), Const("x")).eval({"a": ""}) == ""
