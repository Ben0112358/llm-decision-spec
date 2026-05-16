from llm_decision_spec.filters.comparison import Eq, Ne, Gt, Gte, Lt, Lte


def ids(result):
    return sorted(e["id"] for e in result.data)


def test_eq_matches_exact(context):
    op = Eq("currency", "SEK")

    result = op.evaluate(context)

    assert ids(result) == [2, 3]


def test_eq_no_matches(context):
    op = Eq("currency", "EUR")

    result = op.evaluate(context)

    assert ids(result) == []


def test_eq_missing_field(context):
    op = Eq("nonexistent", "X")

    result = op.evaluate(context)

    assert ids(result) == []


def test_ne_excludes_matches(context):
    op = Ne("currency", "SEK")

    result = op.evaluate(context)

    assert ids(result) == [1]


def test_ne_missing_field_excluded(context):
    op = Ne("nonexistent", "X")

    result = op.evaluate(context)

    assert ids(result) == []


def test_gt_amount(context):
    op = Gt("amount", 100)

    result = op.evaluate(context)

    assert ids(result) == [1]


def test_gte_amount(context):
    op = Gte("amount", 100)

    result = op.evaluate(context)

    assert ids(result) == [1, 2]


def test_lt_amount(context):
    op = Lt("amount", 100)

    result = op.evaluate(context)

    assert ids(result) == [3]


def test_lte_amount(context):
    op = Lte("amount", 100)

    result = op.evaluate(context)

    assert ids(result) == [2, 3]


def test_comparisons_ignore_missing_fields(context):
    op = Gt("does_not_exist", 10)

    result = op.evaluate(context)

    assert ids(result) == []
