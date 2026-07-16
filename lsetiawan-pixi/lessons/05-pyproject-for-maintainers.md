# 05 · Pixi for package maintainers

**Time:** 2:40–2:53 (13 min)

**Goals:** after this lesson you can:

- Embed pixi in an installable package's `pyproject.toml` instead of a standalone `pixi.toml`.
- Say which tables belong to standard packaging and which belong to pixi.
- Prove the editable install works via a test environment derived from a standard `[project.optional-dependencies]` extra.

## ⏩ Catch up

This lesson is independent of every previous one — you can start here cold.

```bash
cd ~/curriculum
rm -rf scratch/pi-lib
```

## Analyses are projects; libraries are packages

Everything so far treated `scratch/monte-carlo` as a standalone analysis — it owns its own `pixi.toml`, and nobody outside this workshop needs to `pip install` it. If you maintain an installable package instead, you already have a `pyproject.toml`: pip reads it, uv reads it, your CI reads it, and if you publish, PyPI reads it too.

Pixi does not ask you to replace that file with a second manifest. It moves in *alongside* your existing metadata, under `[tool.pixi.*]` — one file, read by every tool in your stack.

> 💭 **Think:** What in your `pyproject.toml` do pip, uv, AND your CI all rely on today? What would go wrong if you duplicated it into a second manifest?

## One file, two audiences

```bash
pixi init --format pyproject scratch/pi-lib
cd scratch/pi-lib
cat pyproject.toml
ls -R
```

```toml
[project]
authors = [{name = "Landung 'Don' Setiawan", email = "landungs@uw.edu"}]
dependencies = []
name = "pi-lib"
requires-python = ">= 3.11"
version = "0.1.0"

[build-system]
build-backend = "hatchling.build"
requires = ["hatchling"]

[tool.pixi.workspace]
channels = ["conda-forge"]
platforms = ["osx-arm64"]

[tool.pixi.pypi-dependencies]
pi_lib = { path = ".", editable = true }

[tool.pixi.tasks]
```

```
pyproject.toml
src

./src:
pi_lib

./src/pi_lib:
__init__.py
```

