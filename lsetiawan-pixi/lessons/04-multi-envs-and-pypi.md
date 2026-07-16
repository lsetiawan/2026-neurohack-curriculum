# 04 · Beyond one environment

**Time:** 2:25–2:40 (15 min)

**Goals:** after this lesson you can:

- Explain the difference between a feature and an environment.
- Add a dev environment without polluting the default one your users get.
- Run a task or command in a named environment with `-e`.
- Mix PyPI packages into a conda project without breaking reproducibility.

## ⏩ Catch up

```bash
cd ~/curriculum
rm -rf scratch/monte-carlo
pixi init scratch/monte-carlo
cd scratch/monte-carlo
pixi add python numpy matplotlib
cp ../../lsetiawan-pixi/example/analyze.py .
pixi task add analyze "python analyze.py"
pixi task add quick "python analyze.py --samples 2000"
```

This recreates Lesson 03's end state from nothing — if you already have `scratch/monte-carlo` from last time, this is a safe reset, not required.

## The problem with one environment

Your *users* need `numpy` and `matplotlib` to run `analyze.py` — nothing more. *You*, the person developing it, also want `pytest` to test it, maybe a linter, maybe an IPython shell to poke at it interactively. If all of that lands in one `[dependencies]` table, everyone who installs your project — CI, a collaborator, a user who just wants the figure — pulls down your entire dev toolchain too. Installs get slower, the dependency graph gets harder to solve, and the contract of "what does this project need to run" gets muddied with "what do I need to work on it."

Conda's traditional answer is a second environment file (`environment-dev.yml` alongside `environment.yml`) that you maintain by hand and that drifts the moment someone updates one and forgets the other. Pixi's answer stays inside one manifest and one lock file: declare **features** — named groups of extra dependencies — then compose them into **environments**. The default environment is still just `[dependencies]`; anything else is opt-in.

## A dev environment in two commands

```bash
pixi add --feature dev pytest
pixi workspace environment add dev --feature dev
```

The first command adds `pytest` to a new `dev` feature — not to the default environment:

```
✔ Added pytest
Added these only for feature: dev
```

A feature with no environment referencing it is inert, and pixi warns about exactly that the next time it parses the manifest — which happens immediately, on the second command, before that command's own fix takes effect:

```
 WARN Encountered 1 warning while parsing the manifest:
  ⚠ The feature 'dev' is defined but not used in any environment. Dependencies
  │ of unused features are not resolved or checked, and use wildcard (*)
  │ version specifiers by default, disregarding any set `pinning-strategy`
    ╭─[pixi.toml:17:10]
 16 │
 17 │ [feature.dev.dependencies]
    ·          ───
 18 │ pytest = "*"
    ╰────
  help: Remove the feature from the manifest or add it to an environment

✔ Added environment dev
```

