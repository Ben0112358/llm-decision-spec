from llm_decision_spec.expressions import Const, Field
from llm_decision_spec.operators.comparison import Gt
from llm_decision_spec.operators.strings import Contains, Regex
from llm_decision_spec.operators.logical import And


def ids(result):
    return sorted(e["id"] for e in result.data)


def test_contains_matches_substring(context):
    op = Contains(Field("merchant"), Const("A"))

    result = op.evaluate(context)

    assert ids(result) == [2, 3]


def test_contains_no_match(context):
    op = Contains(Field("merchant"), Const("XYZ"))

    result = op.evaluate(context)

    assert ids(result) == []


def test_contains_missing_field_excluded(context):
    op = Contains(Field("does_not_exist"), Const("foo"))

    result = op.evaluate(context)

    assert ids(result) == []


def test_contains_non_string_excluded(context):
    op = Contains(Field("amount"), Const("50"))

    result = op.evaluate(context)

    assert ids(result) == []


def test_regex_matches_pattern(context):
    op = Regex(Field("currency"), Const(r"S.K"))

    result = op.evaluate(context)

    assert ids(result) == [2, 3]


def test_regex_no_match(context):
    op = Regex(Field("merchant"), Const(r"^Z"))

    result = op.evaluate(context)

    assert ids(result) == []


def test_regex_missing_field_excluded(context):
    op = Regex(Field("does_not_exist"), Const(r".*"))

    result = op.evaluate(context)

    assert ids(result) == []


def test_regex_non_string_excluded(context):
    op = Regex(Field("amount"), Const(r"\d+"))

    result = op.evaluate(context)

    assert ids(result) == []


def test_contains_with_and(context):
    op = And(
        Contains(Field("merchant"), Const("A")),
        Gt(Field("amount"), Const(60)),
    )

    result = op.evaluate(context)

    assert ids(result) == [2]
