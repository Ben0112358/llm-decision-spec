from tests.utils.operators import DummyOperator
from tests.utils.transactions import tx_ids
from tests.utils.assertions import assert_tx_ids
from llm_decision_spec.operators.logical import And, Or, Not


# -------------------------
# AND
# -------------------------


def test_and_is_intersection(ctx):
    a = DummyOperator(tx_ids([1, 2]))
    b = DummyOperator(tx_ids([2, 3]))

    result = And(a, b).evaluate(ctx)

    assert_tx_ids(result, [2], ctx)


# -------------------------
# OR
# -------------------------


def test_or_is_union(ctx):
    a = DummyOperator(tx_ids([1, 2]))
    b = DummyOperator(tx_ids([2, 3]))

    result = Or(a, b).evaluate(ctx)

    assert_tx_ids(result, [1, 2, 3], ctx)


# -------------------------
# NOT
# -------------------------


def test_not_is_complement(ctx):
    a = DummyOperator(tx_ids([1, 2]))

    result = Not(a).evaluate(ctx)

    assert_tx_ids(result, [3], ctx)


# -------------------------
# COMPOSITION
# -------------------------


def test_composition_and_or(ctx):
    a = DummyOperator(tx_ids([1, 2]))
    b = DummyOperator(tx_ids([2, 3]))
    c = DummyOperator(tx_ids([3]))

    expr = Or(And(a, b), c)

    result = expr.evaluate(ctx)

    assert_tx_ids(result, [2, 3], ctx)
