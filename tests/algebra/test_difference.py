from tests.utils.operators import DummyOperator
from tests.utils.events import event_ids
from llm_decision_spec.operators.logical import And, Not, Difference


def test_difference_is_and_not_equivalent(context):
    a = DummyOperator(event_ids([1, 2, 3]))
    b = DummyOperator(event_ids([2]))

    result = Difference(a, b).evaluate(context)
    reference = And(a, Not(b)).evaluate(context)

    assert set(context.key(event) for event in result.data) == set(
        context.key(event) for event in reference.data
    )


def test_difference_is_subset_of_left_operand(context):
    a = DummyOperator(event_ids([1, 2, 3]))
    b = DummyOperator(event_ids([2]))

    result = Difference(a, b).evaluate(context)

    result_set = {context.key(event) for event in result.data}
    a_set = {context.key(event) for event in a.evaluate(context).data}

    assert result_set.issubset(a_set)


def test_difference_with_self_is_empty(context):
    a = DummyOperator(event_ids([1, 2, 3]))

    result = Difference(a, a).evaluate(context)

    assert len(result.data) == 0


def test_difference_with_empty_set(context):
    a = DummyOperator(event_ids([1, 2, 3]))
    empty = DummyOperator([])

    result = Difference(a, empty).evaluate(context)

    assert set(context.key(event) for event in result.data) == {1, 2, 3}


def test_empty_difference_with_anything(context):
    a = DummyOperator([])
    b = DummyOperator(event_ids([1, 2, 3]))

    result = Difference(a, b).evaluate(context)

    assert len(result.data) == 0


def test_difference_is_stable(context):
    a = DummyOperator(event_ids([1, 2, 3]))
    b = DummyOperator(event_ids([2]))

    r1 = Difference(a, b).evaluate(context)
    r2 = Difference(a, b).evaluate(context)

    assert set(context.key(event) for event in r1.data) == set(
        context.key(event) for event in r2.data
    )


def test_difference_returns_expected_ids(context):
    a = DummyOperator(event_ids([1, 2, 3]))
    b = DummyOperator(event_ids([2]))

    result = Difference(a, b).evaluate(context)

    assert {context.key(event) for event in result.data} == {1, 3}
