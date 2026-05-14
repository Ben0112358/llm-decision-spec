from llm_decision_spec.operators.logical import And, Not
from llm_decision_spec.reducers.boolean import Exists
from tests.utils.operators import DummyOperator


def test_exists_true_when_non_empty(ctx):
    op = DummyOperator([ctx.transactions[0], ctx.transactions[1]])

    result = Exists().evaluate(op, ctx)

    assert result is True


def test_exists_false_when_empty(ctx):
    op = DummyOperator([])

    result = Exists().evaluate(op, ctx)

    assert result is False


def test_exists_with_and(ctx):
    a = DummyOperator([tx for tx in ctx.transactions if tx["id"] in [1, 2]])
    b = DummyOperator([tx for tx in ctx.transactions if tx["id"] in [2, 3]])

    expr = And(a, b)

    result = Exists().evaluate(expr, ctx)

    assert result is True


def test_exists_with_not(ctx):
    a = DummyOperator(ctx.transactions)

    expr = Not(a)

    result = Exists().evaluate(expr, ctx)

    assert result is False


def test_exists_is_deterministic(ctx):
    op = DummyOperator([ctx.transactions[0], ctx.transactions[1]])

    r1 = Exists().evaluate(op, ctx)
    r2 = Exists().evaluate(op, ctx)

    assert r1 == r2


def test_exists_on_full_universe(ctx):
    op = DummyOperator(ctx.transactions)

    result = Exists().evaluate(op, ctx)

    assert result is True
