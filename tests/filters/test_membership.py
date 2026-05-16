from llm_decision_spec.filters.membership import In, NotIn


def ids(result):
    return sorted(e["id"] for e in result.data)


def test_in_matches_values(context):
    op = In("currency", ["SEK"])

    result = op.evaluate(context)

    assert ids(result) == [2, 3]


def test_in_multiple_values(context):
    op = In("currency", ["SEK", "USD"])

    result = op.evaluate(context)

    assert ids(result) == [1, 2, 3]


def test_in_no_matches(context):
    op = In("currency", ["EUR"])

    result = op.evaluate(context)

    assert ids(result) == []


def test_in_missing_field_excluded(context):
    op = In("nonexistent", ["X"])

    result = op.evaluate(context)

    assert ids(result) == []


def test_not_in_filters_out_values(context):
    op = NotIn("currency", ["SEK"])

    result = op.evaluate(context)

    assert ids(result) == [1]


def test_not_in_multiple_values(context):
    op = NotIn("currency", ["SEK", "USD"])

    result = op.evaluate(context)

    assert ids(result) == []


def test_not_in_missing_field_excluded(context):
    op = NotIn("nonexistent", ["X"])

    result = op.evaluate(context)

    assert ids(result) == []


def test_membership_with_and(context):
    from llm_decision_spec.filters.comparison import Gt
    from llm_decision_spec.operators.logical import And

    op = And(
        In("currency", ["SEK", "USD"]),
        Gt("amount", 100),
    )

    result = op.evaluate(context)

    assert ids(result) == [1]
