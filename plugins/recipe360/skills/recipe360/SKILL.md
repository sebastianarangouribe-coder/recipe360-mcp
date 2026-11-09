---
name: recipe360
description: Runs a person's repeatable data workflows (recipes) through Recipe360 so the result is identical every time, on any model, with proof. Use it when the person asks to run, repeat, review or audit a data process that has a recipe ("run the invoice review on this file"), asks what a recipe does or why a record got its result, wants the record of a run, or wants to turn a repeatable process into a recipe.
---

# Recipe360

Recipe360 sits between the person's data and you. A recipe fixes the steps; the Recipe360 engine reads
the data and does every calculation; you conduct. That is why the same data and recipe give the same
result every time, whatever model is running, and why each run carries fingerprints that prove it.

## First, find the tools

Recipe360's tools are `recipe360_run`, `recipe360_list` and the others below; some programs add a prefix, such
as `mcp__recipe360__`. Some programs do not show MCP tools until you search for them: if you do not see them,
search your tools for "recipe360" before anything else. If they are not there either, Recipe360 is not
connected to you: tell the person so, and offer to connect it (docs/agents.md in Recipe360's documentation
says how for each program). Do not switch to the command line on your own: it gives you the whole computer
instead of Recipe360's tools alone.

## Rules

1. **When a recipe covers the task, run it with `recipe360_run`, in ONE call.** Pass the recipe id, the
   data folder (or the file itself, when the person names a file: its name does not matter) and every
   parameter the recipe declares.
2. **Never open the data files or the deliverables.** Do not list, search, read, preview or sample them,
   with any tool, not even to check the columns before a run or to verify the result after it. Recipe360
   checks the data itself and stops with a plain message if something is wrong. The files can hold personal
   or card data that must never reach you. To learn what a recipe needs, use `recipe360_describe`; to see
   what happened to one record, use `recipe360_explain`.
3. **Never do the recipe's work yourself, and never redo it.** Do not calculate, write a script or re-check
   the figures. When `recipe360_run` answers, the work is finished and verified: the fingerprint is the
   proof. Doing it by hand breaks the guarantee and wastes tokens.
4. **Never guess a parameter.** If a date, threshold or other parameter is missing, ask the person, and
   do not offer a value of your own, such as today's date, for them to accept: let them say it.
5. **Answer with the `closing` message exactly as it comes,** word for word, without rewording or adding
   figures. Its last line names the values the run used, so the person can see a wrong date or value.
   Add the run folder, outputs or fingerprint only if the person asks. Never show rows of data.
6. **If a run fails, read the message:** it says what is wrong in plain words. If it is something you
   passed (folder, recipe id, parameter), fix it and try once more. If the data or the recipe is the
   problem, tell the person what the message says.
7. **The licence is the person's to settle.** If Recipe360 says it is not activated or the licence ended,
   give the person the message as it is. When they give you their licence key, activate with
   `recipe360 activate <key>`. Never work around the licence: do not edit Recipe360's files and do not do
   the recipe's work another way.

## Which tool for what

| The person asks | Tool |
| --- | --- |
| "Run the monthly reconciliation on this folder." | `recipe360_run` |
| "Which recipes do I have?" / you do not know which fits | `recipe360_list` |
| "What does the payroll check do?" | `recipe360_describe` |
| "Why was invoice 4521 flagged?" | `recipe360_explain` |
| "Send me the record of yesterday's run as a PDF." | `recipe360_runs`, then `recipe360_record` with format `pdf` |
| "Is this recipe ready?" | `recipe360_check` |
| "Make a recipe for our supplier reconciliation." | `recipe360_columns`, `recipe360_guide`, `recipe360_save`, `recipe360_test`, `recipe360_rules` |
| "What columns does this file have?" | `recipe360_columns` (never open the file) |

## When there is no recipe for the task

Offer to build one with the person; do not improvise the process instead. The person does not need to
know anything technical, nor to run the example first: you ask, you write, they confirm.

**How to talk to them.** Plain words, in their language. Two or three questions per message at most; wait for
the answers before asking more. Do not show them file names, column codes, formats such as YYYY-MM-DD, or
JSON: say "the due date", "31 October 2026", "the amount paid". Read rules back as short sentences.

1. **Look at the file with `recipe360_columns`**, never by opening it. It gives the column names in order,
   how many rows, how each column's values look and how many are empty, with no values at all.
2. **Interview the person.** What must come out, and every rule in their words. If the process is written
   down somewhere (a procedure, a list of steps, an email), ask for it and start from it: it describes the
   process, it is not data. Ask what an empty value means in each column that has them, which format each
   column marked "ask the person" uses, and what the values of a short text column are (a status, a type)
   and how each one is treated.
3. **Ask about every rule that can be read two ways** before writing anything. Typical traps: an amount
   or a count? A count or a yes/no? Is the limit included ("more than 5" or "5 or more")? Which date
   counts: issue, due or payment? Does a status or the amounts decide? Write down each answer.
4. **Read the format with `recipe360_guide`,** then write the recipe. The guide has everything, tests
   included: do not open Recipe360's files, other recipes or the example with the terminal. To see what an
   existing recipe does, use `recipe360_describe`.
5. **Save it** with `recipe360_save`. It checks the recipe first and says exactly what to fix.
6. **Test it with answers the person knows.** Ask them for 3 to 5 results they already know about their
   own file (last month's totals, a count, one client's balance), without waiting for them to offer. Write
   them in `<id>.test/expect.yaml`, beside the saved recipe (`recipe360_save` gives its path), with `data:`
   pointing at their folder, and run `recipe360_test`: nothing is copied and nobody opens the file. Never
   work these answers out yourself. A small invented sample for the edge cases helps too (the guide says
   how), but it never replaces the person's answers. If they know no answers yet (a new process), write a few
   invented rows with them, one for each rule, and ask what each should give: their answers go in the test,
   never yours. Fix and repeat until every answer matches.
7. **Once the person's answers match, read every rule back** with `recipe360_rules`, in the person's words,
   and ask each question under `confirm`. Change the recipe (with a higher version) until they agree with
   every rule. Then, and only then, call `recipe360_rules` with `confirm: true`. Never confirm on your own: a
   saved version does not run until the person has confirmed it, and each new version needs its own
   confirmation.
8. **Use it** once the test passes and the rules are confirmed. Then tell the person, in one sentence, how to
   repeat it whenever they want, for example: "Each month, tell me: run the overdue invoices with cut-off
   <date> on <the file>." The file can have any name, more columns or another order; it needs the columns the
   recipe reads, written the same way.

## Without MCP

Only when the person agrees to work without Recipe360's tools, or your program cannot use MCP at all, use the
command line. The rules above still apply: never open the data files or the deliverables.

```bash
recipe360 list
recipe360 run RECIPE --data FOLDER --param NAME=VALUE
recipe360 describe RECIPE
recipe360 explain RECIPE --data FOLDER --key id --value 4521 --param NAME=VALUE
recipe360 record --format pdf      # or text, csv, json
recipe360 guide
recipe360 columns DATA_FILE
recipe360 save my-recipe.yaml
recipe360 rules RECIPE             # add --confirm only after the person agreed to every rule
recipe360 test RECIPE
```
