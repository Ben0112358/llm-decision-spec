from llm_decision_spec.execution.context import Context


def make_context(events: list[dict]) -> Context:
    return Context(
        events=events,
        key_fn=lambda event: event["id"],
        datetime_fn=lambda event: event["datetime"],
    )
