from utils.dummy import DummyOperator
from utils.ops import OPS
import pytest


@pytest.mark.parametrize(
    "op,a_val,b_val,a_ev,b_ev,expected_val,expected_ev",
    [
        # OR
        (
            "+",
            True,
            True,
            [{"id": 1}],
            [{"id": 2}],
            True,
            [{"id": 1}, {"id": 2}],
        ),
        (
            "+",
            True,
            False,
            [{"id": 1}],
            [{"id": 2}],
            True,
            [{"id": 1}, {"id": 2}],
        ),
        (
            "+",
            False,
            True,
            [{"id": 1}],
            [{"id": 2}],
            True,
            [{"id": 1}, {"id": 2}],
        ),
        (
            "+",
            False,
            False,
            [{"id": 1}],
            [{"id": 2}],
            False,
            [{"id": 1}, {"id": 2}],
        ),
        # AND
        (
            "*",
            True,
            True,
            [{"id": 1}],
            [{"id": 2}],
            True,
            [{"id": 1}, {"id": 2}],
        ),
        (
            "*",
            True,
            False,
            [{"id": 1}],
            [{"id": 2}],
            False,
            [{"id": 1}, {"id": 2}],
        ),
        (
            "*",
            False,
            True,
            [{"id": 1}],
            [{"id": 2}],
            False,
            [{"id": 1}, {"id": 2}],
        ),
        (
            "*",
            False,
            False,
            [{"id": 1}],
            [{"id": 2}],
            False,
            [{"id": 1}, {"id": 2}],
        ),
        # And(Not())
        (
            "-",
            True,
            True,
            [{"id": 1}],
            [{"id": 2}],
            False,
            [{"id": 1}, {"id": 2}],
        ),
        (
            "-",
            True,
            False,
            [{"id": 1}],
            [{"id": 2}],
            True,
            [{"id": 1}, {"id": 2}],
        ),
        (
            "-",
            False,
            True,
            [{"id": 1}],
            [{"id": 2}],
            False,
            [{"id": 1}, {"id": 2}],
        ),
        (
            "-",
            False,
            False,
            [{"id": 1}],
            [{"id": 2}],
            False,
            [{"id": 1}, {"id": 2}],
        ),
    ],
)
def test_logical_operator_contract(
    op,
    a_val,
    b_val,
    a_ev,
    b_ev,
    expected_val,
    expected_ev,
):
    a = DummyOperator(a_val, a_ev)
    b = DummyOperator(b_val, b_ev)

    rule = OPS[op](a, b)

    result = rule.evaluate(None)

    assert result.value is expected_val
    assert result.evidence == expected_ev
