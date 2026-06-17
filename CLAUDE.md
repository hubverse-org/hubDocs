# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this repo is

This repo generates the Hubverse documentation site at https://docs.hubverse.io/. It uses [Sphinx](https://www.sphinx-doc.org/) with the [Sphinx Book Theme](https://sphinx-book-theme.readthedocs.io/) and is built/hosted by [Read the Docs](https://readthedocs.org/). The site is rebuilt automatically on every push to `main`.

## Commands

```bash
# Install dependencies
uv pip install -r requirements/requirements.txt

# Live preview (rebuilds on file save, served at http://127.0.0.1:8000)
uv run sphinx-autobuild docs/source docs/_build/html

# Install pre-commit hooks (one-time setup)
uv run pre-commit install
```

### Managing dependencies

Never edit `requirements/requirements.txt` directly — it is auto-generated.

```bash
# Add a dependency
uv add <package>
uv pip compile pyproject.toml -o requirements/requirements.txt
uv pip install -r requirements/requirements.txt

# Remove a dependency
uv remove <package>
uv pip compile pyproject.toml -o requirements/requirements.txt
uv pip install -r requirements/requirements.txt
```

## Architecture

All documentation source lives in `docs/source/` as MyST Markdown files. The Sphinx config is at `docs/source/conf.py`.

**Key `conf.py` variables for versioning:**
- `schema_version` — the Hub schema version this doc release tracks (e.g. `v6.0.0`). Controls URLs in docson schema widgets throughout the docs.
- `schema_branch` — overridden automatically by Read the Docs on `main`; set manually when developing against an unreleased schema branch.

**Build pipeline:** Read the Docs installs `requirements/requirements.txt` (not `pyproject.toml`) as specified in `.readthedocs.yaml`. The `uv.lock` file is not used by Read the Docs.

**Known dependency constraint:** `myst-parser 5.1.0` requires `docutils<0.23`. Dependabot will periodically propose bumping docutils to `>=0.23` — reject those PRs until myst-parser lifts this upper bound.

## Versioning and releases

Documentation versions track Hub schema releases in the [`schemas` repo](https://github.com/hubverse-org/schemas). Release tags on this repo should match the `schemas` version number but without the `v` (e.g. schemas `v0.0.1` → hubDocs release `0.0.1`).

When preparing a release for a new schema version:
1. Branch from `main` using the convention `br-<version-number>`.
2. Update `schema_version` in `docs/source/conf.py`.
3. Optionally set `schema_branch` if the schema hasn't merged to `main` yet.
4. PR → merge → create GitHub release with the matching version tag.

## Style conventions

- New pages must be added to `docs/source/index.md` to appear in the table of contents.
- File names and directories: lowercase, hyphens (not underscores).
- Section/subsection titles: sentence case.
- Prefer native Markdown → HTML → custom CSS (`docs/_static/css/custom.css`) in that order.
- Images: `docs/source/images/`; non-Markdown assets: `docs/source/files/`.
- Use explicit anchors for cross-reference targets: `(my-target)=` above the heading.
