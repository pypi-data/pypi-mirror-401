# Development Instructions

## Running Tools

Use `uv` to run development tools:

```bash
uv run tox -p          # Run all tox environments in parallel
uv run tox -e tests    # Run tests only
uv run tox -e type-checking  # Run type checking only
uv run tox -e pre-commit     # Run pre-commit checks
```
