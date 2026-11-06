# Recipe360 for MCP

Recipe360 turns a process you repeat (reviewing invoices, checking applications, tracking deadlines) into a
recipe your AI assistant follows to the letter. The code does every calculation on your computer, so the result
is the same on every run and on any model, and every run leaves a record you can show an auditor. Your data
stays on your computer.

This repository only publishes **recipe360.mcpb**, an [MCP Bundle](https://github.com/modelcontextprotocol/mcpb)
that connects the Claude desktop app (and other MCP Bundle hosts) to Recipe360 in one click. It holds no
Recipe360 code: Recipe360 itself is installed and activated from **https://recipe.pulso360.ai**.

## Install

1. Install Recipe360 with its one-line installer from https://recipe.pulso360.ai and activate it with your
   licence key (`recipe360 activate R360-...`). A 15-day free trial is available.
2. Download `recipe360.mcpb` from the [latest release](../../releases/latest) and open it. The Claude app shows
   an "Install" window; Recipe360's tools then appear in your conversations.

The bundle starts the Recipe360 you installed: `~/.local/bin/recipe360 mcp` (on Windows,
`%USERPROFILE%\.local\bin\recipe360.exe mcp`).

## Learn more

- Website and pricing: https://recipe.pulso360.ai
- Documentation: https://recipe.pulso360.ai/docs/
- Security and data flow: https://recipe.pulso360.ai/docs/security.md
- Privacy: https://recipe.pulso360.ai/privacy/

In the MCP Registry as `ai.pulso360/recipe360`.

Recipe360 is produced by Sebastián Arango Uribe and commercialized by Pulso 360 S.A.S. (Bogotá, Colombia).
© 2026. All rights reserved.
