# tpl – Template Puller CLI

`tpl` treats single-file Cookiecutter templates like versioned building blocks. Instead of copy/pasting snippets or maintaining giant boilerplate repos, point tpl at any Git tag (GitHub, Bitbucket, or a local directory), drop the rendered file into your project, and record the provenance in `.tpl-lock.toml`. When a new tag ships, `tpl upgrade` tells you exactly what changed and keeps your tweaks safe.

> **Install note:** The PyPI package is published as `tpl-cli` (the CLI binary is still `tpl`). Install it via uv (`uv sync --package tpl-cli`) or pip (`pip install tpl-cli`).

## Why tpl?

- **Composable building blocks** – pull one template at a time or describe an entire starter kit in `tpl.toml`. Every block is still a normal Cookiecutter repo, with tags for versioning and hooks for customization.
- **Deterministic upgrades** – tpl stores the source URL, tag, entry file, checksum, and context for every managed file. Upgrades re-render using the same context, detect local edits, and produce `.tpl-new` / `.tpl.diff` artifacts (or run `git merge-file` when `--merge` is set).
- **Works offline** – reference `local:/path/to/repo` entries to test unreleased templates or run integration tests without hitting the network.
- **Zero vendor lock-in** – tpl orchestrates Git + Cookiecutter. Templates live wherever you keep them; tpl just fetches, renders, and tracks provenance.

```
# Pull a single template
uv run tpl pull gh:you/tpl-logging@v0.3.0 --file infra/logging.yaml=logging.yaml --set project_slug=my-app

# Compose an entire starter kit
uv run tpl compose gh:you/python-service@v1.2.0 --set project_name=my-app

# Reapply a local tpl.toml (hierarchical blocks + shared context)
uv run tpl apply --config tpl.toml --force

# Detect drift / upgrade safely
uv run tpl status
uv run tpl upgrade --merge
```

## Feature highlights

- **Single-file template pulls** – `tpl pull` grabs any tagged Cookiecutter repo and writes the requested entry file. Supports overrides via `--set key=value`.
- **Project composition** – `tpl compose gh:user/repo@tag` runs every block defined in `tpl.toml`, sharing context variables across blocks and supporting nested `kind = "project"` entries.
- **Local configs** – keep `tpl.toml` inside your repo and run `tpl apply --config tpl.toml` so teammates can rehydrate the same files without remembering commands.
- **Hierarchical layering** – include other project templates (Docker layer, CI layer, etc.) to build multi-stage starter kits.
- **Upgrade safety** – checksum tracking, optional three-way merge (`--merge`), and consistent conflict artifacts.
- **Private repo support** – authenticate with GitHub or Bitbucket tokens; tpl passes creds to Git via `GIT_ASKPASS` so secrets never hit disk.

## Commands at a glance

| Command | Purpose | Example |
| --- | --- | --- |
| `tpl pull` | Render a single file from a tagged template | `uv run tpl pull gh:you/tpl-logging@v0.3.0 --file infra/logging.yaml=logging.yaml` |
| `tpl compose` | Apply every block in a project template | `uv run tpl compose gh:you/python-service@v1.2.0 --set project_name=my-app` |
| `tpl apply` | Reapply a local `tpl.toml` config | `uv run tpl apply --config tpl.toml --set project_name=my-app` |
| `tpl status` | Show managed files and drift | `uv run tpl status` |
| `tpl upgrade` | Re-render and merge newer versions | `uv run tpl upgrade infra/logging.yaml --to v0.4.0 --merge` |

## Quick start (uv)

