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


def make(context, ids):
    return DummyOperator(
        [event for event in context.events if event["id"] in ids]
    )


def test_sum_basic(context):
    op = make(context, [1, 2, 3])

    result = Sum("amount").evaluate(op, context)

    assert result == 350


def test_sum_subset(context):
    op = make(context, [2, 3])

    result = Sum("amount").evaluate(op, context)

    assert result == 150


def test_sum_empty(context):
    op = make(context, [])

    result = Sum("amount").evaluate(op, context)

    assert result is None


def test_avg_basic(context):
    op = make(context, [1, 2, 3])

    result = Average("amount").evaluate(op, context)

    assert result == pytest.approx(116.6666666)


def test_avg_subset(context):
    op = make(context, [1, 2])

    result = Average("amount").evaluate(op, context)

    assert result == pytest.approx(150)


def test_avg_empty(context):
    op = make(context, [])

    result = Average("amount").evaluate(op, context)

    assert result is None


def test_min_basic(context):
    op = make(context, [1, 2, 3])

    result = Min("amount").evaluate(op, context)

    assert result == 50


def test_min_subset(context):
    op = make(context, [1, 2])

    result = Min("amount").evaluate(op, context)

    assert result == 100


def test_min_empty(context):
    op = make(context, [])

    result = Min("amount").evaluate(op, context)

    assert result is None


def test_max_basic(context):
    op = make(context, [1, 2, 3])

    result = Max("amount").evaluate(op, context)

    assert result == 200


def test_max_subset(context):
    op = make(context, [2, 3])

    result = Max("amount").evaluate(op, context)

    assert result == 100


def test_max_empty(context):
    op = make(context, [])

    result = Max("amount").evaluate(op, context)

    assert result is None


def test_percentile_0(context):
    op = make(context, [1, 2, 3])

    result = Percentile("amount", 0.0).evaluate(op, context)

    assert result == 50


def test_percentile_median(context):
    op = make(context, [1, 2, 3])

    result = Percentile("amount", 0.5).evaluate(op, context)

    assert result == 100


def test_percentile_1(context):
    op = make(context, [1, 2, 3])

    result = Percentile("amount", 1.0).evaluate(op, context)

    assert result == 200


def test_percentile_empty(context):
    op = make(context, [])

    result = Percentile("amount", 0.5).evaluate(op, context)

    assert result is None


def test_numeric_with_and(context):
    a = make(context, [1, 2])
    b = make(context, [2, 3])

    expr = And(a, b)

    result = Sum("amount").evaluate(expr, context)

    assert result == 100
