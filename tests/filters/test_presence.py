from llm_decision_spec.expressions import Const, Field
from llm_decision_spec.filters.comparison import Gt
from llm_decision_spec.filters.presence import Has, Missing
from llm_decision_spec.operators.logical import And


def ids(result):
    return sorted(e["id"] for e in result.data)


def test_has_field_exists(context):
    op = Has(Field("currency"))

    result = op.evaluate(context)

    assert ids(result) == [1, 2, 3]


def test_has_nonexistent_field(context):
    op = Has(Field("does_not_exist"))

    result = op.evaluate(context)

    assert ids(result) == []


def test_missing_field(context):
    op = Missing(Field("currency"))

    result = op.evaluate(context)

    assert ids(result) == []


def test_missing_nonexistent_field(context):
    op = Missing(Field("does_not_exist"))

    result = op.evaluate(context)

    assert ids(result) == [1, 2, 3]


def test_has_and_missing_are_complements(context):
    has = Has(Field("currency"))
    missing = Missing(Field("currency"))

    has_result = set(ids(has.evaluate(context)))
    missing_result = set(ids(missing.evaluate(context)))

    universe = set(e["id"] for e in context.events)

    assert has_result.isdisjoint(missing_result)
    assert has_result.union(missing_result) == universe


def test_missing_with_and(context):
    op = And(
        Has(Field("amount")),
        Gt(Field("amount"), Const(100)),
    )

    result = op.evaluate(context)

    assert ids(result) == [1]
