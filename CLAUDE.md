# CLAUDE.md

## Project

nolegend — a pip-installable Python library that makes Plotly charts beautiful
by default, following Edward Tufte's principles. Also ships a Claude Code skill
(`SKILL.md`) that teaches the visualization workflow.

Package: `nolegend` (import as `import nolegend`).
Only runtime dependency: `plotly>=5.0`.

## Dev setup

```bash
uv sync                          # install deps
./scripts/install-hooks.sh       # install pre-commit hook
```

## Commands

```bash
uv run poe fix        # auto-format + lint fix
uv run poe lint       # ruff check (no fix)
uv run poe typecheck  # ty check
uv run poe test       # pytest
uv run poe check      # all checks (lint + typecheck parallel, then tests)
```

## Code layout

```
nolegend/
├── __init__.py     # public API, template auto-registration
├── template.py     # tufte + tufte_dark Plotly templates
├── colors.py       # palettes and spotlight technique
└── helpers.py      # range_frame, direct_label, sparkline, etc.
```

## Style

- ruff for linting and formatting (line-length 88, py310 target)
- ty for type checking
- See `pyproject.toml [tool.ruff.lint]` for the full rule set
- Tests go in `tests/`, pytest with coverage

## Design constraints

- px → go refinement workflow: always draft with Plotly Express first
- Hard ceiling of 5 colors per chart, all palettes colorblind-safe
- Minimal deps — no numpy, no pandas, no matplotlib
- Works with Polars DataFrames directly
- marimo-native: dark mode detection, `mo.ui.plotly()` patterns
