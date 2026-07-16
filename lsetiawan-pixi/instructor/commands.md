# Instructor commands during exercises



## Slide 20

*Add one more dependency of your choice from conda-forge (ideas: rich, scipy, polars) and prove you can import it. Then look at what changed in pixi.toml vs pixi.lock.*

```
# before adding the dependency
cp pixi.toml pixi.lock /tmp/

pixi add rich
pixi run python -c "import rich; rich.get_console().print('[bold green]it works[/]')"

# the intent change — one colored line
git diff --no-index /tmp/pixi.toml pixi.toml

# the lock — show the scale first, then a taste
wc -l /tmp/pixi.lock pixi.lock
diff /tmp/pixi.lock pixi.lock | head -n 15
```



## Slide 30

*Create a task full that runs the complete analysis — but only after quick has passed as a fast sanity check (task chaining).*

```
pixi task add full "python analyze.py" --depends-on quick
pixi run full
```



## Slide 38

*Create a repl feature and environment containing ipython, launch it, and prove it can see the project's packages. Then confirm the **default** environment can't.*

```
pixi add --feature repl ipython
pixi workspace environment add repl --feature repl
pixi run -e repl ipython
```



## Slide 46

*Give contributors a one-command test entry point: a test task that lives in the test feature.*

```
pixi task add test "pytest -q" --feature test
pixi run test
```

