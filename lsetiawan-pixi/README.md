# Managing Python Projects with Pixi: From Zero to Reproducible Environments

Pixi is a fast, modern package and environment manager for Python (and beyond) that combines conda-forge and PyPI packages, per-project environments, and reproducible lock files in one tool. In 90 minutes, you'll go from an empty folder to a locked, task-automated, multi-environment project you could hand to anyone and have it just work.

## Learning goals

After the session, participants can:

1. Create a pixi project and describe the anatomy of `pixi.toml`
   (workspace, channels, platforms, dependencies, tasks).
2. Add conda-forge and PyPI (`--pypi`) dependencies to a project.
3. Run project code with `pixi run` and `pixi shell` — no manual
   environment activation.
4. Define tasks, including `depends-on` chains, to automate a workflow.
5. Explain the distinct roles of `pixi.toml` and `pixi.lock` and why both
   are committed.
6. Reproduce another person's project exactly from a committed lock file.
7. Create additional environments from features (e.g., a `dev` environment
   with pytest) and run commands in them with `-e`.
8. Embed pixi in a Python package's `pyproject.toml` via `[tool.pixi.*]`
   tables: standard `[project]` metadata stays the single source of truth
   for pip/uv users, the package installs editable, and
   `[project.optional-dependencies]` extras map automatically to pixi
   features.
9. Name the next steps beyond the session: multi-platform locking, CI with
   `setup-pixi`, `pixi global`, and `pixi init --import` migration from
   conda `environment.yml`.

## Schedule

| Time | Lesson | What you'll do |
| --- | --- | --- |
| 1:30–1:42 | [01 · Why pixi?](lessons/01-why-pixi.md) | Understand the motivation for pixi and how it compares to conda/pip/uv. |
| 1:42–2:05 | [02 · Your first project](lessons/02-first-project.md) | Create a pixi project and add your first dependencies. |
| 2:05–2:25 | [03 · Tasks & the lock file](lessons/03-tasks-and-lock.md) | Define tasks, chain them with `depends-on`, and understand `pixi.lock`. |
| 2:25–2:40 | [04 · Beyond one environment](lessons/04-multi-envs-and-pypi.md) | Add PyPI dependencies and create additional environments/features. |
| 2:40–2:53 | [05 · Pixi for package maintainers](lessons/05-pyproject-for-maintainers.md) | Embed pixi in a `pyproject.toml`-based package. |
| 2:53–3:00 | [06 · Going further](lessons/06-going-further.md) | Preview multi-platform locking, CI, `pixi global`, and migration paths. |

## Before the session

You'll run this tutorial on the NeuroHackademy JupyterHub, where pixi is
already installed and the curriculum repo is already in your home directory.

1. Sign in to the JupyterHub and start your server.
2. Open a terminal (**File ▸ New ▸ Terminal**).
3. Move into the repo and pull the latest changes:

```bash
cd ~/curriculum
git pull
```

4. Verify pixi is available:

```bash
pixi --version
```

If that prints a version, you're ready.

## Lessons

1. [01 · Why pixi?](lessons/01-why-pixi.md)
2. [02 · Your first project](lessons/02-first-project.md)
3. [03 · Tasks & the lock file](lessons/03-tasks-and-lock.md)
4. [04 · Beyond one environment](lessons/04-multi-envs-and-pypi.md)
5. [05 · Pixi for package maintainers](lessons/05-pyproject-for-maintainers.md)
6. [06 · Going further](lessons/06-going-further.md)
