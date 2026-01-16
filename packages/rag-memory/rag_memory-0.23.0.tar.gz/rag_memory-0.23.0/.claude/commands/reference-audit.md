---
description: Audit .reference/ directory to ensure all implementation claims match actual source code
argument-hint: ""
allowed-tools: ["Read", "Grep", "Glob", "Bash", "Edit"]
---

# Reference Audit - Bi-Directional Verification (Full-Stack)

I'm going to audit the .reference/ directory using a **two-way verification process** to ensure documentation matches reality and reality is fully documented.

This audit covers the **complete stack**: Frontend (React), Backend (FastAPI), and MCP Server.

---

## Project Structure Declaration

**CRITICAL:** This section defines the canonical project structure. Update this section when you reorganize directories.

### Top-Level Directories

**Frontend:**
- Primary: `frontend/src/rag/`
- If not found, check: `frontend/src/`, `ui/src/`, `web/src/`
- Fallback: ERROR - Frontend directory not found

**Backend:**
- Primary: `backend/app/`
- If not found, check: `backend/src/`, `api/`, `server/`
- Fallback: ERROR - Backend directory not found

**MCP Server:**
- Primary: `mcp-server/src/mcp/` (CURRENT STRUCTURE)
- If not found, check: `src/mcp/`, `mcp/src/`, `mcp/`
- Fallback: ERROR - MCP server directory not found

### Component Locations (Relative to Top-Level)

**Frontend Components:**
- React components: `{FRONTEND}/components/**/*.tsx`
- API layer: `{FRONTEND}/api.ts`, `{FRONTEND}/ragApi.ts`
- State: `{FRONTEND}/store.ts`
- Types: `{FRONTEND}/types.ts`

**Backend Endpoints:**
- Main router: `{BACKEND}/rag/router.py`
- MCP proxy: `{BACKEND}/rag/mcp_proxy.py`
- Models: `{BACKEND}/rag/models.py`

**MCP Server:**
- Tool definitions: `{MCP}/server.py`
- Tool implementations: `{MCP}/tools.py`
- HTTP routes: `{MCP}/http_routes.py`

### Pre-Audit Directory Verification

Before starting the audit, verify all top-level directories exist:

```bash
# Check frontend
ls frontend/src/rag/ || ls frontend/src/ || ls ui/src/ || echo "ERROR: Frontend not found"

# Check backend
ls backend/app/ || ls backend/src/ || ls api/ || echo "ERROR: Backend not found"

# Check MCP server
ls mcp-server/src/mcp/ || ls src/mcp/ || ls mcp/src/ || echo "ERROR: MCP server not found"
```

**If any directory is missing:**
1. Report which directory is missing
2. List alternatives checked
3. Tell user: "Project structure has changed. Please update the Project Structure Declaration section."
4. **STOP the audit** until user updates the section

---

## PHASE 1: Documentation → Implementation (Forward Verification)

### Step 1.1: Discover Documentation
- Read `.reference/README.md` (ONLY hardcoded path)
- List all documentation files
- Understand each file's purpose from README

### Step 1.2: Categorize Each Document

**Type A: Specification Documentation** (what is X?)
- Technical facts: ports, models, dimensions, counts, names
- Verification: Search/grep for values, verify accuracy

**Type B: Procedural Documentation** (how to do X?)
- Setup guides, deployment workflows, step-by-step procedures
- **Verification: MUST find and read implementation script line-by-line**
  - Discover script location (grep for keywords/prompts from doc)
  - Read main() execution flow completely
  - Compare EVERY step (order, prompts, defaults, outputs)
  - Bi-directional check:
    - Every doc step → exists in script
    - Every script step → exists in doc

**Type C: Component Documentation (NEW)** (architecture/API reference)
- Frontend component libraries
- Backend API endpoint references
- System architecture overviews
- **Verification: Compare documented components/endpoints to source code**
  - For ARCHITECTURE.md: Verify 3-tier structure, tech stack, database claims
  - For BACKEND_API.md: Compare endpoints to @router decorators, verify schemas
  - For FRONTEND_COMPONENTS.md: Compare components to .tsx files, verify exports

### Step 1.3: Verify and Fix
- For Type A: Search for claimed values, verify accuracy, fix errors
- For Type B: Full script comparison, fix ALL discrepancies
  - Wrong step order → fix
  - Missing prompts → add
  - Wrong defaults → fix
  - Wrong output → fix
