from llm_decision_spec.operators.logical import And, Not
from llm_decision_spec.reducers.boolean import Exists
from tests.helpers.operators import DummyOperator


def test_exists_true_when_non_empty(context):
    op = DummyOperator([context.events[0], context.events[1]])

    result = Exists().evaluate(op, context)

    assert result is True


def test_exists_false_when_empty(context):
    op = DummyOperator([])

    result = Exists().evaluate(op, context)

    assert result is False


def test_exists_with_and(context):
    a = DummyOperator(
        [event for event in context.events if event["id"] in [1, 2]]
    )
    b = DummyOperator(
        [event for event in context.events if event["id"] in [2, 3]]
    )

    expr = And(a, b)

    result = Exists().evaluate(expr, context)

    assert result is True


def test_exists_with_not(context):
    a = DummyOperator(context.events)

    expr = Not(a)

    result = Exists().evaluate(expr, context)

    assert result is False


def test_exists_is_deterministic(context):
    op = DummyOperator([context.events[0], context.events[1]])

    r1 = Exists().evaluate(op, context)
    r2 = Exists().evaluate(op, context)

    assert r1 == r2


def test_exists_on_full_universe(context):
    op = DummyOperator(context.events)

    result = Exists().evaluate(op, context)

    assert result is True
