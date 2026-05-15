from llm_decision_spec.reducers.counting import Count, CountDistinct
from llm_decision_spec.operators.logical import And
from tests.utils.operators import DummyOperator


def make(context, ids):
    return DummyOperator(
        [event for event in context.events if event["id"] in ids]
    )


def test_count_all_rows(context):
    op = make(context, [1, 2, 3])

    result = Count().evaluate(op, context)

    assert result == 3


def test_count_subset(context):
    op = make(context, [1, 2])

    result = Count().evaluate(op, context)

    assert result == 2


def test_count_empty(context):
    op = make(context, [])

    result = Count().evaluate(op, context)

    assert result == 0


def test_count_field_non_null(context):
    op = make(context, [1, 2, 3])

    result = Count("amount").evaluate(op, context)

    assert result == 3


def test_count_field_mixed_nulls(context):
    modified = context.events.copy()
    modified[0] = {**modified[0], "amount": None}

    op = DummyOperator(modified)

    result = Count("amount").evaluate(op, context)

    assert result == 2


def test_count_distinct_transactions(context):
    op = make(context, [1, 2, 2, 3])

    result = CountDistinct().evaluate(op, context)

    assert result == 3


def test_count_distinct_subset(context):
    op = make(context, [1, 1, 2])

    result = CountDistinct().evaluate(op, context)

    assert result == 2


def test_count_distinct_empty(context):
    op = make(context, [])

    result = CountDistinct().evaluate(op, context)

    assert result == 0


def test_count_distinct_field(context):
    op = make(context, [1, 2, 3])

    result = CountDistinct("merchant").evaluate(op, context)

    assert result == 2


def test_count_distinct_field_empty(context):
    op = make(context, [])

    result = CountDistinct("merchant").evaluate(op, context)

    assert result == 0


def test_count_with_and(context):
    a = make(context, [1, 2])
    b = make(context, [2, 3])

    expr = And(a, b)

    result = Count().evaluate(expr, context)

    assert result == 1
