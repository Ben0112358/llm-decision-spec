import pytest
from tests.utils.operators import DummyOperator
from llm_decision_spec.operators.logical import And, Or, Not


def test_and_idempotent(ctx):
    A = DummyOperator([tx for tx in ctx.transactions if ctx.key(tx) in {1, 2}])

    result = And(A, A).evaluate(ctx)

    assert {ctx.key(tx) for tx in result.data} == {1, 2}


def test_or_idempotent(ctx):
    A = DummyOperator([tx for tx in ctx.transactions if ctx.key(tx) in {1, 2}])

    result = Or(A, A).evaluate(ctx)

    assert {ctx.key(tx) for tx in result.data} == {1, 2}

def test_and_commutative(ctx):
    A = DummyOperator([tx for tx in ctx.transactions if ctx.key(tx) in {1, 2}])
    B = DummyOperator([tx for tx in ctx.transactions if ctx.key(tx) in {2, 3}])

    r1 = And(A, B).evaluate(ctx)
    r2 = And(B, A).evaluate(ctx)

    assert {ctx.key(tx) for tx in r1.data} == {ctx.key(tx) for tx in r2.data}

def test_or_commutative(ctx):
    A = DummyOperator([tx for tx in ctx.transactions if ctx.key(tx) in {1, 2}])
    B = DummyOperator([tx for tx in ctx.transactions if ctx.key(tx) in {2, 3}])

    r1 = Or(A, B).evaluate(ctx)
    r2 = Or(B, A).evaluate(ctx)

    assert {ctx.key(tx) for tx in r1.data} == {ctx.key(tx) for tx in r2.data}


def test_and_associative(ctx):
    A = DummyOperator([tx for tx in ctx.transactions if ctx.key(tx) in {1, 2}])
    B = DummyOperator([tx for tx in ctx.transactions if ctx.key(tx) in {2, 3}])
    C = DummyOperator([tx for tx in ctx.transactions if ctx.key(tx) in {3}])

    left = And(And(A, B), C).evaluate(ctx)
    right = And(A, And(B, C)).evaluate(ctx)

    assert {ctx.key(tx) for tx in left.data} == {ctx.key(tx) for tx in right.data}


def test_or_associative(ctx):
    A = DummyOperator([tx for tx in ctx.transactions if ctx.key(tx) in {1, 2}])
    B = DummyOperator([tx for tx in ctx.transactions if ctx.key(tx) in {2, 3}])
    C = DummyOperator([tx for tx in ctx.transactions if ctx.key(tx) in {3}])

    left = Or(Or(A, B), C).evaluate(ctx)
    right = Or(A, Or(B, C)).evaluate(ctx)

    assert {ctx.key(tx) for tx in left.data} == {ctx.key(tx) for tx in right.data}

def test_and_identity(ctx):
    U = DummyOperator(ctx.transactions)

    A = DummyOperator([tx for tx in ctx.transactions if ctx.key(tx) in {1, 2}])

    result = And(A, U).evaluate(ctx)

    assert {ctx.key(tx) for tx in result.data} == {1, 2}


def test_or_identity(ctx):
    A = DummyOperator([tx for tx in ctx.transactions if ctx.key(tx) in {1, 2}])
    empty = DummyOperator([])

    result = Or(A, empty).evaluate(ctx)

    assert {ctx.key(tx) for tx in result.data} == {1, 2}


def test_double_negation(ctx):
    A = DummyOperator([tx for tx in ctx.transactions if ctx.key(tx) in {1, 2}])

    result = Not(Not(A)).evaluate(ctx)

    assert {ctx.key(tx) for tx in result.data} == {1, 2}

def test_complement_union(ctx):
    A = DummyOperator([tx for tx in ctx.transactions if ctx.key(tx) in {1, 2}])
    U = DummyOperator(ctx.transactions)

    result = Or(A, Not(A)).evaluate(ctx)

    assert {ctx.key(tx) for tx in result.data} == {ctx.key(tx) for tx in U._data}

def test_contradiction(ctx):
    A = DummyOperator([tx for tx in ctx.transactions if ctx.key(tx) in {1, 2}])

    result = And(A, Not(A)).evaluate(ctx)

    assert len(result.data) == 0


    