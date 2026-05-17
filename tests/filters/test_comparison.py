from llm_decision_spec.expressions import Const, Field
from llm_decision_spec.filters.comparison import Eq, Ne, Gt, Gte, Lt, Lte


def ids(result):
    return sorted(e["id"] for e in result.data)


def test_eq_matches_exact(context):
    op = Eq(Field("currency"), Const("SEK"))

    result = op.evaluate(context)

    assert ids(result) == [2, 3]


def test_eq_no_matches(context):
    op = Eq(Field("currency"), Const("EUR"))

    result = op.evaluate(context)

    assert ids(result) == []


def test_eq_missing_field(context):
    op = Eq(Field("nonexistent"), Const("X"))

    result = op.evaluate(context)

    assert ids(result) == []


def test_ne_excludes_matches(context):
    op = Ne(Field("currency"), Const("SEK"))

    result = op.evaluate(context)

    assert ids(result) == [1]


def test_ne_missing_field_excluded(context):
    op = Ne(Field("nonexistent"), Const("X"))

    result = op.evaluate(context)

    assert ids(result) == []


def test_gt_amount(context):
    op = Gt(Field("amount"), Const(100))

    result = op.evaluate(context)

    assert ids(result) == [1]


def test_gte_amount(context):
    op = Gte(Field("amount"), Const(100))

    result = op.evaluate(context)

    assert ids(result) == [1, 2]


def test_lt_amount(context):
    op = Lt(Field("amount"), Const(100))

    result = op.evaluate(context)

    assert ids(result) == [3]


def test_lte_amount(context):
    op = Lte(Field("amount"), Const(100))

    result = op.evaluate(context)

    assert ids(result) == [2, 3]


def test_comparisons_ignore_missing_fields(context):
    op = Gt(Field("does_not_exist"), Const(10))

    result = op.evaluate(context)

    assert ids(result) == []