`pixi init --format pyproject` also scaffolded the `src/pi_lib/` layout for you (empty `__init__.py` — we'll fill it in shortly). Three call-outs on the file itself:

- `[project]` is 100% standard packaging metadata — pip and uv keep reading it exactly as before. `requires-python` does double duty: it's also how pixi derives its own `python` dependency, so you don't restate the version constraint anywhere else.
- `[build-system]` defaults to `hatchling` — pixi didn't invent a new build backend, it uses the one the Python packaging ecosystem already standardized on.
- `[tool.pixi.*]` is pixi's own space, layered on top. The line to notice is `pi_lib = { path = ".", editable = true }` under `[tool.pixi.pypi-dependencies]` — pixi added *your own package* as an editable dependency of itself. Every pixi environment you define will have `pi_lib` importable straight from `src/`, no extra install step.

## Standard metadata stays the single source of truth

Edit `pyproject.toml`: inside the existing `[project]` table, set

```toml
dependencies = ["numpy>=2.1"]
```

and add a new table:

```toml
[project.optional-dependencies]
test = ["pytest"]
```

Then:

```bash
pixi install
pixi workspace environment add test --feature test
pixi run -e test pytest --version
```

```
✔ The default environment has been installed.
```

```
✔ Added environment test
```

```
pytest 9.1.1
```

Pixi read `[project.dependencies]` and pulled `numpy` in as a PyPI dependency — no `[tool.pixi.dependencies]` entry needed. Then the maintainer superpower: it recognized the `test` extra you already had to declare for pip's sake and let you turn it into a pixi *feature* of the same name, with zero duplication. `pixi workspace environment add test --feature test` is what makes that feature runnable — it wires the feature into an environment pixi can actually solve and launch tasks in.

Display-only, no need to type these: `pixi add numpy` would instead pin a conda-forge `numpy` under `[tool.pixi.dependencies]`, which *overrides* the PyPI one of the same name — that's your escape hatch when you need a conda-only build (MKL, CUDA) without touching `[project.dependencies]`. And PEP 735 `[dependency-groups]` map to pixi features the same way `[project.optional-dependencies]` extras do — you'll use one in the stretch goal below.

> 💭 **Think:** For a library, why should runtime deps live in `[project.dependencies]` rather than `[tool.pixi.dependencies]`? Who consumes each table?

## Prove the editable install

`src/pi_lib/` and `tests/` already exist from the `pixi init` scaffold (create them yourself with `mkdir -p src/pi_lib tests` if your version of pixi didn't). Fill in `src/pi_lib/__init__.py`:

```python
"""pi_lib: tiny Monte Carlo pi estimation library (tutorial artifact)."""

import numpy as np


def estimate_pi(n_samples, rng=None):
    if rng is None:
        rng = np.random.default_rng(42)
    xy = rng.random((n_samples, 2))
    inside = (xy**2).sum(axis=1) <= 1.0
    return 4 * inside.mean()
```

and `tests/test_pi_lib.py`:

```python
from pi_lib import estimate_pi


def test_estimate_pi_converges():
    assert abs(estimate_pi(50_000) - 3.14159) < 0.05
```

Then:

```bash
pixi run -e test pytest -q
```

```
.                                                                        [100%]
1 passed in 2.73s
```

No `sys.path` hacks, no separate `pip install -e .` — the editable entry from section 4 makes your package importable in every pixi environment, so contributors get everything from `git clone` plus any `pixi run`.

## 🏋️ Your turn

*Give contributors a one-command test entry point: a `test` task that lives in the `test` feature.*

<details>
<summary>Hint</summary>

`pixi task add --help` — look at `--feature`.

</details>

<details>
<summary>Solution</summary>

```bash
pixi task add test "pytest -q" --feature test
pixi run test
```

```
✔ Added task `test`: pytest -q
```

```
✨ Pixi task (test in test): pytest -q
.                                                                        [100%]
1 passed in 0.06s
```

In this pixi version, `pixi run test` found the task and resolved straight to the `test` environment automatically — no `-e test` needed, because `test` is the only environment where the `test` task exists. If your pixi prompts you to disambiguate instead, be explicit: `pixi run -e test test`.

`pyproject.toml` now has the task nested under the feature:

```toml
[tool.pixi.feature.test.tasks]
test = "pytest -q"
```

</details>

## Debrief

- `[project]` stays 100% standard — pip users, uv users, and PyPI publishing are completely untouched by anything pixi adds.
- `[tool.pixi.*]` layers environments, tasks, and conda overrides on top, with ONE lock file covering every environment your contributors need.
- Extras map to features, so `pixi run -e test` mirrors `pip install .[test]` — one list to maintain, not two.

## 🚀 If you're ahead

**(a) A PEP 735 dependency group.** Add a `[dependency-groups]` table:

```toml
[dependency-groups]
dev = ["ruff"]
```

```bash
pixi workspace environment add dev --feature dev
pixi list -e dev
```

```
✔ Added environment dev
```

`pixi list -e dev` shows `ruff` resolved and installed alongside `numpy` and `pi_lib` — confirming the `dev` group became a real, runnable pixi feature exactly like the `test` extra did, with no `[tool.pixi.dependencies]` entry required.

**(b) Find your own package in the lock.**

```bash
pixi list -e test --sort-by name
```

```
pi_lib                                          323.77 MiB  pypi   ./
```

`pi_lib` shows up as a `pypi`-kind dependency sourced from `./` — that's pixi's editable install of your own package, sitting in the resolved environment right next to `pytest` and `numpy`. That size reflects the resolved editable source tree pixi tracks, not the actual size of your tiny library code.
