"""End-to-end: selection then aggregation over Context.events."""

from llm_decision_spec.expressions import Const, Field
from llm_decision_spec.expressions.arithmetic import Add
from llm_decision_spec.filters.comparison import Gt
from llm_decision_spec.filters.membership import In
from llm_decision_spec.operators.logical import And
from llm_decision_spec.reducers.numeric import Sum


def test_filter_then_sum(context):
    op = And(
        Gt(Field("amount"), Const(50)),
        In(Field("currency"), Const(frozenset({"SEK", "USD"}))),
    )
    result = Sum(Field("amount")).evaluate(op, context)
    assert result == 300


def test_expr_in_comparison(context):
    op = Gt(
        Add(Field("amount"), Const(10)),
        Field("amount"),
    )
    result = op.evaluate(context)
    ids = sorted(e["id"] for e in result.data)
    assert ids == [1, 2, 3]
