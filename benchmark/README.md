# A benchmark anyone can repeat

Does an AI assistant do the same data process right every time? This folder lets you measure it yourself, with
and without Recipe360, on data that is public and invented.

The task is a monthly review of a card portfolio: 400 cards, nine rules, 28 numbers to report
([task.md](task.md)). It is the process Recipe360's own example recipe runs.

| File | What it is |
| --- | --- |
| [task.md](task.md) | The task, as a person would brief it |
| [data/cards.csv](data/cards.csv) | The card file. Every value is invented |
| [make_data.py](make_data.py) | Writes that file from a seed, or a fresh one nobody has seen |
| [reference.py](reference.py) | The right answers, worked out in plain Python from the rules. It uses nothing from Recipe360 |
| [expected.json](expected.json) | What the reference gives for `data/cards.csv` |
| [check.py](check.py) | Scores one attempt: `EXACT` or the fields that are wrong |
| [with_recipe.py](with_recipe.py) | Does the task with Recipe360, several times, and scores every run |
| [without_recipe.md](without_recipe.md) | How to run the same task without a recipe, fairly |
| [results.csv](results.csv) | A table to fill in |

You need Python 3.9 or later. Nothing else to install for the reference and the scoring.

## With Recipe360

Install Recipe360 with its one-line installer from https://recipe.pulso360.ai. Its example runs without a
licence. Then:

```bash
python with_recipe.py --runs 10
```

Every run should print `EXACT` and the same delivery fingerprint, which for `data/cards.csv` and cut-off
2026-10-31 starts with `4989f850`. The script runs the recipe through the `recipe360` command; to measure an
agent program as well, ask your agent, with Recipe360 connected: "Run the card portfolio review on
`<folder>` with cut-off October 31, 2026", and compare the fingerprint in its answer.

## Without a recipe

Follow [without_recipe.md](without_recipe.md): the same agent program and model, the same request, a new
conversation each time, each `answers.json` scored with `check.py`.

## What to compare

- **Exact runs**, out of all the runs that were answered, in each arm.
- **The same result every time**: one fingerprint with the recipe; without it, how many different answers.
- **Time and tokens** per run, as your agent program reports them.

## What this is, and what it is not

- The reference is independent: it was written from the rules in `task.md`, not from Recipe360, and the two
  agree field by field. Read it; it is under 150 lines.
- Scoring is exact. A report that is nearly right is a wrong report.
- The figures on Recipe360's website (100% of runs correct with a recipe against 39% without, across ten models)
  come from Pulso 360's internal tests, whose data is not published. This benchmark is not those tests: it is a
  way to check the same question yourself. Your numbers will depend on the model, the agent program and the
  task.
- A fresh file shows that nothing is memorised:

  ```bash
  python make_data.py --seed 7 --cards 2000 --out fresh/cards.csv
  python with_recipe.py --data fresh/cards.csv --cutoff 2027-03-31      # a file of your own needs a licence
  ```

## Check the benchmark itself

```bash
python -m pytest test_benchmark.py        # or: python test_benchmark.py
```

It checks that the generator still writes `data/cards.csv` byte for byte, that the reference still gives
`expected.json`, that the scoring catches a wrong field, and, when Recipe360 is installed, that the recipe is
exact.

The files in this folder are licensed under the Apache License 2.0 ([LICENSE](LICENSE)). Recipe360 itself is
proprietary software, used under its own terms at https://recipe.pulso360.ai/terms/.
