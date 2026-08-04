from tests.utils.operators import DummyOperator
from tests.utils.events import event_ids
from tests.utils.assertions import assert_event_ids
from llm_decision_spec.operators.logical import And, Or, Not

# -------------------------
# AND
# -------------------------


def test_and_is_intersection(context):
    a = DummyOperator(event_ids([1, 2]))
    b = DummyOperator(event_ids([2, 3]))

    result = And(a, b).evaluate(context)

    assert_event_ids(result, [2], context)


# -------------------------
# OR
# -------------------------


def test_or_is_union(context):
    a = DummyOperator(event_ids([1, 2]))
    b = DummyOperator(event_ids([2, 3]))

    result = Or(a, b).evaluate(context)

    assert_event_ids(result, [1, 2, 3], context)


# -------------------------
# NOT
# -------------------------


def test_not_is_complement(context):
    a = DummyOperator(event_ids([1, 2]))

    result = Not(a).evaluate(context)

    assert_event_ids(result, [3], context)


# -------------------------
# COMPOSITION
# -------------------------


def test_composition_and_or(context):
    a = DummyOperator(event_ids([1, 2]))
    b = DummyOperator(event_ids([2, 3]))
    c = DummyOperator(event_ids([3]))

    expr = Or(And(a, b), c)

    result = expr.evaluate(context)

    assert_event_ids(result, [2, 3], context)
