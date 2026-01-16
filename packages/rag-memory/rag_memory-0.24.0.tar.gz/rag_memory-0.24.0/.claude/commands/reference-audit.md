---
description: Audit documentation directories to ensure all claims match actual source code
argument-hint: "[reference|docs] (default: both)"
allowed-tools: ["Read", "Grep", "Glob", "Bash", "Edit"]
---

# Reference Audit

## Critical Rule

**Explore the repository FIRST. Read documentation SECOND.**

Do NOT let documentation guide your exploration. You must independently discover what exists in this codebase, then compare with what's documented. If you only look for what documentation mentions, you will miss new components.

## Scope

- No argument → Audit both `.reference/` and `docs/`
- `reference` → Only `.reference/`
- `docs` → Only `docs/`

## Constraints

- You CAN edit files in `.reference/` and `docs/`
- You CANNOT edit code, `.claude/commands/`, `.claude/hooks/`, or settings
- README files are indexes only - never add detailed content to them

## Task

**Step 1: Explore the entire repository.**

Discover everything that exists - services, tools, commands, interfaces, configuration, scripts. Leave no directory unexplored. Build a complete mental model of what this project contains.

**Step 2: Read the documentation directories.**

Now read `.reference/` and/or `docs/` (based on scope). Understand what is currently documented.

**Step 3: Compare both directions.**

- For each documented claim: Does the code actually work that way?
- For each discovered component: Is it documented?

**Step 4: Fix gaps.**

Edit existing files or create new ones. Update README indexes if you create new files.

**Step 5: Report.**

What you discovered. What you fixed. What requires user decision.
