# Recipe360

Recipe360 turns a process you repeat, such as reviewing invoices, checking applications or tracking deadlines,
into a recipe that Claude follows to the letter. The Recipe360 program does every calculation on your computer,
so the result is the same on every run and on any model, and every run leaves a record you can show an auditor.
Your data rows never reach the model.

This plugin connects Claude to the Recipe360 program on your computer and adds the Recipe360 skill, which tells
Claude when and how to use Recipe360's tools. It holds no code of its own.

## Before you install

Recipe360 is a separate program, installed and activated on your computer:

1. Install it with the one-line installer from https://recipe.pulso360.ai (macOS with Apple silicon, Linux or
   Windows).
2. Activate it with your licence key: `recipe360 activate R360-...`. A 15-day free trial is available; after it,
   Recipe360 costs USD 5 a month or USD 45 a year per computer.
3. Open a new terminal and check that `recipe360 --version` answers. The plugin starts Recipe360 by that name.

## Install

Add Recipe360 from Claude's plugin directory, or in Claude Code with:

```
/plugin install recipe360 --marketplace sebastianarangouribe-coder/recipe360-mcp
```

## Where it works

- **Claude Code** (the terminal, the IDE extensions and the desktop app's Code tab): yes.
- **Cowork**, when the session runs on your computer: yes.
- **Chat** on claude.ai, in the desktop app or on mobile: no, because chat does not start programs on your
  computer. In the Claude desktop app's chat, use the Recipe360 desktop extension instead, `recipe360.mcpb`,
  from this repository's [latest release](https://github.com/sebastianarangouribe-coder/recipe360-mcp/releases/latest).

If you connected Recipe360 to Claude Code by hand before, remove that connection and that skill so Claude does not
see Recipe360 twice: run `claude mcp remove recipe360 --scope user` and delete the folder
`~/.claude/skills/recipe360`.

## Use it

Ask Claude in plain words:

- "Run the invoice review on this file."
- "Why did card 42 get its decision?"
- "Send me the record of yesterday's run as a PDF."
- "Turn the monthly reconciliation I just described into a recipe."

## What it runs, reads and sends

- **Runs** one command, `recipe360 mcp`: the Recipe360 program you installed. It talks to Claude over standard
  input and output and listens on no port.
- **Reads** the data files or folders you name for a run, and its workspace (`~/.recipe360`).
- **Writes** only to its workspace: recipes and their history, run folders and records, settings, and a signing
  key if you create one.
- **Gives Claude** counts, fingerprints, folder names and fixed messages, never rows of data. What you and Claude
  say to each other goes to Anthropic under your plan's terms; Recipe360 does not see it.
- **Sends**, and nothing else:
  - the licence check: activating, renewing (about once a month) and deactivating contact
    https://recipe.pulso360.ai/licence/ with the licence key, a random installation id, a one-way fingerprint of
    the computer, the computer's name, and the Recipe360 version and operating system;
  - time stamps, only if you turn them on (`recipe360 timestamps on`): the sha256 fingerprint of each new run
    record goes to the time-stamping authority you choose, FreeTSA (https://freetsa.org) by default.

No data file, recipe, result, run record or conversation is ever sent, and Pulso 360 does not receive them.
The full data flow is in [Security and data flow](https://recipe.pulso360.ai/docs/security.md).

## Links

- Website and pricing: https://recipe.pulso360.ai
- Documentation: https://recipe.pulso360.ai/docs/
- Troubleshooting: https://recipe.pulso360.ai/docs/troubleshooting.md
- Privacy: https://recipe.pulso360.ai/privacy/
- Terms: https://recipe.pulso360.ai/terms/

## License

The files in this plugin folder (the skill, the configuration, this README and the icon) are licensed under the
Apache License 2.0, in [LICENSE](LICENSE). Recipe360 itself, the program this plugin starts, is not part of the
plugin: it is proprietary software, used under its own terms at https://recipe.pulso360.ai/terms/. The licence does not grant use
of the names Recipe360 or Pulso 360.

Recipe360 is produced by Sebastián Arango Uribe and commercialized by Pulso 360 S.A.S. (Bogotá, Colombia).
