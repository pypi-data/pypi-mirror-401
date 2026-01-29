---
description: Capture content into RAG Memory with intelligent routing
argument-hint: "[url|file|text] [--to=collection] [--topic=topic] [--no-preview]"
allowed-tools:
  - mcp__rag-memory__list_collections
  - mcp__rag-memory__get_collection_info
  - mcp__rag-memory__analyze_website
  - mcp__rag-memory__ingest_url
  - mcp__rag-memory__ingest_file
  - mcp__rag-memory__ingest_directory
  - mcp__rag-memory__ingest_text
  - mcp__rag-memory__list_directory
  - Read
  - Glob
  - AskUserQuestion
---

# Capture to RAG Memory

Intelligently route and ingest content into the right collection.

## Critical Instructions

**NEVER ingest without approval** - Always ask for explicit user approval before calling any ingest tool.

**Approval is mandatory:** Use AskUserQuestion in Step 6 to present what will be ingested and wait for user confirmation before proceeding.

---

## Step 1: Check Collections (REQUIRED)

Always start by reading current collections:

```
mcp__rag-memory__list_collections()
```

**Why:** Never assume collection names. They may have been renamed, deleted, or new ones added.

---

## Step 2: Parse User Input

Determine what the user wants to capture:

**URL(s):**
- Single URL: `https://example.com`
- Multiple URLs: Space or comma separated

**File(s):**
- Single file path: `/path/to/file.txt`
- Directory: `/path/to/directory/` (will use list_directory first)

**Text:**
- Quoted text: `"This is some text to remember"`
- Unquoted text in arguments

**Overrides:**
- `--to=CollectionName` - Force specific collection (skip routing)
- `--topic="Topic Name"` - Provide explicit topic
- `--no-preview` - Skip website analysis for URLs (not recommended)

---

## Step 3: Route to Collection

### If user provided --to=CollectionName:
- Validate collection exists (check list from Step 1)
- If exists: Use it
- If not exists: Error and show available collections

### Otherwise, analyze content and recommend collection:

**Routing Logic:**

**IMPORTANT: Never hardcode collection names. Always discover them dynamically from list_collections().**

Analyze content and match against collection descriptions using semantic similarity:

**Content Pattern Matching:**

1. **External Documentation/Reference Content:**
   - URL contains: "docs", "documentation", "api", "reference", "manual", "guide"
   - User says: "official docs", "framework docs", "library reference"
   - Match to collections describing: "documentation", "reference", "external", "standards", "manuals"

2. **Project/Work-in-Progress Content:**
   - URL/file is: Internal domain, project repo, design doc
   - User says: "working on", "building", "project", "in-progress", "draft"
   - Match to collections describing: "project", "work-in-progress", "active work", "design", "exploration"

3. **Process/Procedure Content:**
   - Keywords: "SOP", "procedure", "checklist", "workflow", "process", "how we", "standard"
   - User says: "how we do X", "team process", "workflow"
   - Match to collections describing: "procedure", "process", "workflow", "SOP", "checklist", "standard"

4. **People/Relationship Content:**
   - Contains person names, "meeting with", "follow-up with"
   - User says: "about [person]", "their preferences", "context on"
   - Match to collections describing: "people", "person", "relationship", "contact", "teammate", "client"

5. **Business/Operations Content:**
   - Keywords: "invoice", "vendor", "client", "accounting", "finance", "strategy"
   - User says: "business", "ops", "financial"
   - Match to collections describing: "business", "finance", "accounting", "vendor", "operations"

6. **Unsorted/Temporary Content:**
   - User says: "not sure where", "misc", "random", "just save it"
   - Content is ambiguous or doesn't clearly match any category
   - Match to collections describing: "inbox", "unsorted", "temporary", "staging"
   - **Use as last resort**

**Routing Algorithm:**
1. Extract content semantics (URL patterns, keywords, user hints)
2. For each collection, calculate match score based on description similarity
3. If best match score > 80%: Use that collection
4. If best match score 50-80%: Ask user to choose between top 2-3 matches
5. If best match score < 50%: Default to "unsorted/inbox" type collection if exists, otherwise ask

