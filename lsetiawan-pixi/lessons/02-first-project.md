# 02 · Your first project

**Time:** 1:42–2:05 (23 min)

**Goals:** after this lesson you can:

- Create a pixi project from scratch.
- Read a `pixi.toml` and say what each table does.
- Add dependencies and explain what changed on disk.
- Explain what `pixi.lock` and `.pixi/` are for.
- Run code in the project environment without activating anything.

## ⏩ Catch up

```bash
cd ~/curriculum
```

This is the first hands-on lesson — as long as you're at the repo root, you're ready.

## Create the project

```bash
pixi init scratch/monte-carlo
cd scratch/monte-carlo
cat pixi.toml
```

```toml
[workspace]
authors = ["Landung 'Don' Setiawan <landungs@uw.edu>"]
channels = ["conda-forge"]
name = "monte-carlo"
platforms = ["osx-arm64"]
version = "0.1.0"

[tasks]

[dependencies]
```

(Your `authors` line will show whatever git identity is configured on your machine, and `platforms` will match whatever machine you ran `pixi init` on — this example was generated on macOS, so it shows `osx-arm64`; on the JupyterHub it will read `linux-64` instead, since the hub runs Linux. Everything else should match.)

Three tables, three jobs:

- **`[workspace]`** — the project's identity. `channels` says where packages come from (`conda-forge` here); `platforms` says what the lock file must cover.
- **`[tasks]`** — empty for now, we'll fill it in Lesson 03.
- **`[dependencies]`** — empty for now, that's next.

`pixi init` also dropped a `.gitignore` and `.gitattributes` in the folder — pixi assumes a real project lives in git from day one.

> 💭 **Think:** Why does the manifest list `platforms` at all — why would a Linux machine care about locking for macOS?

## Add dependencies

```bash
pixi add python numpy matplotlib
```

```
✔ Added python >=3.14.6,<3.15
✔ Added numpy >=2.5.1,<3
✔ Added matplotlib >=3.11.0,<4
```

(Exact version ranges depend on what's current on conda-forge the day you run this — don't worry if your numbers differ slightly.)

```bash
ls -a
cat pixi.toml
```

```
.  ..  .gitattributes  .gitignore  .pixi  pixi.lock  pixi.toml
```

```toml
[dependencies]
python = ">=3.14.6,<3.15"
numpy = ">=2.5.1,<3"
matplotlib = ">=3.11.0,<4"
```

Three new or changed artifacts, three different jobs:

- **`pixi.toml`** gained version *ranges* — this is your intent, loose enough to allow future patch releases.
- **`pixi.lock`** appeared — this is the exact, fully-solved set of package versions for every platform in `platforms`. Open it, scroll through it, close it. You will never hand-edit this file.
- **`.pixi/`** appeared — the actual environment on disk (interpreter, site-packages, everything). It's disposable and gitignored; delete it any time and `pixi run`/`pixi shell` rebuild it from the lock file.

> 💭 **Think:** Which of the three belongs in version control: `pixi.toml`, `pixi.lock`, `.pixi/`? Why? (Answer lands in the debrief.)

## Run without activating

```bash
pixi run python -V
pixi run python -c "import numpy; print(numpy.__version__)"
pixi shell   # then inside: python -V, exit
```

`pixi run <command>` executes a single command inside the project's environment, from anywhere inside the project tree — no activation, no shell state to forget. `pixi shell` is the exception: it drops you into an activated shell for the project (handy for a longer interactive session), and plain `exit` leaves it and returns you to your normal shell, unchanged. Either way, there is no global environment to remember to deactivate.

## Your first analysis

```bash
cp ../../lsetiawan-pixi/example/analyze.py .
pixi run python analyze.py
```

```
samples : 100,000
estimate: 3.150080
error   : 0.008487 (0.2702%)
wrote   : pi-estimate.png
```

Same script, same seed, same conda-forge channel as Lesson 01's demo — bit-identical output. Open `pi-estimate.png` from the file explorer to see the plot it wrote. The script itself is a ~50-line seeded Monte Carlo estimate of π; worth reading later, but not required right now.

## 🏋️ Your turn

*Add one more dependency of your choice from conda-forge (ideas: `rich`, `scipy`, `polars`) and prove you can import it. Then look at what changed in `pixi.toml` vs `pixi.lock`.*

<details>
<summary>Solution (using rich)</summary>

```bash
pixi add rich
pixi run python -c "import rich; rich.get_console().print('[bold green]it works[/]')"
git diff --no-index /dev/null pixi.toml   # or just: cat pixi.toml
```

```
✔ Added rich >=15.0.0,<16
it works
```

`pixi.toml` grows by exactly one line. `pixi.lock` grows by far more than one line — the lock captures rich's entire transitive dependency tree (its own dependencies, and theirs), not just the package you asked for.

</details>

## Debrief

- **Manifest (`pixi.toml`) = intent.** Version ranges, written by you, small and human-readable.
- **Lock (`pixi.lock`) = exact solution.** Auto-maintained by pixi every time dependencies change; never edited by hand.
- **`.pixi/` = disposable build product.** The environment itself, rebuildable from the lock file at any time. Commit the first two, never the third.

Nobody activated anything.

## 🚀 If you're ahead

```bash
pixi tree | head -n 20
```

Find where numpy's own dependencies (like `python` itself, or BLAS libraries) come from in the tree.

Then try downgrading on purpose:

```bash
pixi add "numpy<2"
```

Watch the solver refuse — with the `python` version already locked to something recent, no numpy `<2` release has a compatible build. Restore it:

```bash
pixi add "numpy>=2.1"
```