1. Install [uv](https://github.com/astral-sh/uv) and ensure Python 3.8+ exists (recommend 3.12): `uv python install 3.12`.
2. Sync dependencies (grab the `dev` extras for tooling):

   ```bash
   uv sync --extra dev
   ```

3. Run commands through uv to pick up the managed `.venv`:

   ```bash
   uv run tpl --help
   uv run pytest
   ```

   To run the test suite across multiple Python versions (if installed), use:

   ```bash
   tox
   ```

## Template authoring

tpl works with standard Cookiecutter repositories—no extra metadata files. A typical repo looks like this:

```
tpl-logging/
├── cookiecutter.json
└── {{cookiecutter.project_slug}}/
    └── logging.yaml
```

- `cookiecutter.json` declares the variables tpl can override via `--set key=value`.
- Everything inside `{{cookiecutter.project_slug}}/` renders normally. tpl copies whichever file you request through `--file dest=entry` or via the project configuration.
- Tag releases using normal Git tags (e.g., `git tag v0.3.0`). tpl records the tag you pulled so `tpl upgrade --to v0.4.0` knows which version to fetch next.
- You can keep additional files in the same repo and reference each one as a separate entry, which tpl will render in a single pass.
- If a local template directory has no Cookiecutter templated folder, tpl treats it as a raw file tree and copies files without rendering.

### Example templates in this repo

This repo includes a real, ready-to-use logging template at `examples/tpl-logging`. It renders two files:

- `logging_setup.py` — loads a `logging.toml` dictConfig, writes all levels to a daily-rotated file under `platformdirs`, and tunes Rich console output.
- `logging.toml` — the config (daily rotation, 7-day retention, INFO console default).

Pull it with a local repo spec (any tag label works for local):

```bash
uv run tpl pull local:examples/tpl-logging@v0.1.0 \
  --file logging/logging_setup.py=logging_setup.py \
  --file logging/logging.toml=logging.toml
```

Note: `local:` paths now work even if the directory is not a git repo (you can omit the @version in that case). If you want `tpl upgrade` to discover versions, initialize a git repo and add tags.

Wire it into a Typer app with `-v/-q` support:

```python
import typer

from logging_setup import setup_logging

app = typer.Typer()

@app.callback()
def main(
    verbose: int = typer.Option(0, "-v", count=True),
    quiet: int = typer.Option(0, "-q", count=True),
) -> None:
    setup_logging("my-app", verbose=verbose, quiet=quiet)
```

Additional example templates:

- `examples/tpl-justfile` — a pragmatic `justfile` with lint/format/typecheck/test targets.
- `examples/tpl-makefile` — the same targets, but as a `Makefile`.
- `examples/tpl-github-actions` — a pull_request workflow that runs tests, optionally via `just`.

Pull any of these as building blocks:

```bash
uv run tpl pull local:examples/tpl-justfile@v0.1.0 \
  --file justfile=justfile \
  --set project_slug=my-app \
  --set python_package=my_app
```

```bash
uv run tpl pull local:examples/tpl-makefile@v0.1.0 \
  --file Makefile=Makefile \
  --set project_slug=my-app \
  --set python_package=my_app
```

```bash
uv run tpl pull local:examples/tpl-github-actions@v0.1.0 \
  --file .github/workflows/tests.yml=.github/workflows/tests.yml \
  --set project_slug=my-app \
  --set python_version=3.12 \
  --set use_just=true \
  --set just_target=test
```

Bring them together for a fresh repo (or augment an existing one) by running multiple pulls:

```bash
uv run tpl pull local:examples/tpl-logging@v0.1.0 \
  --file logging/logging_setup.py=logging_setup.py \
  --file logging/logging.toml=logging.toml

uv run tpl pull local:examples/tpl-justfile@v0.1.0 \
  --file justfile=justfile \
  --set project_slug=my-app \
  --set python_package=my_app

uv run tpl pull local:examples/tpl-github-actions@v0.1.0 \
  --file .github/workflows/tests.yml=.github/workflows/tests.yml \
  --set project_slug=my-app \
  --set python_version=3.12 \
  --set use_just=true \
  --set just_target=test
```

You can also use a single project config to do the same. See `examples/tpl-starter/tpl.toml` and run:

```bash
uv run tpl apply --config examples/tpl-starter/tpl.toml \
  --set project_name=my-app \
  --set python_package=my_app
```

## Daily workflow

### A three-step workflow: create → pull → upgrade

#### 1. Author a template once

Build a standard Cookiecutter repo (`tpl-logging`):

```
tpl-logging/
├── cookiecutter.json
└── {{cookiecutter.project_slug}}/
    └── logging.yaml
```

`cookiecutter.json` might look like:

```json
{
  "project_slug": "logging",
  "environment": "staging"
}
```

…and `{{cookiecutter.project_slug}}/logging.yaml` can reference those values:

```yaml
version: 1
environment: {{ cookiecutter.environment }}
```

Tag releases with meaningful versions (`git tag v0.3.0`). tpl records the tag you pull so upgrades know where to fetch the next version.

#### 2. Pull it into another project

```bash
uv run tpl pull gh:you/tpl-logging@v0.3.0 \
  --file infra/logging.yaml=logging.yaml \
  --set environment=prod
```

tpl clones the tagged repo into `~/.tpl-cache`, renders it with the provided context, copies `logging.yaml` into your project, and stores the source/tag/context in `.tpl-lock.toml`. Now `tpl status` will track that file.

#### 3. Upgrade when a new tag ships

```bash
uv run tpl upgrade infra/logging.yaml --to v0.4.0
```

tpl re-renders the template, checks if the file changed locally, and either overwrites it or writes `<file>.tpl-new` plus a `<file>.tpl.diff`. tpl automatically attempts a Git-like merge when it detects local edits; pass `--no-merge` to skip the merge step and jump straight to conflict artifacts.

#### Pull multiple files from one template

Need more than one output? Repeat `--file DEST[=ENTRY]` for each extra file:

```bash
uv run tpl pull gh:you/tpl-logging@v0.3.0 \
  --file infra/logging.yaml=logging.yaml \
  --file infra/logging-dev.yaml=logging-dev.yaml \
  --set environment=dev
```

tpl renders the template once, copies both files, and records each entry in `.tpl-lock.toml` so upgrades work the same way.

#### Pull an entire template

Omit `--file` to copy every rendered file into your project root, preserving directories:

```bash
uv run tpl pull gh:you/python-starter@v1.0.0 --set project_slug=my-app
```

Each file is tracked in `.tpl-lock.toml` using its relative path.

### Check managed files

```bash
uv run tpl status
```

Outputs each tracked file plus its checksum status (`OK`, `MODIFIED`, `MISSING`).

### Create a starter tpl.toml

Generate a minimal `tpl.toml` in your project and fill in the blocks you want:

```bash
uv run tpl init
```

Use `--force` to overwrite an existing file and `--path` to write elsewhere.

### Compose a remote project template

Project templates ship a `tpl.toml`:

```toml
name = "python-service"
version = "0.2.0"

[context]
project_name = "my-service"

[[blocks]]
source = "gh:you/logging-block@v0.1.0"

[[blocks.files]]
path = "infra/logging.yaml"
entry = "logging.yaml"

[blocks.context]
environment = "prod"

[[blocks]]
kind = "project"
source = "gh:you/docker-layer@v0.3.0"
```

`kind = "project"` layers another template, letting you stack base scaffolds, Docker bits, CI pipelines, etc.
`[[blocks.files]]` describes each destination/entry pair you want to copy from the same template—add as many as you need.
If you omit `path`/`files` entirely for a block, tpl renders the whole template into your project root (preserving directories).

```bash
uv run tpl compose gh:you/python-service@v0.2.0 --set project_name=my-service
```

### Apply a local `tpl.toml`

Keep the same schema in your own repo to define reusable building blocks:

```toml
name = "demo"
version = "0.3.0"

[context]
project_name = "demo"

[[blocks]]
source = "gh:you/logging-block@v0.1.0"

[[blocks.files]]
path = "infra/logging.yaml"
entry = "logging.yaml"

[blocks.context]
environment = "prod"

[[blocks]]
source = "bb:team/docker-layer@v0.4.0"

[[blocks.files]]
path = "infra/docker-compose.yaml"
entry = "docker-compose.yaml"

[[blocks]]
source = "local:../templates/tpl-cache@v0.1.0"

[[blocks.files]]
path = "scripts/bootstrap.py"
entry = "scripts/bootstrap.py"
```

Add more `[[blocks.files]]` entries to copy additional files from the same template. tpl renders the template once per block and copies each requested output.

```bash
uv run tpl apply --config tpl.toml --set project_name=my-service
```

### Upgrade everything

```bash
uv run tpl upgrade
```

If a file’s checksum changed, tpl attempts a Git-style merge first. If it can’t merge cleanly (or you pass `--no-merge`), tpl writes `<file>.tpl-new` and `<file>.tpl.diff`. Target a single file with `uv run tpl upgrade path/to/file --to v0.3.0`.

## CLI reference

| Command | Description |
| --- | --- |
| `tpl pull <repo-spec> --file dest=entry [--file ...] [--set key=value]` | Render a Cookiecutter repo once, copy each requested entry into your project, and record provenance in `.tpl-lock.toml`. Supports GitHub (`gh:user/repo@tag`), Bitbucket (`bb:`), and `local:/path/to/repo@tag`. |
| `tpl status` | Show whether every managed file matches its stored checksum (`OK`, `MODIFIED`, `MISSING`). |
| `tpl upgrade <path> [--to tag] [--no-merge]` | Re-render a single managed file. tpl attempts to merge local edits automatically; add `--no-merge` to skip merging and always emit `<file>.tpl-new` / `.tpl.diff`. |
| `tpl compose <repo-spec> [--set key=value] [--force]` | Fetch a remote project template (`tpl.toml`), render every block, and write all configured files. |
| `tpl apply --config tpl.toml [--set key=value] [--force]` | Apply a local project configuration stored in your repo (same schema as a remote `tpl.toml`). |
| `tpl upgrade` (no path) | Reapply whichever project template is recorded in `.tpl-lock.toml` (remote or local). Honors `--no-merge`. |

## Project configuration (`tpl.toml`) reference

Minimal structure:

```toml
name = "demo"
version = "0.1.0"

[context]
project_name = "demo"

[[blocks]]
source = "gh:you/some-template@v1.0.0"

[[blocks.files]]
path = "src/config.yaml"    # Destination path in your project
entry = "config.yaml"        # File inside the rendered template (defaults to basename of path)
```

Key fields:

| Field | Where | Description |
| --- | --- | --- |
| `name`, `version` | root | Metadata only; helpful for humans/logging. |
| `[context]` | root | Default context values shared across every block. Overridden per block context or nested project templates. |
| `[[blocks]]` | root array | Each block references a Cookiecutter repo (GitHub, Bitbucket, or local). Set `kind = "project"` to include another `tpl.toml`. |
| `source` | block | Repo spec. Examples: `gh:you/template@v1.0.0`, `bb:team/repo@v0.4.0`, `local:../templates/logging@v0.3.0`. |
| `[[blocks.files]]` | block | Destination/entry pairs copied from that repo. Add multiple entries to copy multiple files. |
| `path` | block file | Destination inside your project. Directories are created automatically. |
| `entry` | block file | Relative file inside the rendered template. Defaults to `basename(path)` if omitted. |
| `[blocks.context]` or inline `context = { key = "value" }` | block | Optional overrides merged on top of the root context before rendering the block. Useful for per-file tweaks. |

## Repository specs

| Prefix | Example | Notes |
| --- | --- | --- |
| `gh:` / `github:` | `gh:openai/tpl-example@v0.1.0` | HTTPS clone via GitHub. Use `TPL_GITHUB_TOKEN`/`GITHUB_TOKEN` for private repos. |
| `bb:` / `bitbucket:` | `bb:team/repo@v1.2.0` | HTTPS clone via Bitbucket. Use `TPL_BITBUCKET_USERNAME` + `TPL_BITBUCKET_APP_PASSWORD`. |
| `local:` / `file:` | `local:../templates/logging@v0.1.0` | Absolute or relative path to a local git repo. Great for integration tests or unpublished templates. |

## Authentication & state

- **GitHub** – set `TPL_GITHUB_TOKEN` (or `GITHUB_TOKEN`). tpl authenticates as `x-access-token` automatically.
- **Bitbucket** – set `TPL_BITBUCKET_USERNAME` and `TPL_BITBUCKET_APP_PASSWORD`.
- **Cookiecutter state** – tpl writes replay/config data under `${HOME}/.tpl-state` by default (override with `TPL_COOKIECUTTER_STATE_DIR`). The directory is safe to delete if you need a clean slate.

Credentials feed Git via `GIT_ASKPASS`, so secrets never appear in lockfiles or logs.

## Automation & development

| Command | Description |
| --- | --- |
| `just fmt` | Run `ruff format`. |
| `just lint` / `just lint-fix` | Run `ruff check` (optionally with `--fix`). |
| `just typecheck` | Run `mypy tpl`. |
| `just test` | Run `pytest` (unit + integration). |
| `just check` | Run lint, typecheck, and tests sequentially. |
| `just precommit` | Run the full pre-commit stack. |

Install hooks once per machine:

```bash
uv run pre-commit install
```

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for the full workflow (uv setup, testing expectations, release process). CI runs Ruff, mypy, pre-commit, and pytest on every PR, and tagged commits on `main` auto-publish to PyPI.