**Confidence levels:**
- **High (>80%):** Announce decision and proceed: "Routing to [Collection] because [reason]"
- **Medium (50-80%):** Ask ONE question with 2-4 options + Inbox:
  ```
  This could fit multiple collections. Which is best?

  1. [Collection 1] - [Why it might fit]
  2. [Collection 2] - [Why it might fit]
  3. [Unsorted/Inbox Collection if exists] - Decide later

  Choose 1, 2, or 3:
  ```
- **Low (<50%):** Default to unsorted/inbox collection if exists, otherwise ask user

---

## Step 4: Extract/Ask for Topic

Topics improve quality scoring during ingest. RAG Memory provides `topic_relevance_score` when a topic is supplied.

**Strategy:**

1. **For official documentation URLs:**
   - Extract from URL/title: "https://react.dev" → topic="React framework"
   - Confidence: High, don't ask

2. **For project-specific content:**
   - If routing to Projects collection, ask: "What project is this for?"
   - Use answer as topic

3. **For general content:**
   - Only ask if content is clearly domain-specific
   - Otherwise omit topic (better than wrong topic)

4. **User-provided topic:**
   - If `--topic="..."` provided, use it directly

**NEVER guess topics** - extract confidently or ask. Wrong topics harm quality more than no topics.

---

## Step 5: Preview Large Operations (URLs with follow_links)

For URLs that will crawl multiple pages:

**ALWAYS preview using analyze_website():**

```
mcp__rag-memory__analyze_website(url=base_url)
```

Present results:
```
Website analysis:
- Total pages: [count]
- Estimated time: [X minutes]
- Estimated cost: ~$[amount]

Patterns found:
- /docs/api/* ([count] pages)
- /docs/guides/* ([count] pages)

Proceed with full crawl? (yes/no/preview-urls)
```

**If >20 pages:** Recommend targeted ingests by section instead of full crawl.

**Skip preview only if:** User explicitly passed `--no-preview` flag.

---

## Step 6: Ask for Explicit Approval (REQUIRED)

**BEFORE calling any ingest tool**, you MUST ask the user for explicit approval using AskUserQuestion.

Present a clear summary of what will be ingested:

```
Use AskUserQuestion to ask:

"Ready to ingest into RAG Memory:

Collection: [chosen_collection]
Content: [content_summary]
Topic: [topic or "None"]
[If URL with follow_links: "Will crawl up to X pages"]

Approve this ingest?"

Options:
1. Yes, proceed
2. No, cancel
3. Change collection
4. Change topic
```

**If user chooses 1 (Yes):** Proceed to Step 7 and call the ingest tool.

**If user chooses 2 (No):** Stop immediately. Report "❌ Ingest cancelled. No changes made to RAG Memory."

**If user chooses 3 (Change collection):** Go back to Step 3 and ask which collection.

**If user chooses 4 (Change topic):** Go back to Step 4 and ask for topic.

---

## Step 7: Call Ingest Tool (Only After Approval)

**ONLY call ingest after user explicitly approved in Step 6.**

Based on content type, call appropriate ingest tool:

**URL:**
```
mcp__rag-memory__ingest_url(
    url=url,
    collection_name=chosen_collection,
    topic=topic_or_null,
    follow_links=true_if_docs,
    max_pages=20,
    mode="ingest"
)
```

**File:**
```
mcp__rag-memory__ingest_file(
    file_path=path,
    collection_name=chosen_collection,
    topic=topic_or_null,
    mode="ingest"
)
```

**Directory:**
```
mcp__rag-memory__ingest_directory(
    directory_path=path,
    collection_name=chosen_collection,
    file_extensions=[".md", ".txt", ...],
    recursive=true_or_false,
    topic=topic_or_null,
    mode="ingest"
)
```

**Text:**
```
mcp__rag-memory__ingest_text(
    content=text,
    collection_name=chosen_collection,
    document_title="[Generated from first line or timestamp]",
    topic=topic_or_null,
    mode="ingest"
)
```

---

## Step 8: Report Results

After successful ingest:

```
✅ Ingested successfully

Collection: [collection_name]
Content: [summary]
Chunks: [num_chunks]
Topic: [topic or "None"]
Quality Score: [quality_score if available]
Topic Relevance: [topic_relevance_score if topic provided]

[Any warnings about large ingests, duplicate content, etc.]
```

