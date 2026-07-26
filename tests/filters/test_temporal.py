from datetime import datetime

from llm_decision_spec.expressions.base import Const
from llm_decision_spec.filters.temporal import (
    After,
    Before,
    StrictlyAfter,
    StrictlyBefore,
)
from llm_decision_spec.operators.logical import And

# Fixture event times (see conftest universe):
#   id 3 → 2026-01-01
#   id 1 → 2026-01-02 12:00
#   id 2 → 2026-01-03 12:00
T_MID = datetime(2026, 1, 2, 12, 0, 0)
T_LATE = datetime(2026, 1, 3, 12, 0, 0)
T_BETWEEN = datetime(2026, 1, 3, 0, 0, 0)


def ids(result):
    return sorted(e["id"] for e in result.data)


def test_strictly_before_open_right(context):
    """(-inf, a)  →  event_time < a"""
    op = StrictlyBefore(Const(T_BETWEEN))
    assert ids(op.evaluate(context)) == [1, 3]


def test_before_closed_right(context):
    """(-inf, a]  →  event_time <= a"""
    op = Before(Const(T_BETWEEN))
    assert ids(op.evaluate(context)) == [1, 3]


def test_after_open_left(context):
    """(a, inf)  →  event_time > a"""
    op = After(Const(T_MID))
    assert ids(op.evaluate(context)) == [2]


def test_strictly_after_closed_left(context):
    """[a, inf)  →  event_time >= a"""
    op = StrictlyAfter(Const(T_MID))
    assert ids(op.evaluate(context)) == [1, 2]


def test_open_interval(context):
    """(a, b)  →  a < event_time < b"""
    op = And(
        After(Const(T_MID)),
        StrictlyBefore(Const(T_LATE)),
    )
    assert ids(op.evaluate(context)) == []


def test_open_closed_interval(context):
    """(a, b]  →  a < event_time <= b"""
    op = And(
        After(Const(T_MID)),
        Before(Const(T_LATE)),
    )
    assert ids(op.evaluate(context)) == [2]


def test_closed_open_interval(context):
    """[a, b)  →  a <= event_time < b"""
    op = And(
        StrictlyAfter(Const(T_MID)),
        StrictlyBefore(Const(T_LATE)),
    )
    assert ids(op.evaluate(context)) == [1]


def test_closed_interval(context):
    """[a, b]  →  a <= event_time <= b"""
    op = And(
        StrictlyAfter(Const(T_MID)),
        Before(Const(T_LATE)),
    )
    assert ids(op.evaluate(context)) == [1, 2]


def test_boundary_included_only_on_closed_side(context):
    """At exactly a"""
    assert ids(Before(Const(T_MID)).evaluate(context)) == [1, 3]
    assert ids(StrictlyBefore(Const(T_MID)).evaluate(context)) == [3]
    assert ids(StrictlyAfter(Const(T_MID)).evaluate(context)) == [1, 2]
    assert ids(After(Const(T_MID)).evaluate(context)) == [2]
