import pytest

from llm_decision_spec.expressions import Const, Field
from llm_decision_spec.filters.comparison import Gt
from llm_decision_spec.expressions.arithmetic import Add
from llm_decision_spec.operators.logical import And


def test_add_rejects_operator_child():
    with pytest.raises(TypeError, match="must be Expr"):
        Add(Gt(Field("a"), Const(1)), Const(2))


def test_and_rejects_expr_child():
    with pytest.raises(TypeError, match="must be Operator"):
        And(Field("x"), Field("y"))
