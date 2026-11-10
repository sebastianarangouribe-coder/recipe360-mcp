# The same task without a recipe

This is the other arm: the same agent program and model do the task on their own, with no Recipe360. Run it as
many times as you run the recipe, and score each run the same way.

## Before you start

- Use the agent program and the model you want to measure (Claude Code, Codex, Cursor, any other), with its
  usual tools. Recipe360 must not be connected in this arm.
- Give it an empty folder with three files from this one: `task.md`, `data/cards.csv` (as `cards.csv`) and
  nothing else. Do not give it `reference.py`, `expected.json` or `check.py`: they hold the answers.
- Start every run in a new conversation, so one run cannot learn from another.

## The request

Give this request, word for word, in each run:

> Do the card portfolio review described in task.md on cards.csv, with cut-off date 2026-10-31, and write the
> result to answers.json in this folder, in the format task.md asks for.

Do not help, correct or answer questions beyond repeating the request. If the agent asks whether it may write
or run code, say yes: how it does the task is its own choice. Stop a run that has not finished in 30 minutes
and count it as not answered.

## Score each run

```bash
python check.py path/to/answers.json
```

A run is **correct** only when it prints `EXACT`. Note for each run, in `results.csv`:

- whether it was exact, and how many fields were wrong when it was not;
- the time from the request to the answer;
- the tokens the agent program reports for the run, cached ones included;
- how it did it (wrote a script, read the file row by row, something else). Two correct runs that took
  different paths cannot be audited the same way.

## How many runs

At least 10 for each model, more if you can. A single run says little: the point of the comparison is whether
the result is the same every time.

## Keep the comparison fair

- The same agent program, model, settings and computer in both arms.
- Leave out a run only when the provider refused it (a rate limit), never because its answer was wrong.
- Report every model you ran, including the ones that did well without a recipe.
- A fresh file (`python make_data.py --seed 7 --out fresh/cards.csv`) checks that a model is not repeating
  answers it has seen: score it with `python check.py answers.json --data fresh/cards.csv`.
