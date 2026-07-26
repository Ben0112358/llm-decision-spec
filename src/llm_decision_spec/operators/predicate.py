"""Unified predicate evaluation skeleton for value-driven operators."""

from __future__ import annotations

from collections.abc import Callable
from typing import Any

from llm_decision_spec.expressions.base import Expr
from llm_decision_spec.expressions.evaluate import (
    eval_expr,
    is_missing,
    predicate_values,
)
from llm_decision_spec.operators.base import EvaluationResult
from llm_decision_spec.execution.context import Context
from datetime import datetime


def filter_events_by_predicate(
    context,
    *,
    left: Expr,
    right: Expr | None = None,
    match: Callable[[Any, Any], bool] | None = None,
    match_left: Callable[[Any], bool] | None = None,
) -> EvaluationResult:
    data = []
    for e in context.events:
        if match_left is not None:
            lv = eval_expr(left, e)
            if is_missing(lv):
                continue
            if match_left(lv):
                data.append(e)
            continue
        if match is None or right is None:
            raise ValueError("binary predicate requires right and match")
        vals = predicate_values(left, right, e)
        if vals is None:
            continue
        lv, rv = vals
        if match(lv, rv):
            data.append(e)
    return EvaluationResult(data=data)


def filter_events_by_str_binary(
    context,
    left: Expr,
    right: Expr,
    match: Callable[[str, str], bool],
) -> EvaluationResult:
    data = []
    for e in context.events:
        vals = predicate_values(left, right, e)
        if vals is None:
            continue
        lv, rv = vals
        if not isinstance(lv, str) or not isinstance(rv, str):
            continue
        if match(lv, rv):
            data.append(e)
    return EvaluationResult(data=data)


def filter_events_by_context_datetime(
    context, *, match: Callable[[dict, Context], bool]
) -> EvaluationResult:
    data = []
    for e in context.events:
        if match(e, context):
            data.append(e)
    return EvaluationResult(data=data)


def filter_events_by_event_datetime(
    context,
    *,
    right: Expr,
    match: Callable[[datetime, Any], bool],
) -> EvaluationResult:
    data = []

    for event in context.events:
        rv = eval_expr(right, event)

        if is_missing(rv):
            continue

        event_time = context.datetime(event)

        if match(event_time, rv):
            data.append(event)

    return EvaluationResult(data=data)
