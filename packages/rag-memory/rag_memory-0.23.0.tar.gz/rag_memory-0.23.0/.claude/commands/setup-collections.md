---
description: Interactive wizard to scaffold RAG Memory collections based on your use cases
argument-hint: ""
allowed-tools: ["Read", "AskUserQuestion"]
---

# Setup Collections - RAG Memory Collection Wizard

You are helping a user set up their RAG Memory collections. Your goal is to understand their use cases and create well-organized collections that will serve them well.

## Critical Instructions

- **Use MCP tools directly** - Don't tell user to run commands, just create collections via `mcp__rag-memory__create_collection`
- **Ask questions first** - Understand their use cases before suggesting anything
- **One step at a time** - Don't overwhelm with options
- **Explain "why"** - Help them understand collection organization principles

---

## Step 1: Check Current State

First, check what collections already exist:

```
mcp__rag-memory__list_collections()
```

**If collections exist:**
- Show them what's there
- Ask: "You already have some collections. Would you like to:
  1. Add more collections for additional use cases
  2. Review and understand what you have
  3. Start fresh (I'll explain, won't delete anything)"
- [WAIT FOR RESPONSE]

**If no collections:**
- Say: "You don't have any collections yet. Let me help you set up the right ones for your use cases."
- Proceed to Step 2

---

## Step 2: Understand Use Cases

Ask the user about their intended use:

"What will you primarily use RAG Memory for? Select all that apply:

1. **Technical Documentation** - API docs, SDKs, library references, technical guides
2. **Meeting Notes** - Decisions, action items, discussion summaries
3. **Project Context** - Design docs, specs, architecture for specific projects
4. **Research** - Papers, articles, competitive analysis, exploration
5. **Company/Team Knowledge** - Policies, processes, internal documentation
6. **Personal Learning** - Notes, learnings, interests
7. **Something else** (describe it)

Type numbers separated by commas (e.g., '1, 3, 5') or describe your use case."

[WAIT FOR RESPONSE]

---

## Step 3: Gather Specifics

For each use case they selected, ask ONE follow-up question to customize the collection:

### For Technical Documentation (1):
"What kind of technical documentation?
- A specific library or framework (e.g., 'React', 'LangChain')
- Multiple libraries you work with regularly
- Internal APIs you're building
- General tech reference"

### For Project Context (3):
"What's the project name or codename? I'll create a dedicated collection like `project-{name}`."

### For Something Else (7):
"Tell me more about this use case:
- What content will you ingest? (URLs, files, text?)
- What questions will you ask?
- How would you categorize this domain?"

[WAIT FOR EACH RESPONSE before proceeding]

---

## Step 4: Design Collections

Based on their answers, design the collections. Follow these principles:

**Naming:**
- Lowercase with hyphens: `tech-docs`, `meeting-notes`, `project-alpha`
- Specific but not too narrow: `react-docs` not `react-hooks-usememo-docs`
- Avoid generic names: `my-stuff`, `general`, `misc`

**Domain (high-level category):**
- Engineering, Product, Marketing, Research, Personal, Organization, Project

**Domain Scope (what's in/out):**
- Be specific about boundaries
- Example: "Python standard library documentation only, not third-party packages"
- Example: "Team Alpha weekly standups and sprint retrospectives"

Present your recommendation:

"Based on what you've told me, here's what I recommend:

**Collection 1: `{name}`**
- Domain: {domain}
- Scope: {scope}
- For: {brief description of what goes here}

**Collection 2: `{name}`**
...

Does this look right? I can adjust names, domains, or scope before creating."

[WAIT FOR CONFIRMATION]

---

## Step 5: Create Collections

Once confirmed, create each collection:

```
mcp__rag-memory__create_collection(
    name="{name}",
    description="{description}",
    domain="{domain}",
    domain_scope="{scope}"
)
```

Report each success:
"Created `{name}` collection"

If any fail, explain why and offer to retry with adjustments.

---

## Step 6: Verify and Next Steps

After all collections are created, verify:

```
mcp__rag-memory__list_collections()
```

Show the user their new setup:

"Your collections are ready:

| Collection | Domain | Purpose |
|------------|--------|---------|
| {name} | {domain} | {brief} |
| ... | ... | ... |

**What's next?**
1. **Ingest content** - I can help you add documents, URLs, or files
2. **Learn search** - I can show you how to query your collections
3. **All set** - You're ready to go!

Which would you like?"

[WAIT FOR RESPONSE]

---

## Collection Templates Reference

Use these as starting points, but always customize based on user's specific needs:

| Use Case | Suggested Name | Domain | Example Scope |
|----------|---------------|--------|---------------|
| Tech Docs | `tech-docs` or `{lib}-docs` | Engineering | "API documentation and technical guides" |
| Meetings | `meeting-notes` | Knowledge Management | "Team meetings, decisions, and action items" |
| Project | `project-{name}` | Project | "Design docs and specs for {Project Name}" |
| Research | `research` or `{topic}-research` | Research | "Papers, articles, and analysis on {topic}" |
| Company | `company-docs` | Organization | "Internal policies and processes" |
| Personal | `personal` or `notes` | Personal | "Personal notes and learnings" |

---

## Principles to Communicate

When explaining collection organization, share these insights:

1. **Collections partition search** - When you search a collection, you only search documents in that collection. Separate domains = better relevance.

2. **Domain + Scope are immutable** - These can't be changed after creation, so get them right. Description can be updated.

3. **One domain per collection** - Don't mix meeting notes with API docs. Keep domains focused.

4. **You can link documents** - A document can exist in multiple collections if needed.

5. **Start narrow, expand later** - Better to have focused collections than a big dumping ground.

---

## Error Handling

**If collection already exists:**
"A collection named `{name}` already exists. Would you like to:
1. Use a different name (suggest: `{name}-2` or more descriptive)
2. Skip this one (it's already set up)
3. View what's in the existing collection"

**If MCP server not connected:**
"I can't connect to the RAG Memory server. Make sure:
1. The server is running (`rag status`)
2. I'm configured to use it (check MCP settings)

Would you like help troubleshooting?"
