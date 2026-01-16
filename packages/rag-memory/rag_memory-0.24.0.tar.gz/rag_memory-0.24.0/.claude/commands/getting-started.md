---
description: Interactive guided tour of RAG Memory - learn concepts, capabilities, and setup step by step
argument-hint: ""
allowed-tools: ["Read", "Grep", "Glob", "Bash"]
---

# Getting Started with RAG Memory

## Goal

Guide the user through understanding RAG Memory and getting fully set up.

## Expected Outcomes

By the end of this guide, the user should:

1. **Understand the concepts** - What is RAG? Semantic search? Knowledge graphs? Why dual storage?
2. **Understand the tools and capabilities** - What can RAG Memory do? CLI commands, MCP tools, ingestion methods, search features
3. **Complete installation** - Docker services running, CLI available, services healthy
4. **Complete initial configuration** - Collections set up for their use cases, first documents ingested, first searches run

## Menu Structure

Present these options to the user:

**What would you like to learn first?**

1. **Understand the Concepts** - What is RAG? Semantic search? Knowledge graphs? Why do I care?
2. **Learn the Capabilities** - What can RAG Memory actually DO for me?
3. **Just Get Started** - Skip explanations, install and configure now
4. **Show Me the Commands** - I know what this is, just show me how to use it

**Type 1, 2, 3, or 4 to choose your path.**

## Detail Level

Before proceeding with their chosen path, ask:

**How much detail do you want?**

1. **Quick Overview** (5-10 minutes) - Essential concepts only, minimal examples
2. **Standard Tutorial** (15-20 minutes) - Balanced explanations with key examples
3. **Deep Dive** (30+ minutes) - Comprehensive training with full details

**Type 1, 2, or 3**

Adjust depth of coverage based on their choice.

## How to Execute Each Path

1. Read `.reference/README.md` to discover what documentation exists
2. For the user's chosen path, find and read the relevant documentation
3. Present ONE step at a time - never dump multiple steps at once
4. Wait for user response before proceeding to the next step
5. Confirm each step completed successfully before moving on
6. After completing a path, offer to continue to another path or end

## Rules

- All content (examples, commands, explanations) comes from reading `.reference/`
- Search examples must be FULL QUESTIONS (semantic search), never keywords
- Never hardcode config paths - let the setup script show the actual path
- For installation: GIVE INSTRUCTIONS, don't run commands for the user (setup scripts, service commands)
- If user reports issues, read troubleshooting docs and guide them through solutions
