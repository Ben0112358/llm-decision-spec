import pytest
from llm_decision_spec.reducers.counting import Count, CountDistinct
from llm_decision_spec.operators.logical import And
from tests.utils.operators import DummyOperator



def make(ctx, ids):
    return DummyOperator([tx for tx in ctx.transactions if tx["id"] in ids])



def test_count_all_rows(ctx):
    op = make(ctx, [1, 2, 3])

    result = Count().evaluate(op, ctx)

    assert result == 3


def test_count_subset(ctx):
    op = make(ctx, [1, 2])

    result = Count().evaluate(op, ctx)

    assert result == 2


def test_count_empty(ctx):
    op = make(ctx, [])

    result = Count().evaluate(op, ctx)

    assert result == 0


def test_count_field_non_null(ctx):
    op = make(ctx, [1, 2, 3])

    result = Count("amount").evaluate(op, ctx)

    assert result == 3


def test_count_field_mixed_nulls(ctx):
    modified = ctx.transactions.copy()
    modified[0] = {**modified[0], "amount": None}

    op = DummyOperator(modified)

    result = Count("amount").evaluate(op, ctx)

    assert result == 2


def test_count_distinct_transactions(ctx):
    op = make(ctx, [1, 2, 2, 3])

    result = CountDistinct().evaluate(op, ctx)

    assert result == 3


def test_count_distinct_subset(ctx):
    op = make(ctx, [1, 1, 2])

    result = CountDistinct().evaluate(op, ctx)

    assert result == 2


def test_count_distinct_empty(ctx):
    op = make(ctx, [])

    result = CountDistinct().evaluate(op, ctx)

    assert result == 0



def test_count_distinct_field(ctx):
    op = make(ctx, [1, 2, 3])

    result = CountDistinct("merchant").evaluate(op, ctx)
    
    assert result == 2


def test_count_distinct_field_empty(ctx):
    op = make(ctx, [])

    result = CountDistinct("merchant").evaluate(op, ctx)

    assert result == 0


def test_count_with_and(ctx):
    a = make(ctx, [1, 2])
    b = make(ctx, [2, 3])

    expr = And(a, b)

    result = Count().evaluate(expr, ctx)

    assert result == 1