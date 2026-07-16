# Instructor run-sheet — Pixi tutorial (2026-07-17, 1:30–3:00pm)

This is the live-delivery run-sheet for the Pixi tutorial: timing, cut/stretch
decisions, a question bank, and the fixes for the stumbling points we expect.
It complements — and does not replace — the participant-facing lessons.

## Learning goals

Copied from `lsetiawan-pixi/README.md` (## Learning goals). **Keep these in
sync with the landing page** — if the goals change there, update this list
too.

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

## Timing & hard checkpoints

| Wall clock | Lesson | Hard checkpoint | If behind |
| --- | --- | --- | --- |
| 1:30–1:42 | [01 · Why pixi?](../lessons/01-why-pixi.md) | — | Trim discussion of the failure-modes table; the "watch" demo and setup check are non-negotiable. |
| 1:42–2:05 | [02 · Your first project](../lessons/02-first-project.md) | — | Let the 🚀 stretch (pixi tree / downgrade) go first. |
| 2:05–2:25 | [03 · Tasks & the lock file](../lessons/03-tasks-and-lock.md) | **At 2:10, Lesson 03 must have started** — else skip its platforms section ("One lock, many platforms") and its CI section ("The same trick in CI"). | Cut the CI walkthrough (display-only anyway) and the platforms section; keep tasks + lock file, which carry the core reproducibility goal. |
| 2:25–2:40 | [04 · Beyond one environment](../lessons/04-multi-envs-and-pypi.md) | **At 2:30, Lesson 04 must have started** — else demo the dev-env commands from the projector instead of hands-on. | Switch straight to projector demo of `pixi add --feature dev` / `pixi workspace environment add`; skip the PyPI hands-on and just show the toml diff. |
| 2:40–2:53 | [05 · Pixi for package maintainers](../lessons/05-pyproject-for-maintainers.md) | **At 2:45, Lesson 05 must have started** — else run it display-only from the projector (the pyproject anatomy still lands as a demo). | Narrate the `pyproject.toml` anatomy and the editable-install proof from the projector; don't wait for everyone's `scratch/pi-lib` to catch up. |
| 2:53–3:00 | [06 · Going further](../lessons/06-going-further.md) | **At 2:55, jump to Lesson 06's recap ("What you can now do") no matter what.** | Skip `pixi global` and migration demos entirely; land on the checklist recap and the two closing questions. |

## Cut list & stretch list

**Cut, in this order, if the clock is against us:**

1. Lesson 06 `pixi global` live demo — point at the page instead of typing it.
2. Lesson 03 CI walkthrough (`.github/workflows/pixi-tutorial-example.yml`) —
   it's display-only already, so cut the narration time, not the concept.
3. Lesson 05 hands-on → switch to instructor-driven display-only.
4. Lesson 04 PyPI section hands-on → show the `pixi.toml` diff (the new
   `[pypi-dependencies]` table) on screen instead of having everyone type it.

**Stretch, if we're ahead of schedule:**

- The 🚀 "If you're ahead" blocks in each lesson (pixi tree / downgrade in
  L02, task descriptions in L03, combined environments + pytest in L04,
  PEP 735 dependency groups in L05).
- Extra roam-and-help time during "Your turn" blocks.

## Question bank

Verbatim 💭 **Think** prompts per lesson, each with expected answer(s) and
one common misconception + reframe, followed by four standing FAQ items.

### Lesson 01 · Why pixi? (2 prompts)

> 💭 **Think:** Have you ever inherited (or written!) a project you couldn't get running six months later? What broke?

- **Expected answer(s):** Dependency versions drifted (upstream releases changed behavior); no lock file existed so `pip install -r requirements.txt` re-solved to different versions; a named/shared conda env got mutated by an unrelated `pip install`; nobody recorded which Python version was used.
- **Misconception + reframe:** "It broke because I didn't pin versions carefully enough." Reframe: pinning by hand in a `requirements.txt` still isn't a lock file — it doesn't capture the full transitive dependency tree or build hashes. The fix isn't more discipline, it's a tool that writes the lock automatically.

> 💭 **Think:** What information must pixi have stored for every one of us to get bit-identical numbers just now?

- **Expected answer(s):** The exact package versions (and build strings) for numpy/matplotlib/python; the random seed used in the script; the conda-forge channel/platform the packages were solved for — i.e., everything now living in `pixi.lock` plus the script itself.
- **Misconception + reframe:** "It's just because we're all using the same script." Reframe: the same script with different numpy builds (e.g., different BLAS backends) can produce different floating-point results — bit-identical output requires the environment to match too, not just the code.

### Lesson 02 · Your first project (2 prompts)

> 💭 **Think:** Why does the manifest list `platforms` at all — why would a Linux machine care about locking for macOS?

- **Expected answer(s):** `platforms` tells pixi which machines the lock file must be solved for. A single `pixi.lock` can carry solved environments for several platforms at once, so a Linux machine "cares" the moment the project needs to also run correctly for macOS or Windows collaborators/CI runners.
- **Misconception + reframe:** "It's just metadata about my own machine." Reframe: it's a declaration of *who else* must be able to reproduce this project — add a platform and pixi solves and locks for it too, even though you never run code there yourself.

> 💭 **Think:** Which of the three belongs in version control: `pixi.toml`, `pixi.lock`, `.pixi/`? Why? (Answer lands in the debrief.)

- **Expected answer(s):** `pixi.toml` and `pixi.lock` — both committed. `.pixi/` is gitignored: it's the disposable, rebuildable environment on disk.
- **Misconception + reframe:** "Committing `.pixi/` would make setup faster for everyone." Reframe: `.pixi/` is platform- and machine-specific and can be rebuilt byte-for-bit from `pixi.toml` + `pixi.lock` in seconds — committing it bloats the repo and can't even be reused across platforms.

### Lesson 03 · Tasks & the lock file (2 prompts)

> 💭 **Think:** What project commands do you currently keep in a README, a Makefile, or your shell history?

- **Expected answer(s):** Things like "run the analysis," "run tests," "build docs," "format code" — commands that only work if you remember the right flags/working directory, and that a new contributor has to hunt for.
- **Misconception + reframe:** "A README is documentation enough — anyone can read it." Reframe: documentation can drift out of date silently; a `[tasks]` table is executable and versioned with the code, so `pixi run analyze` either works or the manifest itself is wrong (there's no separate doc to go stale).

> 💭 **Think:** Your collaborator runs this project on their machine next week. Which file guarantees they get YOUR versions — the manifest or the lock?

- **Expected answer(s):** The lock file (`pixi.lock`). The manifest only records ranges/intent; the lock records the exact solved versions and hashes.
- **Misconception + reframe:** "If the manifest has version ranges, that's specific enough." Reframe: a range like `numpy = ">=2.5.1,<3"` can resolve to different exact builds on different days unless a lock file pins it — ranges describe what's *allowed*, not what you *got*.

### Lesson 04 · Beyond one environment (2 prompts)

> 💭 **Think:** The default environment is what your users get. What belongs in it — and what have you been making users install that they never needed?

- **Expected answer(s):** Only runtime deps needed to use the project (e.g., numpy/matplotlib for the analysis script) belong in the default `[dependencies]`. Dev tooling — pytest, linters, IPython — has often been bundled in unnecessarily via a single shared conda `environment.yml`, forcing every installer to pull it down.
- **Misconception + reframe:** "More dependencies pre-installed is more convenient for everyone." Reframe: every extra dependency in the default environment is something CI, collaborators, and end users all pay for in install time and solver complexity — features let you make dev tooling opt-in without a second environment file to maintain.

> 💭 **Think:** Name one package you've only ever found on PyPI. Where does it fit in this project now?

- **Expected answer(s):** Any pure-Python package without a conda-forge build (participants will name real examples). It fits under `[pypi-dependencies]` via `pixi add --pypi <name>`, resolved by the same solver and locked in the same `pixi.lock` as the conda-forge packages.
- **Misconception + reframe:** "PyPI-only packages need a separate `requirements.txt` and a second install step." Reframe: pixi resolves conda-forge and PyPI dependencies together in one manifest and one lock file — there's no second tool or second lock to keep in sync.

### Lesson 05 · Pixi for package maintainers (2 prompts)

> 💭 **Think:** What in your `pyproject.toml` do pip, uv, AND your CI all rely on today? What would go wrong if you duplicated it into a second manifest?

- **Expected answer(s):** `[project]` metadata (name, version, dependencies, requires-python) and `[build-system]` — pip, uv, and CI all read these directly. Duplicating them into a second pixi-only manifest creates two sources of truth that can drift (e.g., a dependency bumped in one file but not the other), and pixi itself would no longer agree with what pip/uv installs.
- **Misconception + reframe:** "Pixi needs its own separate manifest, like conda's `environment.yml` alongside `setup.py`." Reframe: `[tool.pixi.*]` is designed to live inside the *existing* `pyproject.toml`, reading `[project]` directly — there's no second file to keep in sync.

> 💭 **Think:** For a library, why should runtime deps live in `[project.dependencies]` rather than `[tool.pixi.dependencies]`? Who consumes each table?

- **Expected answer(s):** `[project.dependencies]` is read by pip, uv, and PyPI when someone installs your package normally — that's the audience that matters for a library's actual users. `[tool.pixi.dependencies]` is pixi-only and would be invisible to anyone installing via pip/uv, and using it for a conda-forge override instead (e.g., MKL/CUDA builds) is the intended exception, not the default.
- **Misconception + reframe:** "Since I'm using pixi, my deps should go in the pixi table." Reframe: for a library meant to be `pip install`-able, `[tool.pixi.dependencies]` is an override mechanism (e.g., forcing a conda-forge build), not the primary place to declare what the package needs to run — that's still `[project.dependencies]`.

### Lesson 06 · Going further (0 prompts)

No 💭 Think prompts in this lesson — it's the 7-minute recap/preview lesson.

### Standing FAQ

- **"Isn't this just conda?"** → No. Pixi gives per-project environments (not shared/named), a lock file by default (not opt-in `conda env export`), bundled tasks in the manifest, no activation step (`pixi run`/`pixi shell`), and conda-forge + PyPI packages resolved in the same solve.
- **"Should I commit `pixi.lock`?"** → Yes, always. It IS the reproducibility artifact — without it, `pixi.toml`'s version ranges are just intent, not a guarantee.
- **"Why not `requirements.txt`?"** → No solver (pip resolves greedily, not a full SAT-style solve), no non-Python (conda-forge) dependencies, and no hash-locked transitive dependency tree by default.
- **"Do I have to abandon my `pyproject.toml` or build backend for pixi?"** → No. `[tool.pixi.*]` tables embed alongside your existing metadata; `[project]` and `[build-system]` stay authoritative for pip/uv/PyPI users.
- **"Isn't `uv` enough now — it has locking and isolated environments too?"** → For a pure-Python, PyPI-only project, `uv` is excellent — and pixi doesn't compete with it, it *uses* it: pixi resolves conda packages with `rattler` and PyPI packages with `uv` (one `resolvo` SAT solver), with PyPI resolved on top of the conda base into a single `pixi.lock`. The difference is scope: `uv` is PyPI-only, while pixi also resolves the conda-forge ecosystem — the Python interpreter itself plus compiled/system libraries that don't ship as working PyPI wheels (GDAL's C libs, CUDA, MKL). That conda-forge reach is exactly what the scientific stack needs. Advice: keep deps in the conda `[dependencies]` table where possible, use `[pypi-dependencies]` only for packages not on conda-forge. (This is the "But `uv` already does this?" aside in Lesson 01.)

## Common stumbling points

- **Ran pixi in the repo root, not `scratch/monte-carlo`.** The repo root has no manifest, so pixi commands there fail with a "could not find pixi.toml" / missing-manifest error. Fix: `cd scratch/monte-carlo` (or the relevant scratch dir) before running pixi commands.
- **Repo missing or out of date.** Point the participant back to the landing page's "Before the session" section: `cd ~/curriculum && git pull`.
- **Forgot `-e dev`.** `pytest` reports "not found" in the default environment — this is expected behavior and a good teachable moment about environments being opt-in, not a bug.
- **Stuck inside IPython during the Lesson 04 exercise.** The `repl` exercise deliberately ends inside an IPython session — prove it sees the project's packages (`import numpy; numpy.__version__`), then leave with `exit` (or Ctrl-D). Plain `pixi run ipython` without `-e repl` failing with "command not found" is the boundary check working — same teachable moment as the missing `-e dev` above, not a bug.
- **Ran Lesson 05 commands inside `scratch/monte-carlo` instead of `scratch/pi-lib`.** The catch-up box (`rm -rf scratch/pi-lib` then `pixi init --format pyproject scratch/pi-lib`) fixes it — Lesson 05 is intentionally independent of prior lessons.
- **TOML syntax error after hand-editing `pyproject.toml`.** Pixi prints a parse error with a line number — check brackets and quotes (common culprit: an unmatched `[` or a missing closing quote around a version string).

## Pre-session checklist

Run T-1 day (2026-07-16):

1. Start a **fresh** JupyterHub server and confirm `cd ~/curriculum && git pull` gives a clean, up-to-date repo.
2. Run every lesson's command blocks top-to-bottom on the hub: lessons 02→04 in sequence (they build on `scratch/monte-carlo`), then lesson 05 in its own `scratch/pi-lib`, including the catch-up boxes.
3. Confirm `cd lsetiawan-pixi/example && pixi run analyze` matches the transcripts shown in lessons 01 and 03.
4. Confirm the CI workflow (`.github/workflows/pixi-tutorial-example.yml`) is green on its last run.
5. Confirm the hub image has pixi installed (`pixi --version`) and the curriculum repo is present in participants' home directories.
6. The morning of 2026-07-17, post the hub link and a "start your server and `git pull`" reminder to participants.

## Feedback

- **(a) After Lesson 03, ~2:25:** one-minute temperature check — "fist-to-five: how's the pace?" Adjust using the cut list above based on the response.
- **(b) At 2:58:** two closing questions — "one thing that clicked?" / "one thing still fuzzy?" — collect verbally or via sticky notes.

Jot participant answers here after the session:

_(fill in after 2026-07-17)_

## Room logistics

- Project the slide deck ([`pixi-tutorial-slides.html`](../pixi-tutorial-slides.html)); the lesson pages mirror its content, so participants can follow along or catch up there.
- Keep [`commands.md`](commands.md) open on the demo machine — the copy-paste commands for each 🏋️ exercise, keyed to slide numbers.
- Keep one healthy hub session open as the demo machine, separate from any session used for live troubleshooting.
- Co-instructor/helper roams the room during "Your turn" blocks to help participants who fall behind.
- Write the repo short-link on the board so participants can find it without hunting through chat.
