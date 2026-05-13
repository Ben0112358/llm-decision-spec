import pytest
from tests.utils.operators import DummyOperator
from tests.utils.transactions import tx_ids
from tests.utils.assertions import assert_tx_ids
from llm_decision_spec.operators.logical import And, Not, Difference


def test_difference_is_and_not_equivalent(ctx):
    a = DummyOperator(tx_ids([1, 2, 3]))
    b = DummyOperator(tx_ids([2]))

    result = Difference(a, b).evaluate(ctx)
    reference = And(a, Not(b)).evaluate(ctx)

    assert set(ctx.key(tx) for tx in result.data) == \
           set(ctx.key(tx) for tx in reference.data)
    
def test_difference_is_subset_of_left_operand(ctx):
    a = DummyOperator(tx_ids([1, 2, 3]))
    b = DummyOperator(tx_ids([2]))

    result = Difference(a, b).evaluate(ctx)

    result_set = {ctx.key(tx) for tx in result.data}
    a_set = {ctx.key(tx) for tx in a.evaluate(ctx).data}

    assert result_set.issubset(a_set)

def test_difference_with_self_is_empty(ctx):
    a = DummyOperator(tx_ids([1, 2, 3]))

    result = Difference(a, a).evaluate(ctx)

    assert len(result.data) == 0

def test_difference_with_empty_set(ctx):
    a = DummyOperator(tx_ids([1, 2, 3]))
    empty = DummyOperator([])

    result = Difference(a, empty).evaluate(ctx)

    assert set(ctx.key(tx) for tx in result.data) == {1, 2, 3}

def test_empty_difference_with_anything(ctx):
    a = DummyOperator([])
    b = DummyOperator(tx_ids([1, 2, 3]))

    result = Difference(a, b).evaluate(ctx)

    assert len(result.data) == 0

def test_difference_is_stable(ctx):
    a = DummyOperator(tx_ids([1, 2, 3]))
    b = DummyOperator(tx_ids([2]))

    r1 = Difference(a, b).evaluate(ctx)
    r2 = Difference(a, b).evaluate(ctx)

    assert set(ctx.key(tx) for tx in r1.data) == \
           set(ctx.key(tx) for tx in r2.data)
    
def test_difference_returns_expected_ids(ctx):
    a = DummyOperator(tx_ids([1, 2, 3]))
    b = DummyOperator(tx_ids([2]))

    result = Difference(a, b).evaluate(ctx)

    assert {ctx.key(tx) for tx in result.data} == {1, 3}