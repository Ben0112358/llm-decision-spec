import pytest
from llm_decision_spec.reducers.numeric import (
    Sum,
    Average,
    Min,
    Max,
    Percentile,
)
from llm_decision_spec.operators.logical import And
from tests.utils.operators import DummyOperator


def make(ctx, ids):
    return DummyOperator([tx for tx in ctx.transactions if tx["id"] in ids])


def test_sum_basic(ctx):
    op = make(ctx, [1, 2, 3])

    result = Sum("amount").evaluate(op, ctx)

    assert result == 350


def test_sum_subset(ctx):
    op = make(ctx, [2, 3])

    result = Sum("amount").evaluate(op, ctx)

    assert result == 150


def test_sum_empty(ctx):
    op = make(ctx, [])

    result = Sum("amount").evaluate(op, ctx)

    assert result is None


def test_avg_basic(ctx):
    op = make(ctx, [1, 2, 3])

    result = Average("amount").evaluate(op, ctx)

    assert result == pytest.approx(116.6666666)


def test_avg_subset(ctx):
    op = make(ctx, [1, 2])

    result = Average("amount").evaluate(op, ctx)

    assert result == pytest.approx(150)


def test_avg_empty(ctx):
    op = make(ctx, [])

    result = Average("amount").evaluate(op, ctx)

    assert result is None


def test_min_basic(ctx):
    op = make(ctx, [1, 2, 3])

    result = Min("amount").evaluate(op, ctx)

    assert result == 50


def test_min_subset(ctx):
    op = make(ctx, [1, 2])

    result = Min("amount").evaluate(op, ctx)

    assert result == 100


def test_min_empty(ctx):
    op = make(ctx, [])

    result = Min("amount").evaluate(op, ctx)

    assert result is None


def test_max_basic(ctx):
    op = make(ctx, [1, 2, 3])

    result = Max("amount").evaluate(op, ctx)

    assert result == 200


def test_max_subset(ctx):
    op = make(ctx, [2, 3])

    result = Max("amount").evaluate(op, ctx)

    assert result == 100


def test_max_empty(ctx):
    op = make(ctx, [])

    result = Max("amount").evaluate(op, ctx)

    assert result is None


def test_percentile_0(ctx):
    op = make(ctx, [1, 2, 3])

    result = Percentile("amount", 0.0).evaluate(op, ctx)

    assert result == 50


def test_percentile_median(ctx):
    op = make(ctx, [1, 2, 3])

    result = Percentile("amount", 0.5).evaluate(op, ctx)

    assert result == 100


def test_percentile_1(ctx):
    op = make(ctx, [1, 2, 3])

    result = Percentile("amount", 1.0).evaluate(op, ctx)

    assert result == 200


def test_percentile_empty(ctx):
    op = make(ctx, [])

    result = Percentile("amount", 0.5).evaluate(op, ctx)

    assert result is None


def test_numeric_with_and(ctx):
    a = make(ctx, [1, 2])
    b = make(ctx, [2, 3])

    expr = And(a, b)

    result = Sum("amount").evaluate(expr, ctx)

    assert result == 100