- **For Type C: Compare components/endpoints to source code, fix discrepancies**
  - Component renamed/moved → update docs
  - Endpoint path changed → update docs
  - Missing components/endpoints → flag for addition
  - Stale descriptions → update

---

## PHASE 2: Implementation → Documentation (Reverse Discovery)

**PURPOSE:** Find undocumented or changed implementation that needs documentation.

### Step 2.1: Discover All User-Facing Implementation

**PRE-CHECK: Verify directory structure (from declaration above)**

**Search for setup/deployment scripts:**
```
glob: scripts/*.py
glob: deploy/**/*.py
grep: "def main" + "if __name__ == '__main__'"
```

**Search for deployment configurations:**
```
glob: docker-compose*.yml
glob: config/*.yaml, config/*.example.yaml
glob: deploy/docker/**
```

**Search for package configuration:**
```
read: pyproject.toml (entry points, scripts, dependencies)
```

**Search for CLI implementation:**
```
glob: mcp-server/src/cli_commands/*.py
grep: @click.command, @click.group
```

**Search for MCP implementation:**
```
glob: mcp-server/src/mcp/*.py  # or {MCP}/*.py after verification
grep: @mcp.tool
```

**Search for frontend components (NEW):**
```
# Use discovered FRONTEND directory from pre-check
glob: {FRONTEND}/components/**/*.tsx
read: {FRONTEND}/api.ts
read: {FRONTEND}/ragApi.ts
read: {FRONTEND}/store.ts
read: {FRONTEND}/types.ts
grep: "^export default function" {FRONTEND}/components/**/*.tsx
grep: "^export (async )?function" {FRONTEND}/api.ts {FRONTEND}/ragApi.ts
grep: "^export interface" {FRONTEND}/types.ts
```

**Search for backend endpoints (NEW):**
```
# Use discovered BACKEND directory from pre-check
read: {BACKEND}/rag/router.py
read: {BACKEND}/rag/mcp_proxy.py
grep: "^@router\\.(get|post|patch|delete)" {BACKEND}/rag/
```

**Search for backend models (NEW):**
```
read: {BACKEND}/rag/models.py
grep: "^class .*(Base):" {BACKEND}/rag/models.py
```

**Search for MCP HTTP routes (NEW):**
```
# Use discovered MCP directory from pre-check
read: {MCP}/http_routes.py
read: {MCP}/server.py
grep: "^async def .+_endpoint" {MCP}/http_routes.py
grep: "@mcp\\.custom_route" {MCP}/server.py
```

### Step 2.2: Create Implementation Inventory

List everything discovered:
- All Python scripts with main() functions
- All deployment configurations (dev, test, prod, cloud)
- All CLI command groups
- All MCP tools
- All entry points from pyproject.toml
- **All frontend components (NEW)**
  - Layout: AppLayout, TopBar, LeftNavigation, RightPanel, MainContent
  - Views: SearchView, DocumentsView
  - Core: ChatInput, MessageList, MessageBubble, CollectionBrowser, etc.
  - Modals: IngestionModal, ConfirmDeleteModal, LinkToCollectionModal, etc.
  - Visualizations: GraphVisualization, TimelineVisualization
