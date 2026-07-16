# 03 · Tasks & the lock file

**Time:** 2:05–2:25 (20 min)

**Goals:** after this lesson you can:

- Define tasks in `pixi.toml`, including tasks that chain to other tasks.
- Explain exactly what `pixi.lock` records.
- Restore an environment from the lock file alone.
- Reproduce someone else's project bit-for-bit.
- Extend a project's locked platforms.

## ⏩ Catch up

```bash
cd ~/curriculum
rm -rf scratch/monte-carlo
pixi init scratch/monte-carlo
cd scratch/monte-carlo
pixi add python numpy matplotlib
cp ../../lsetiawan-pixi/example/analyze.py .
```

This recreates Lesson 02's end state from nothing — if you already have `scratch/monte-carlo` from last time, this is a safe reset, not required.

## Stop memorizing commands: tasks

```bash
pixi task add analyze "python analyze.py"
pixi task add quick "python analyze.py --samples 2000"
pixi run analyze
pixi run quick
```

```
✔ Added task `analyze`: python analyze.py
✔ Added task `quick`: python analyze.py --samples 2000
✨ Pixi task (analyze): python analyze.py
samples : 100,000
estimate: 3.150080
error   : 0.008487 (0.2702%)
wrote   : pi-estimate.png
✨ Pixi task (quick): python analyze.py --samples 2000
samples : 2,000
estimate: 3.138000
error   : 0.003593 (0.1144%)
wrote   : pi-estimate.png
```

`pixi.toml` now has a `[tasks]` table:

```toml
[tasks]
analyze = "python analyze.py"
quick = "python analyze.py --samples 2000"
```

Tasks ship *with* the project. The next person who clones this repo runs `pixi run analyze` — they never have to read a README, hunt through your shell history, or reverse-engineer a Makefile to find the right invocation.

> 💭 **Think:** What project commands do you currently keep in a README, a Makefile, or your shell history?

## What the lock file actually is

```bash
grep -m 1 -A 5 "/numpy-" pixi.lock
wc -l pixi.lock pixi.toml
```

```
      - conda: https://conda.anaconda.org/conda-forge/osx-arm64/numpy-2.5.1-py314hb79c6fa_0.conda
  sha256: 3aa853ec05e6fe6b660be354fd05ab2a89b2e6cc6346612a6c75a18f38f62c3d
  md5: 3587914062d5537dde5fa8c2131cf624
  depends:
  - python
  - __osx >=11.0
    1187 pixi.lock
      15 pixi.toml
    1202 total
```

That's one package. `pixi.lock` records every package pixi's solver picked — the exact version, the exact build string, a content hash (`sha256`/`md5`), and its own dependencies — repeated per platform your project targets. Your manifest is ~15 lines of intent (`numpy = ">=2.5.1,<3"`); the lock is the complete, solved answer: 1,187 lines that pin down precisely what "the environment" means, byte for byte. (This was captured on macOS; a linux-64 hub session will show `linux-64` paths and build strings, and a different line count.)

## Delete your environment. On purpose.

```bash
rm -rf .pixi
pixi run analyze
```

```
✨ Pixi task (analyze): python analyze.py
samples : 100,000
estimate: 3.150080
error   : 0.008487 (0.2702%)
wrote   : pi-estimate.png
```

No error, no re-solve, no prompt. `pixi` silently reinstalled every package from `pixi.lock` and ran the task — same four lines as before. The environment on disk (`.pixi/`) is a *cache*, rebuildable at any time from `pixi.toml` + `pixi.lock`. Those two files are the project; `.pixi/` is disposable. This is exactly why `.pixi/` is gitignored, and why a dead laptop or a fresh hub session is a non-event.

> 💭 **Think:** Your collaborator runs this project on their machine next week. Which file guarantees they get YOUR versions — the manifest or the lock?

## Reproduce a stranger's project

Now do what the instructor did in Lesson 01 — reproduce someone else's environment without touching a version number yourself.

```bash
cd ../../lsetiawan-pixi/example
pixi run analyze
cd ../../scratch/monte-carlo
```

