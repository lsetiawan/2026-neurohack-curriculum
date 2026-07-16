# 06 · Going further

**Time:** 2:53–3:00 (7 min)

**Goals:** after this lesson you can:

- Install standalone CLI tools with `pixi global`.
- Migrate an existing conda project into pixi.
- Know where to keep learning.

## ⏩ Catch up

This lesson needs no project state; any terminal works:

```bash
cd ~/curriculum
```

## Tools without projects: pixi global

Everything so far lived inside a project's own `pixi.toml`. Some tools you want everywhere — a linter, a formatter, a CLI utility — with no project of their own.

```bash
pixi global install ruff
ruff --version
```

```
└── ruff: 0.15.20 (installed)
    └─ exposes: ruff
ruff 0.15.20
```

```bash
pixi global list
```

```
Global environments as specified in '~/.pixi/manifests/pixi-global.toml'
└── ruff: 0.15.20
    └─ exposes: ruff
```

- Each global tool gets its own isolated environment under `~/.pixi` — no dependency fights between tools.
- This replaces "I pip-installed a linter into my analysis env and broke it."

## Already have conda projects? Migrate.

Display-only — read, don't type. Say you have an existing `environment.yml`:

```yaml
name: old-analysis
channels: [conda-forge]
dependencies:
  - python=3.11
  - numpy
  - pip
  - pip:
      - tqdm
```

```bash
pixi init --import environment.yml my-migrated-project
```

Conda entries land in `[dependencies]`, `pip:` entries land in `[pypi-dependencies]`, and you get a lock file for free — no manual translation required.

## What you can now do

- [x] Create a pixi project and describe the anatomy of `pixi.toml` (workspace, channels, platforms, dependencies, tasks).
- [x] Add conda-forge and PyPI (`--pypi`) dependencies to a project.
- [x] Run project code with `pixi run` and `pixi shell` — no manual environment activation.
- [x] Define tasks, including `depends-on` chains, to automate a workflow.
- [x] Explain the distinct roles of `pixi.toml` and `pixi.lock` and why both are committed.
- [x] Reproduce another person's project exactly from a committed lock file.
- [x] Create additional environments from features (e.g., a `dev` environment with pytest) and run commands in them with `-e`.
- [x] Embed pixi in a Python package's `pyproject.toml` via `[tool.pixi.*]` tables: standard `[project]` metadata stays the single source of truth for pip/uv users, the package installs editable, and `[project.optional-dependencies]` extras map automatically to pixi features.
- [x] Name the next steps beyond the session: multi-platform locking, CI with `setup-pixi`, `pixi global`, and `pixi init --import` migration from conda `environment.yml`.

## Keep going

- Docs: [pixi.sh](https://pixi.sh)
- Multiple environments and features: [pixi.sh/latest/workspace/multi_environment](https://pixi.sh/latest/workspace/multi_environment/)
- CI: [setup-pixi](https://github.com/prefix-dev/setup-pixi) GitHub Action
- Community: [Prefix Discord](https://discord.gg/kKV8ZxyzY4)
- Template to copy: this repo's [`lsetiawan-pixi/example/`](../example/)

## Before you leave

The instructor will ask for one thing that clicked and one thing still fuzzy — think of yours now.
