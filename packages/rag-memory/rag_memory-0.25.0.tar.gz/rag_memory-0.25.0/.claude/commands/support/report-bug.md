---
description: Submit a bug report to the RAG Memory GitHub repository
argument-hint: "[brief bug description]"
allowed-tools: ["Bash", "AskUserQuestion"]
---

# Report Bug to GitHub

I'll help you submit a bug report to the RAG Memory repository using the GitHub CLI.

**CRITICAL INSTRUCTIONS:**
- **DO NOT investigate the codebase**
- **DO NOT read any source files**
- **DO NOT analyze or verify the bug**
- **DO NOT search for code**
- **ONLY collect information from the user and submit it**

---

## Step 1: Check GitHub CLI

First, verify you have the GitHub CLI installed:

```bash
gh --version
```

If the command fails, tell the user to install it from: https://cli.github.com/

---

## Step 2: Collect Bug Information

I need to ask you some questions to create the bug report. I will take your answers at face value and will NOT investigate or verify the bug.

Ask the user these questions ONE AT A TIME using AskUserQuestion:

1. **Bug Title** - A clear, concise title (e.g., "MCP server crashes when ingesting large PDFs")

2. **What happened?** - Describe the unexpected behavior you observed

3. **What did you expect to happen?** - Describe the expected behavior

4. **Steps to reproduce:**
   - Step 1:
   - Step 2:
   - Step 3:
   - etc.

5. **Environment** - Which component is affected?
   - Options: Frontend (React UI), Backend (FastAPI), MCP Server, CLI, Other

6. **Additional context** (optional):
   - Error messages (paste exact text)
   - Environment details (OS, browser if frontend, Python version if backend)
   - Anything else relevant

---

## Step 3: Create GitHub Issue

Once I have your answers, I'll create a GitHub issue with:
- Title from your brief description
- Description with all details you provided
- The `bug` label
- Link to the repository: `codingthefuturewithai/rag-memory`

I will format your answers into a clear bug report but will NOT add any technical analysis or code investigation.

---

## Let's Begin

Let me start by asking you the first question about the bug.
