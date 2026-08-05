from tests.helpers.operators import DummyOperator
from llm_decision_spec.operators.logical import And, Or, Not


def test_and_idempotent(context):
    A = DummyOperator(
        [event for event in context.events if context.key(event) in {1, 2}]
    )

    result = And(A, A).evaluate(context)

    assert {context.key(event) for event in result.data} == {1, 2}


def test_or_idempotent(context):
    A = DummyOperator(
        [event for event in context.events if context.key(event) in {1, 2}]
    )

    result = Or(A, A).evaluate(context)

    assert {context.key(event) for event in result.data} == {1, 2}


def test_and_commutative(context):
    A = DummyOperator(
        [event for event in context.events if context.key(event) in {1, 2}]
    )
    B = DummyOperator(
        [event for event in context.events if context.key(event) in {2, 3}]
    )

    r1 = And(A, B).evaluate(context)
    r2 = And(B, A).evaluate(context)

    assert {context.key(event) for event in r1.data} == {
        context.key(event) for event in r2.data
    }


def test_or_commutative(context):
    A = DummyOperator(
        [event for event in context.events if context.key(event) in {1, 2}]
    )
    B = DummyOperator(
        [event for event in context.events if context.key(event) in {2, 3}]
    )

    r1 = Or(A, B).evaluate(context)
    r2 = Or(B, A).evaluate(context)

    assert {context.key(event) for event in r1.data} == {
        context.key(event) for event in r2.data
    }


def test_and_associative(context):
    A = DummyOperator(
        [event for event in context.events if context.key(event) in {1, 2}]
    )
    B = DummyOperator(
        [event for event in context.events if context.key(event) in {2, 3}]
    )
    C = DummyOperator(
        [event for event in context.events if context.key(event) in {3}]
    )

    left = And(And(A, B), C).evaluate(context)
    right = And(A, And(B, C)).evaluate(context)

    assert {context.key(event) for event in left.data} == {
        context.key(event) for event in right.data
    }


def test_or_associative(context):
    A = DummyOperator(
        [event for event in context.events if context.key(event) in {1, 2}]
    )
    B = DummyOperator(
        [event for event in context.events if context.key(event) in {2, 3}]
    )
    C = DummyOperator(
        [event for event in context.events if context.key(event) in {3}]
    )

    left = Or(Or(A, B), C).evaluate(context)
    right = Or(A, Or(B, C)).evaluate(context)

    assert {context.key(event) for event in left.data} == {
        context.key(event) for event in right.data
    }


def test_and_identity(context):
    U = DummyOperator(context.events)

    A = DummyOperator(
        [event for event in context.events if context.key(event) in {1, 2}]
    )

    result = And(A, U).evaluate(context)

    assert {context.key(event) for event in result.data} == {1, 2}


def test_or_identity(context):
    A = DummyOperator(
        [event for event in context.events if context.key(event) in {1, 2}]
    )
    empty = DummyOperator([])

    result = Or(A, empty).evaluate(context)

    assert {context.key(event) for event in result.data} == {1, 2}


def test_double_negation(context):
    A = DummyOperator(
        [event for event in context.events if context.key(event) in {1, 2}]
    )

    result = Not(Not(A)).evaluate(context)

    assert {context.key(event) for event in result.data} == {1, 2}


def test_complement_union(context):
    A = DummyOperator(
        [event for event in context.events if context.key(event) in {1, 2}]
    )
    U = DummyOperator(context.events)

    result = Or(A, Not(A)).evaluate(context)

    assert {context.key(event) for event in result.data} == {
        context.key(event) for event in U._data
    }


def test_contradiction(context):
    A = DummyOperator(
        [event for event in context.events if context.key(event) in {1, 2}]
    )

    result = And(A, Not(A)).evaluate(context)

    assert len(result.data) == 0
