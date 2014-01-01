# API Contract Checker

Validate a small mock business API's paginated success and structured error responses.

Uses Python 3.10+ and its standard library only. No package installation, virtual
environment, external server, Redis, Celery, or network access is required.

## Run

```console
python -m contracts_lab --help
python -m contracts_lab examples/sample.json
python -m contracts_lab --check-fixtures fixtures/cases.jsonl
python generate_fixtures.py --count 20
python -m unittest discover -s tests -v
```

Run from this directory. The optional path defaults to `-`, which reads JSON from
stdin. Output is JSON or a fixture-check summary. Exit codes are 0 success,
1 file failure, and 2 invalid input. Examples and fixtures contain generated data.

Validates one deliberately small mock contract, not arbitrary Swagger/OpenAPI documents. Supported statuses are 200, 400, 404, 429, and 500. Success payloads have exactly items and next_cursor, ascending unique IDs, and nonblank names. A non-null cursor equals the last item ID. Error payloads contain exactly error with a lowercase code and nonblank message. No HTTP requests are made.

## Learning focus

The modeled progression into Python API clients, response validation, and contract tests. This is an independent concept exercise based on the modeled
roadmap. It makes no claim to be employer-owned or period-authentic production code.

## Structure

- `contracts_lab/core.py`: validated parsing, storage, or state transitions.
- `contracts_lab/cli.py`: JSON command interface.
- `contracts_lab/generate_fixtures.py`: original deterministic validation cases.
- `contracts_lab/fixture_check.py`: expected-output/error checks.
- `fixtures/cases.jsonl`: 389 generated cases, with explicit descriptions.
- `tests/`: independently selected boundaries and the complete corpus check.

Branches `feature/core`, `feature/cli`, `data/fixtures`, and `docs/usage` retain
snapshots; `main` contains the complete tool. Dates and provenance are also recorded
in TIMELINE.json. Many data cases share a scenario; they are not separate features.

Keep changes focused, use actual dates for new work, and add a regression test
for changed behavior. Licensed under [MIT](LICENSE).

[History and provenance](HISTORY.md).
