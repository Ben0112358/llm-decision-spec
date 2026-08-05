# llm-decision-spec

A Python library for defining **event-based features** as a composable AST. Work in progress.

The goal is a single intermediate representation that works for both offline batch evaluation and online serving — and that can serve as a structured target for LLM-assisted feature authoring.

## How it works

Features are built from three layers over a shared `Context` (a list of event dicts plus metadata):

| Layer | Role |
|-------|------|
| **Expr** | Project a value from one event (`Field`, `Add`, …) |
| **Operator** | Select events (`Gt`, `In`, `And`, `Before`, …) |
| **Reducer** | Aggregate selected events into a scalar (`Sum`, `Count`, …) |

```
Expr  →  Operator  →  Reducer
        (filter)      (aggregate)
```

**Example** — sum amounts for events where amount > 50 and currency is SEK or USD:

```python
from llm_decision_spec.expressions import Const, Field
from llm_decision_spec.operators.comparison import Gt
from llm_decision_spec.operators.membership import In
from llm_decision_spec.operators.logical import And
from llm_decision_spec.reducers.numeric import Sum

op = And(
    Gt(Field("amount"), Const(50)),
    In(Field("currency"), Const(frozenset({"SEK", "USD"}))),
)
result = Sum(Field("amount")).evaluate(op, context)
```

See [`tests/test_feature_pipeline.py`](tests/test_feature_pipeline.py) for a runnable version with fixtures.

## Quick start

**Requirements:** Python 3.12+, [Poetry](https://python-poetry.org/)

```bash
poetry install --sync
poetry run pytest -q
```

```bash
poetry run black .
poetry run flake8 src tests
```

## Project layout

```
src/llm_decision_spec/
├── core/          # Context, EvaluationResult
├── expressions/   # Expr AST
├── operators/     # Operator AST (selection)
├── utils/         # Shared operator helpers
└── reducers/      # Aggregation

tests/             # Mirrors src/ layout; see tests/conftest.py for fixtures
docs/              # Architecture, domain rules, conventions
```

## Documentation

Detailed design and contributor guidance live in [`docs/`](docs/README.md):

- [Architecture](docs/architecture.md) — pipeline, package map, layer boundaries
- [Domain](docs/domain.md) — events, missing values (`None`), temporal model
- [Conventions](docs/conventions.md) — how to extend Expr / Operator / Reducer
- [Development](docs/development.md) — CI, commands, workflows