- **All backend endpoints (NEW)**
  - Chat endpoints: /api/chat/stream, /api/chat/approve, /api/chat/reject, /api/chat/revise
  - Conversation endpoints: /api/conversations/* (CRUD operations)
  - Message endpoints: /api/conversations/{id}/messages
  - RAG Memory proxy endpoints: /api/rag-memory/* (collections, search, ingest, documents)
  - Starter prompts: /api/starter-prompts
  - Health check: /api/health
- **All backend models (NEW)**
  - Conversation, Message, StarterPrompt
- **All MCP HTTP routes (NEW)**
  - POST /api/ingest/file
  - PATCH /api/documents/review
  - POST /api/documents/manage-collection-link

### Step 2.3: Gap Analysis

**For each implementation found, check:**
- Is it documented in .reference/?
- If yes: Already verified in Phase 1
- If no: FLAG as potentially undocumented

**Enhanced gap categories (NEW):**
1. **Frontend Gaps** - Undocumented React components, API functions, state management
2. **Backend Gaps** - Undocumented endpoints, models
3. **MCP Gaps** - Undocumented HTTP routes (not just tools)
4. **Architecture Gaps** - Missing ARCHITECTURE.md, BACKEND_API.md, FRONTEND_COMPONENTS.md
5. **Stale Documentation** - Outdated paths, descriptions, component names

**Create gap report with priority levels:**

**CRITICAL Gaps:**
- Missing ARCHITECTURE.md (system overview)
- Missing BACKEND_API.md (API reference)
- Missing FRONTEND_COMPONENTS.md (component library)

**HIGH Gaps:**
- MCP HTTP routes not documented in MCP_GUIDE.md
- New major components/endpoints added recently

**MEDIUM Gaps:**
- Individual undocumented components
- Alternative access methods (HTTP vs MCP)

**LOW Gaps:**
- Rarely used features
- Development-only utilities

### Step 2.4: User Decision Points

For each gap found:
- Report: "Found X in implementation, not documented in .reference/"
- Categorize by layer (Frontend/Backend/MCP/Architecture)
- Assign priority (CRITICAL/HIGH/MEDIUM/LOW)
- Recommend: "Should be added to [FILE] → [SECTION]"
- If stale: Flag for removal/update
- **Do NOT auto-create documentation** - report gaps only

---

## Verification Standards

### ❌ INSUFFICIENT (Don't do this)
- "Grepped for port 54320, found it, declared verified"
- "Checked a few technical specs"
- "Sampled some values"
- "Glanced at component list"

### ✅ REQUIRED (Do this)
- "Read entire setup.py (1365 lines), found 18 steps, doc has 10 steps, fixed discrepancies"
- "Discovered 3 scripts in scripts/, verified all are documented"
- "Found docker-compose.dev.yml not documented, flagged for review"
- "Counted 28 React components, found 15 undocumented, flagged each with location and purpose"
- "Read router.py, found 15 endpoints, compared to BACKEND_API.md (doesn't exist), flagged as CRITICAL gap"

### For Type C (Component Documentation) Specifically:

**Frontend Components:**
- Component name matches file name
- Export type (default/named) correct
- Props interface documented (if TypeScript interface exists)
- State dependencies (useRagStore calls) identified
- Purpose description matches implementation

**Backend Endpoints:**
- HTTP method + path matches @router decorator
- Router prefix included in full path (e.g., /api/chat/stream not just /stream)
- Request/response schemas documented
- Docstring description accurate
- SSE vs REST correctly identified

**Backend Models:**
- Model name matches class name
- Table name documented
- All columns listed with types
- Relationships (foreign keys, cascades) documented
- Purpose matches actual usage

**MCP HTTP Routes:**
- Route registered via @mcp.custom_route (not just @mcp.tool)
- Method + path documented
- Purpose explained (why HTTP instead of MCP tool? Answer: browser file uploads, CORS)
- Parameters accepted
- Response format documented

---

## Completion Checklist

**Pre-Audit Verification:**
- [ ] Frontend directory found (primary or fallback)
- [ ] Backend directory found (primary or fallback)
- [ ] MCP server directory found (primary or fallback)
- [ ] If any fallback used, reported to user (structure may have changed)
- [ ] If any directory missing, STOPPED and requested user update

**Phase 1 - For each documented topic:**
- [ ] Categorized as Type A, Type B, or Type C
- [ ] Found implementation (searched, didn't assume path)
- [ ] Verified accuracy
- [ ] Fixed errors

**Phase 1 - For Type B (procedural) docs specifically:**
- [ ] Found implementation script
- [ ] Read main() function completely
- [ ] Listed all script steps
- [ ] Listed all doc steps
- [ ] Compared both directions
- [ ] Fixed all discrepancies (order, prompts, defaults, outputs)

**Phase 1 - For Type C (component) docs specifically:**
- [ ] Categorized as frontend/backend/MCP/architecture
- [ ] Found source files (glob + grep)
- [ ] Read component/function signatures
- [ ] Compared documented vs actual
- [ ] Fixed discrepancies (names, paths, descriptions)
- [ ] Verified cross-references (frontend API → backend endpoints)

**Phase 2 - Implementation discovery:**
- [ ] Searched for all scripts (glob scripts/*.py, deploy/**/*.py)
- [ ] Searched for all configs (glob docker-compose*, config/*)
- [ ] Searched for CLI commands (grep @click)
- [ ] Searched for MCP tools (grep @mcp.tool)
- [ ] **Searched for frontend components (glob *.tsx)**
- [ ] **Searched for backend endpoints (grep @router)**
- [ ] **Searched for backend models (grep class)**
- [ ] **Searched for MCP HTTP routes (grep endpoint)**
- [ ] Checked pyproject.toml entry points
- [ ] Created complete implementation inventory
- [ ] Compared inventory to documentation
- [ ] Flagged gaps by category (Frontend/Backend/MCP/Architecture)
- [ ] Assigned priority levels (CRITICAL/HIGH/MEDIUM/LOW)
- [ ] Flagged stale docs (outdated descriptions, wrong paths)

---

## Final Report Structure

1. **Pre-Audit Verification Results**
   - Directories found or missing
   - Fallbacks used (if any)
   - Structure changes detected

2. **Documentation Verification Results** (Phase 1)
   - Errors found and fixed per file
   - Type A verification: Technical specs checked
   - Type B verification: Scripts read, steps compared
   - **Type C verification (NEW): Components/endpoints compared to source**

3. **Implementation Discovery Results** (Phase 2)
   - Complete implementation inventory by layer:
     - Scripts and configs
     - CLI commands
     - MCP tools
     - **Frontend: 28 components, API layer, state management**
     - **Backend: 31 endpoints, 3 models**
     - **MCP HTTP: 3 custom REST endpoints**
   - Gap analysis by category:
     - **Frontend gaps** (components, API functions)
     - **Backend gaps** (endpoints, models)
     - **MCP gaps** (HTTP routes)
     - **Architecture gaps** (missing overview docs)
     - **Stale documentation** (outdated info)
   - Priority assignments (CRITICAL/HIGH/MEDIUM/LOW)
   - Recommendations for user

4. **Gap Report (Enhanced)**

   **Summary:**
   - Frontend: X components found, Y documented, Z undocumented
   - Backend: X endpoints found, Y documented, Z undocumented
   - MCP: X HTTP routes found, Y documented
   - Architecture: Missing/present status for ARCHITECTURE.md, BACKEND_API.md, FRONTEND_COMPONENTS.md

   **Critical Gaps:**

   ### Frontend
   - **Component: [Name]**
     - Location: `[path]`
     - Purpose: [description]
     - Key features: [list]
     - Should be added to: FRONTEND_COMPONENTS.md → [Section]
     - Priority: [CRITICAL/HIGH/MEDIUM/LOW]

   ### Backend
   - **Endpoint: [METHOD] [path]**
     - Location: `[file]:[line]`
     - Purpose: [description]
     - Request schema: [Pydantic model]
     - Response schema: [Pydantic model]
     - Should be added to: BACKEND_API.md → [Section]
     - Priority: [level]

   ### MCP Server
   - **HTTP Route: [METHOD] [path]**
     - Location: `[file]:[line]`
     - Purpose: [why HTTP instead of MCP tool]
     - Parameters: [list]
     - Should be added to: MCP_GUIDE.md → HTTP Endpoints (new section)
     - Priority: [level]

   ### Architecture
   - **Missing: ARCHITECTURE.md**
     - Should document: 3-tier structure, tech stack, data flow, databases
     - Priority: CRITICAL

   - **Missing: BACKEND_API.md**
     - Should document: All 31 endpoints with request/response schemas
     - Priority: CRITICAL

   - **Missing: FRONTEND_COMPONENTS.md**
     - Should document: 28 components, state management, API integration
     - Priority: CRITICAL

---

## When You Restructure the Project

If you move directories (e.g., `mcp-server/src/mcp/` → `mcp/`), update the **Project Structure Declaration** section at the top of this file:

1. Update the "Primary" path for the affected layer
2. Move old primary to "If not found, check" list
3. Run `/reference-audit` to verify discovery works
4. If audit succeeds, delete old paths from fallback list

**Example:** Moving MCP server from `mcp-server/src/mcp/` to `mcp/`:

**Before:**
```
**MCP Server:**
- Primary: `mcp-server/src/mcp/`
- If not found, check: `src/mcp/`, `mcp/src/`
```

**After:**
```
**MCP Server:**
- Primary: `mcp/`
- If not found, check: `mcp-server/src/mcp/`, `src/mcp/`
```

**Critical:** This approach prioritizes **reliability over auto-discovery**. Explicit paths prevent confusion and ensure the audit always works correctly.

---

Starting the bi-directional audit now.