(Exact line numbers in the warning depend on how many lines already precede `[feature.dev.dependencies]` in your `pixi.toml` — don't worry if yours differ.)

The second command fixes exactly that — it wires the `dev` feature into a `dev` environment. `pixi.toml` now has:

```toml
[feature.dev.dependencies]
pytest = "*"

[environments]
dev = ["dev"]
```

Now run the same tool in two different environments:

```bash
pixi run -e dev pytest --version
pixi list -e dev | head -n 8
pixi run pytest --version
```

In `dev`, it's there:

```
pytest 9.1.1
```

```
Environment: dev
Installed for: osx-arm64
Name                       Version      Build                      Size  Kind   Source
_openmp_mutex              4.5          7_kmp_llvm             8.13 KiB  conda  https://conda.anaconda.org/conda-forge
brotli                     1.2.0        h7d5ae5b_1            19.76 KiB  conda  https://conda.anaconda.org/conda-forge
brotli-bin                 1.2.0        hc919400_1            18.19 KiB  conda  https://conda.anaconda.org/conda-forge
bzip2                      1.0.8        hd037594_9           121.91 KiB  conda  https://conda.anaconda.org/conda-forge
ca-certificates            2026.6.17    hbd8a1cb_0           125.85 KiB  conda  https://conda.anaconda.org/conda-forge
```

(Captured on macOS — a linux-64 hub session will show `Installed for: linux-64` and Linux build strings instead.)

But without `-e dev`, pixi runs in the **default** environment — and pytest isn't there:

```
pytest: command not found

Available tasks:
	analyze
	quick
```

That failure is the point. The default environment is exactly what a user gets when they clone your project and run `pixi run analyze` — no `pytest`, no dev tooling, nothing you needed but they don't.

> 💭 **Think:** The default environment is what your users get. What belongs in it — and what have you been making users install that they never needed?

## PyPI packages in a conda project

Not every package lives on conda-forge. Pixi lets you add PyPI packages into the same manifest, resolved by the same solver, locked in the same file:

```bash
pixi add --pypi tqdm
pixi run python -c "import tqdm; print(tqdm.__version__)"
```

```
✔ Added tqdm >=4.68.4, <5
Added these as pypi-dependencies.
```

```
4.68.4
```

`pixi.toml` gained a new table, separate from the conda `[dependencies]`:

```toml
[pypi-dependencies]
tqdm = ">=4.68.4, <5"
```

- Prefer conda-forge for compiled or scientific-stack packages (numpy, matplotlib, scipy) — one solver reasons about binary compatibility across your whole environment, avoiding ABI mismatches.
- Reach for `--pypi` when a pure-Python package you want isn't on conda-forge at all.
- Both kinds land in the same `pixi.lock` — one file still pins your entire environment, conda and PyPI packages alike.

> 💭 **Think:** Name one package you've only ever found on PyPI. Where does it fit in this project now?

## 🏋️ Your turn

*Create a `repl` feature and environment containing `ipython`, launch it, and prove it can see the project's packages. Then confirm the **default** environment can't.*

<details>
<summary>Hint</summary>

Same two commands as the dev environment, new names; then `pixi run -e repl ipython`.

</details>

<details>
<summary>Solution</summary>

```bash
pixi add --feature repl ipython
pixi workspace environment add repl --feature repl
pixi run -e repl ipython
```

```
✔ Added ipython
Added these only for feature: repl
✔ Added environment repl
```

Inside IPython, prove the environment sees the project's packages:

```
In [1]: import numpy; numpy.__version__
Out[1]: '2.5.1'
```

Leave with `exit` — then check the boundary in the other direction: plain `pixi run ipython` (no `-e repl`) fails with *command not found*. IPython lives only in the `repl` environment; your users never install it.

</details>

## Debrief

- The default environment is your users' contract — keep it minimal; everything else is opt-in through features.
- An environment is one or more features (optionally plus `default`), and every environment you define is solved and locked in the same single `pixi.lock`.
- Conda and PyPI dependencies coexist in one manifest — you don't need a separate `requirements.txt` or a second solver.

## 🚀 If you're ahead

**(a) Combine features into one environment.** It's named `all` because it combines every feature you've defined so far — `dev` and `repl`:

```bash
pixi workspace environment add all --feature dev --feature repl
pixi list -e all
```

```
✔ Added environment all
```

`pixi list -e all` prints every package resolved for that environment — both `pytest` from the `dev` feature and `ipython` from the `repl` feature, solved together and installed side by side. `pixi.toml`'s `[environments]` table now reads:

```toml
[environments]
dev = ["dev"]
repl = ["repl"]
all = ["dev", "repl"]
```

**(b) Put that dev environment to work.** Create `test_analyze.py`:

```python
import numpy as np

from analyze import estimate_pi


def test_estimate_converges():
    rng = np.random.default_rng(42)
    _, _, running = estimate_pi(50_000, rng)
    assert abs(running[-1] - np.pi) < 0.05
```

Then run it in the environment that actually has pytest:

```bash
pixi run -e dev pytest -q
```

```
.                                                                        [100%]
1 passed in 7.08s
```