```
✨ Pixi task (analyze): python analyze.py
samples : 100,000
estimate: 3.150080
error   : 0.008487 (0.2702%)
wrote   : pi-estimate.png
```

That project carries a committed lock for `linux-64`, `osx-arm64`, and `win-64`. You just reproduced its author's environment exactly — same package versions, same build strings — and the identical `pixi run analyze` works whether you're on this Mac, a Linux hub session, or a Windows laptop.

## One lock, many platforms

```bash
pixi workspace platform add osx-arm64 win-64
wc -l pixi.lock
```

```
✔ Platform osx-arm64 is already present; nothing to do
✔ Added win-64
    2643 pixi.lock
```

(Before this command `pixi.lock` was 1,187 lines. `osx-arm64` was already this project's default platform, so pixi left it alone and only added `win-64` — your own output may differ if you started on a different platform. On the hub, whose default platform is `linux-64`, running this same command reports both `osx-arm64` and `win-64` as newly added — there's no "already present" line — and your starting `wc -l pixi.lock` count will differ from the macOS numbers shown here.) The line count more than doubled: the solver just worked out, and locked, a complete dependency set for a machine you don't own and have never run this code on.

## The same trick in CI

This repo already does this for real. `.github/workflows/pixi-tutorial-example.yml`:

```yaml
name: pixi-tutorial-example

on:
  push:
    paths:
      - "lsetiawan-pixi/example/**"
      - ".github/workflows/pixi-tutorial-example.yml"
  pull_request:
    paths:
      - "lsetiawan-pixi/example/**"
      - ".github/workflows/pixi-tutorial-example.yml"

jobs:
  reproduce:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Install pixi (locked install of the example environment)
        uses: prefix-dev/setup-pixi@v0.10.0
        with:
          manifest-path: lsetiawan-pixi/example/pixi.toml
          locked: true

      - name: Reproduce the analysis
        run: pixi run analyze
        working-directory: lsetiawan-pixi/example

      - name: Upload the figure
        uses: actions/upload-artifact@v4
        with:
          name: pi-estimate
          path: lsetiawan-pixi/example/pi-estimate.png
```

- `prefix-dev/setup-pixi` installs pixi itself on the runner; `locked: true` tells it to install *exactly* what's in `pixi.lock` and fail the job outright if the lock and manifest have drifted apart — no silent re-solve on someone else's machine.
- This exact file is what keeps `lsetiawan-pixi/example/` green in this repo, every time someone touches it.

No hands-on for this section — just read it.

## 🏋️ Your turn

*Create a task `full` that runs the complete analysis, but only after `quick` has passed as a fast sanity check (task chaining).*

<details>
<summary>Hint</summary>

```bash
pixi task add --help
```

Look for `--depends-on`.

</details>

<details>
<summary>Solution</summary>

```bash
pixi task add full "python analyze.py" --depends-on quick
pixi run full
```

```
✨ Pixi task (quick): python analyze.py --samples 2000
samples : 2,000
estimate: 3.138000
error   : 0.003593 (0.1144%)
wrote   : pi-estimate.png

✨ Pixi task (full): python analyze.py
samples : 100,000
estimate: 3.150080
error   : 0.008487 (0.2702%)
wrote   : pi-estimate.png
```

`pixi.toml` gained:

```toml
full = { cmd = "python analyze.py", depends-on = ["quick"] }
```

Both runs execute — `quick` first, then `full` — and `pixi run full` is the only command anyone needs to remember.

</details>

## Debrief

- Tasks make the project self-documenting — the commands live in `pixi.toml`, not in your head or a README.
- The lock file is the reproducibility contract: it pins exact versions and hashes per platform, and it's the thing you commit.
- Platforms + CI extend that contract to machines you don't own — `locked: true` turns "works on my machine" into an enforced guarantee.

## 🚀 If you're ahead

```bash
pixi task add --help
```

Give `quick` a `description` (re-add it with `--description "..."`, or edit `pixi.toml` directly to make it `quick = { cmd = "...", description = "..." }`). Then run:

```bash
pixi run
```

with no arguments, and see the task list pixi prints — including your new description.