**If user denied in Step 6:**
```
❌ Ingest cancelled by user

No changes were made to RAG Memory.
```

---

## Error Handling

**Collection doesn't exist:**
"Collection '[name]' not found. Available collections:
- [list collections]

Use /setup-collections to create new collections."

**File doesn't exist:**
"File '[path]' not found. Please check the path and try again."

**URL unreachable:**
"Could not access URL '[url]'. Status: [status_code]
Please verify the URL is correct and accessible."

**Duplicate content (mode="ingest"):**
"This content was already ingested into [collection].

Options:
- Use mode='reingest' to update it
- Leave it as-is (no action)
- Ingest into a different collection

What would you like to do?"

---

## Examples

### Example 1: Official Docs URL
```
User: /capture https://react.dev/reference

Claude:
✓ Reading collections...
✓ Analyzing URL...

Routing Decision:
- Collection: knowledge-and-reference
- Reason: Official framework documentation
- Topic: React framework
- Will follow links (max 20 pages)

✓ Analyzing website...
Found 15 pages in /reference section.
Estimated: 2-3 minutes, ~$0.10

Ready to ingest into RAG Memory:

Collection: knowledge-and-reference
Content: https://react.dev/reference (will crawl up to 15 pages)
Topic: React framework

Approve this ingest?
1. Yes, proceed
2. No, cancel
3. Change collection
4. Change topic

User: 1

✅ Ingested successfully

Collection: knowledge-and-reference
Content: React documentation (reference section)
Chunks: 234
Topic: React framework
Quality Score: 0.89
Topic Relevance: 0.94 (excellent match)
```

### Example 2: Ambiguous Content (Dynamic Routing)
```
User: /capture meeting-notes-2026-01-14.md

Claude:
✓ Reading collections...
Found: projects, people-and-relationships, practices-and-procedures, inbox-unsorted

✓ Reading file...
✓ Analyzing content...

This could fit multiple collections. Which is best?

1. **projects** - Match score: 65% (content mentions "sprint", "timeline")
2. **people-and-relationships** - Match score: 55% (content mentions person names)
3. **practices-and-procedures** - Match score: 45% (content describes a process)
4. **inbox-unsorted** - Decide later

Choose 1, 2, 3, or 4:

User: 1

Claude:
What project is this for? (This will be used as the topic)

User: Website redesign

Claude:
✓ Routing to: projects (65% match - project-related content)
✓ Topic: Website redesign

Ready to ingest into RAG Memory:

Collection: projects
Content: meeting-notes-2026-01-14.md
Topic: Website redesign

Approve this ingest?
1. Yes, proceed
2. No, cancel
3. Change collection
4. Change topic

User: 1
```

**Note:** This example shows how the agent dynamically discovers collections and calculates match scores based on content analysis and collection descriptions.

### Example 3: Forced Collection
```
User: /capture --to="practices-and-procedures" https://internal.company.com/onboarding-checklist

Claude:
✓ Reading collections...
✓ Collection 'practices-and-procedures' exists
✓ Forcing route to: practices-and-procedures

Ready to ingest into RAG Memory:

Collection: practices-and-procedures
Content: https://internal.company.com/onboarding-checklist
Topic: None

Approve this ingest?
1. Yes, proceed
2. No, cancel
3. Change collection
4. Change topic

User: 1

✅ Ingested successfully
```

---

## Principles

1. **Always read collections at runtime** - Never hardcode collection names
2. **Confidence-based questioning** - Only ask when truly ambiguous
3. **Topic extraction strategy** - Extract confidently or ask, never guess
4. **Preview large operations** - Always analyze websites before multi-page crawls
5. **Clear routing rationale** - Explain WHY you chose a collection
6. **Inbox as last resort** - Only use when genuinely ambiguous
7. **Always ask for approval** - Use AskUserQuestion in Step 6 before any ingest

---

## Anti-Patterns

❌ **Don't assume collection names** - Always call list_collections() first
❌ **Don't bypass routing** - Even if user says "just save it", determine collection first
❌ **Don't guess topics** - Wrong topics are worse than no topics
❌ **Don't skip website preview** - User needs to know scope before approving
❌ **Don't use Inbox by default** - It's for genuine edge cases only
