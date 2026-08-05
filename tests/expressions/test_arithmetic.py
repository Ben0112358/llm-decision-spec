import pytest

from llm_decision_spec.expressions import (
    Add,
    Const,
    Field,
    Mul,
    Neg,
    Pow,
    Sub,
    Abs,
    Div,
)
from llm_decision_spec.operators.comparison import Gt


def test_add():
    event = {"a": 10, "b": 3}
    assert Add(Field("a"), Field("b")).eval(event) == 13


def test_add_propagates_none():
    event = {"a": 10}
    assert Add(Field("a"), Field("b")).eval(event) is None


def test_sub_mul_pow():
    event = {"a": 10, "b": 2}
    assert Sub(Field("a"), Field("b")).eval(event) == 8
    assert Mul(Field("a"), Field("b")).eval(event) == 20
    assert Pow(Field("a"), Const(2)).eval(event) == 100


def test_neg():
    event = {"a": 5}
    assert Neg(Field("a")).eval(event) == -5


def test_add_rejects_operator():
    with pytest.raises(TypeError, match="must be Expr"):
        Add(Gt(Field("a"), Const(1)), Const(2))


def test_abs():
    event = {"a": -5}
    assert Abs(Field("a")).eval(event) == 5


def test_div():
    event = {"a": 10, "b": 2}
    assert Div(Field("a"), Field("b")).eval(event) == 5


def test_div_propagates_none():
    event = {"a": 10}
    assert Div(Field("a"), Field("b")).eval(event) is None


def test_div_by_zero():
    event = {"a": 10, "b": 0}
    with pytest.raises(ZeroDivisionError):
        Div(Field("a"), Field("b")).eval(event)
