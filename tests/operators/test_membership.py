from llm_decision_spec.expressions import Const, Field
from llm_decision_spec.operators.comparison import Gt
from llm_decision_spec.operators.membership import In, NotIn
from llm_decision_spec.operators.logical import And


def ids(result):
    return sorted(e["id"] for e in result.data)


def test_in_matches_values(context):
    op = In(Field("currency"), Const(frozenset({"SEK"})))

    result = op.evaluate(context)

    assert ids(result) == [2, 3]


def test_in_multiple_values(context):
    op = In(Field("currency"), Const(frozenset({"SEK", "USD"})))

    result = op.evaluate(context)

    assert ids(result) == [1, 2, 3]


def test_in_no_matches(context):
    op = In(Field("currency"), Const(frozenset({"EUR"})))

    result = op.evaluate(context)

    assert ids(result) == []


def test_in_missing_field_excluded(context):
    op = In(Field("nonexistent"), Const(frozenset({"X"})))

    result = op.evaluate(context)

    assert ids(result) == []


def test_not_in_filters_out_values(context):
    op = NotIn(Field("currency"), Const(frozenset({"SEK"})))

    result = op.evaluate(context)

    assert ids(result) == [1]


def test_not_in_multiple_values(context):
    op = NotIn(Field("currency"), Const(frozenset({"SEK", "USD"})))

    result = op.evaluate(context)

    assert ids(result) == []


def test_not_in_missing_field_excluded(context):
    op = NotIn(Field("nonexistent"), Const(frozenset({"X"})))

    result = op.evaluate(context)

    assert ids(result) == []


def test_membership_with_and(context):
    op = And(
        In(Field("currency"), Const(frozenset({"SEK", "USD"}))),
        Gt(Field("amount"), Const(100)),
    )

    result = op.evaluate(context)

    assert ids(result) == [1]
