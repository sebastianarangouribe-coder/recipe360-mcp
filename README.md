# Recipe360 for Claude and MCP

Recipe360 turns a process you repeat (reviewing invoices, checking applications, tracking deadlines) into a
recipe your AI assistant follows to the letter. The code does every calculation on your computer, so the result
is the same on every run and on any model, and every run leaves a record you can show an auditor. Your data
stays on your computer.

This repository holds no Recipe360 code: Recipe360 itself is installed and activated from
**https://recipe.pulso360.ai**. It publishes two ways to connect it to Claude:

- **The Recipe360 plugin**, for Claude Code and Cowork: [`plugins/recipe360`](plugins/recipe360). It adds the
  Recipe360 skill and starts the Recipe360 you installed.
- **recipe360.mcpb**, an [MCP Bundle](https://github.com/modelcontextprotocol/mcpb), for the chat in the Claude
  desktop app (and other MCP Bundle hosts).

It also holds [a benchmark anyone can repeat](benchmark): a public task, invented data, an independent reference
and exact scoring, to measure the same process with and without a recipe.

## Install

1. Install Recipe360 with its one-line installer from https://recipe.pulso360.ai and activate it with your
   licence key (`recipe360 activate R360-...`). A 15-day free trial is available.
2. Then, depending on where you use Claude:
   - **Claude Code or Cowork**: add the plugin from Claude's plugin directory, or in Claude Code run
     `/plugin install recipe360 --marketplace sebastianarangouribe-coder/recipe360-mcp`.
   - **Chat in the Claude desktop app**: download `recipe360.mcpb` from the [latest release](../../releases/latest)
     and open it. The Claude app shows an "Install" window; Recipe360's tools then appear in your conversations.

The plugin starts Recipe360 by name, `recipe360 mcp`. The bundle starts it by its full path,
`~/.local/bin/recipe360 mcp` (on Windows, `%USERPROFILE%\.local\bin\recipe360.exe mcp`).

## Learn more

- Website and pricing: https://recipe.pulso360.ai
- Documentation: https://recipe.pulso360.ai/docs/
- Security and data flow: https://recipe.pulso360.ai/docs/security.md
- Privacy: https://recipe.pulso360.ai/privacy/

In the MCP Registry as `ai.pulso360/recipe360`.

Recipe360 is produced by Sebastián Arango Uribe and commercialized by Pulso 360 S.A.S. (Bogotá, Colombia).
© 2026. All rights reserved.
