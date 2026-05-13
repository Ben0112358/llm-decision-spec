from llm_decision_spec.execution.context import Context


def make_context(transactions):
    return Context(transactions=transactions, key_fn=lambda tx: tx["id"])
