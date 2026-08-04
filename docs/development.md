# Development

Local setup, commands, and CI for `llm-decision-spec`.

## Constraints

- Python **3.12+** (see `pyproject.toml`).
- **Poetry** is the package manager. Use `poetry install --sync` to match the lockfile.
- Formatting and linting are enforced in CI. Run `black` and `flake8` before pushing.
- Agent behavior guidelines live in [`.cursorrules`](../.cursorrules) — not duplicated here.

## Local setup

```bash
poetry install --sync
```

To run inside the Poetry environment:

```bash
poetry run pytest -q
poetry run black .
poetry run flake8 src tests
```

## Commands

| Task | Command |
|------|---------|
| Install dependencies | `poetry install --sync` |
| Run all tests | `poetry run pytest -q` |
| Run one test file | `poetry run pytest tests/operators/test_logical.py -q` |
| Format | `poetry run black .` |
| Lint | `poetry run flake8 src tests` |

## CI workflows

| Workflow | File | Trigger | What it runs |
|----------|------|---------|--------------|
| Linting and testing | [`.github/workflows/main.yml`](../.github/workflows/main.yml) | Pull request | `black --check`, `flake8`, `pytest` |
| Security | [`.github/workflows/security.yml`](../.github/workflows/security.yml) | PR, push to `main`, weekly schedule | Gitleaks, Trivy, CodeQL, Opengrep, pip-audit |

Dependabot opens weekly grouped PRs for Python and GitHub Actions dependencies. Config: [`.github/dependabot.yml`](../.github/dependabot.yml).

## Project layout (quick reference)

```
src/llm_decision_spec/   # library source
tests/                   # mirrors src/ at first level + tests/utils/
docs/                    # architecture, domain, conventions (this tree)
```

## See also

- [conventions.md](conventions.md) — where to put new tests
- [README.md](README.md) — documentation index
- [`.cursorrules`](../.cursorrules) — agent working agreements
