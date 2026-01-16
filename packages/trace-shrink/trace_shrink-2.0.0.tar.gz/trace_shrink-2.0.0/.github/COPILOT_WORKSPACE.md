# Copilot Workspace Instructions

This project uses `uv` for dependency management and `ruff` for linting. These notes help GitHub Copilot and other automated assistants understand how to run and check the code.

- Dependency management:
  - Use `uv` commands to run tools inside the project's virtual environment.
  - Example: `uv run pytest` to run tests, `uv run black` to format, `uv run ruff` to lint.
  - The project's virtual environment is present at `./list/` and can be used by `uv`.

- Linting:
  - This project uses `ruff` for linting and simple fixes.
  - Run: `uv run ruff check .` to run lint checks.
  - Run: `uv run ruff check --fix .` to automatically fix fixable issues.

- Formatting:
  - `black` is used for formatting. Run `uv run black .` or `uv run black <file>`.

- Running tests:
  - Use `uv run pytest` to run the full test suite.

- Environment details:
  - Python version and packages are managed via `uv` and the included virtualenv; avoid global installs when making changes.

If Copilot or other agents need to execute commands, prefer `uv run <tool>` so the correct virtual environment and dependencies are used.