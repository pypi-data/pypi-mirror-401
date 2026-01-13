# **End-to-End Documentation: Coding Agent Plugin (OVERVIEW.md)**

---

## **1. Purpose of the Project**

The **Coding Agent Plugin** is an AI-powered, multi-agent system designed to autonomously create, manage, and evolve software projects from natural language prompts. Built as a modular plugin architecture, it integrates large language models (LLMs), project management, file system orchestration, and communication protocols to simulate a human-like software development workflow.

The core mission is to **eliminate manual boilerplate and repetitive coding tasks** by enabling users to describe a desired application in plain language — e.g., _“Create a FastAPI backend with user authentication and PostgreSQL”_ — and have the system **automatically generate, test, document, and deploy** the project with minimal human intervention.

This system is not just a code generator — it is an **agentic coder** that:
- Plans tasks using semantic context analysis
- Writes and modifies code iteratively
- Fixes errors autonomously
- Documents codebases
- Manages version control
- Communicates between specialized agents using standardized protocols

It is designed for both **interactive use** (via CLI or UI) and **autonomous execution** (via API or background services), making it suitable for developers, DevOps teams, and AI-driven development platforms.

---

## **2. Key Components and Their Interactions**

The system is organized into **five core architectural layers**, each with distinct responsibilities and well-defined interfaces.

### **2.1. Core Infrastructure Layer**

| Component | Role |
|---------|------|
| `core/config.py` | Loads and validates environment variables (LLM keys, paths, retry policies, database URLs) from `.env`. |
| `core/database.py` | Manages async SQLAlchemy engine and session lifecycle for PostgreSQL/SQLite. |
| `core/logging.py` | Centralized Rich-based logging with colorized console output and project-specific log directories. |

> ✅ These components provide the foundational environment for all other modules — configuration, persistence, and observability.

### **2.2. Data & Persistence Layer**

| Component | Role |
|---------|------|
| `models/db_models.py` | SQLAlchemy ORM models for `Project`, `File`, `Version`, and `Task` entities. |
| `schemas/project.py` | SQLAlchemy schema definitions (metadata, constraints). |
| `models/project.py` | Pydantic models for request/response validation (e.g., `ProjectCreate`, `ProjectResponse`). |
| `repositories/project.py` | Async repository layer for CRUD operations on projects (abstracts database access). |
| `services/project.py` | Business logic layer: orchestrates project creation, retrieval, and lifecycle management. |
| `managers/project_manager.py` | High-level project lifecycle manager: creates, lists, switches, and validates projects on disk and in DB. |
| `managers/storage_manager.py` | Handles file I/O: saves generated code to disk and tracks metadata (path, hash, timestamp) in DB. |

> 🔗 **Interaction**:  
> `ProjectService` → `ProjectRepository` → `SQLAlchemy` → `PostgreSQL/SQLite`  
> `StorageManager` ↔ `ProjectManager` ↔ Filesystem (writes `.py`, `.md`, `.gitignore`, etc.)

### **2.3. Agent Orchestration Layer (The “Brain”)**

This is the heart of the system — a **dynamic, plugin-based agent framework** that uses **IBM’s Agent Communication Protocol (ACP)** and **Model Control Protocol (MCP)** for inter-agent communication.

| Agent | Role | Protocol Used |
|-------|------|---------------|
| `OrchestratorAgent` (`agents/orchestrator.py`) | Master coordinator. Dynamically discovers and routes tasks to other agents using introspection and ACP. Uses LangChain for planning. | ACP (HTTP/In-process) |
| `PlanningAgent` (`agents/planning.py`) | Breaks down user prompts into actionable tasks using semantic search (MCP) over project context. Extracts keywords and maps to relevant files. | MCP (file resource querying) |
| `CodingAgent` (`agents/coding.py`) | Generates code from task descriptions using LLMs. Integrates with `ProjectManager` to read context and write files. | ACP |
| `FileModifierAgent` (`agents/file_modifier.py`) | Makes targeted edits to existing files (e.g., add a route, fix a bug) using LLM-guided diff generation. | ACP |
| `ErrorAgent` (`agents/error.py`) | Detects runtime or syntax errors (via `ExecutionAgent`) and proposes fixes using context-aware LLM prompts. | ACP |
| `ExecutionAgent` (`agents/execution.py`) | Runs shell commands (e.g., `pip install`, `python main.py`) in project context. Captures stdout/stderr. | Native async subprocess |
| `DocumentationAgent` (`agents/documentation.py`) | Uses Map-Reduce pattern: scans files, summarizes per module, then generates global docs. | MCP (file scanning) |
| `TaskAgent` (`agents/task.py`) | Persists task status to `tasks.md` in project root. Tracks progress. | File I/O + DB |

> 🔗 **Interaction Flow (Typical Workflow)**:
> 1. User submits prompt → `OrchestratorAgent` receives it.
> 2. Orchestrator calls `PlanningAgent` → MCP queries project context → generates task list.
> 3. Orchestrator delegates each task:
>    - `CodingAgent` → generates `main.py`
>    - `FileModifierAgent` → adds FastAPI route
>    - `ExecutionAgent` → runs `pip install fastapi`
>    - `ErrorAgent` → catches `ImportError` → fixes import
>    - `DocumentationAgent` → generates `README.md`
> 4. `TaskAgent` updates `tasks.md`
> 5. `StorageManager` saves all files and commits to DB
> 6. `GitManager` initializes repo and commits changes

### **2.4. Communication Protocols Layer**

| Component | Role |
|----------|------|
| `acp/client.py`, `acp/server.py` | ACP (Agent Communication Protocol) client/server wrappers. Converts internal agent messages to IBM ACP-compliant JSON format over HTTP. |
| `mcp/server.py`, `mcp/__init__.py` | MCP (Model Control Protocol) server exposing project files as read-only resources via URI paths (e.g., `mcp://project1/src/main.py`). |
| `acp_sdk/client.py`, `acp_sdk/server.py` | Mock ACP server/client for testing (used in `tests/acp_sdk/`). |
| `acp_sdk/models/models.py` | Pydantic models for ACP message structure (`Message`, `MessagePart`). |

> 🔗 **Why ACP & MCP?**  
> - **ACP** enables **decoupled, protocol-standardized communication** between agents — critical for scalability and testing.  
> - **MCP** allows agents to **safely query project files** without direct filesystem access — enabling sandboxing and remote agent execution.

### **2.5. Utility & Support Layer**

| Component | Role |
|----------|------|
| `utils/token_manager.py` | Counts and truncates tokens using `tiktoken` to fit prompts within LLM context windows. |
| `utils/validation.py` | Validates project IDs, prompts, file paths; throws custom `ValidationError`. |
| `utils/logger.py` | Extends `core/logging.py` with project-scoped log files. |
| `services/llm_service.py` | Abstracts LLM API calls (OpenAI, Anthropic, etc.) with retry, timeout, and token tracking. |
| `services/prompt_service.py` | Provides standardized system prompts for Planning, Coding, and Error agents. |
| `integrations/git_manager.py` | Initializes Git repo, adds `.gitignore`, and commits changes after each major phase. |

---

## **3. Data Flow: End-to-End Journey**

Here’s how a typical user request flows through the system:

### **Step 1: Input — User Prompt**
```bash
$ coding-agent create "FastAPI app with /login and /register endpoints, PostgreSQL, JWT auth"
```

→ CLI (`cli/main.py`) parses input → passes to `ProjectService.create()`

### **Step 2: Project Initialization**
- `ProjectService` → creates DB record (`Project` model)
- `ProjectManager` → creates project directory: `projects/my-fastapi-app/`
- `StorageManager` → logs project metadata in DB: `project_id`, `created_at`, `status=initializing`

### **Step 3: Planning Phase**
- `OrchestratorAgent` → invokes `PlanningAgent` via ACP
- `PlanningAgent` → uses MCP to scan project directory (empty at first) → identifies no context
- Uses **semantic search** on prompt → extracts keywords: `FastAPI`, `login`, `register`, `PostgreSQL`, `JWT`
- Generates task plan:
  ```
  1. Create main.py with FastAPI app
  2. Create models/user.py
  3. Create routes/auth.py
  4. Create config/database.py
  5. Install dependencies: fastapi, psycopg2, python-jose
  6. Generate README.md
  ```

### **Step 4: Execution Phase — Agent Coordination**
The `OrchestratorAgent` executes tasks in sequence:

| Task | Agent | Action | Output |
|------|-------|--------|--------|
| 1 | `CodingAgent` | Generates `main.py` with `FastAPI()` app | `projects/my-fastapi-app/main.py` |
| 2 | `CodingAgent` | Generates `models/user.py` | `projects/my-fastapi-app/models/user.py` |
| 3 | `CodingAgent` | Generates `routes/auth.py` | `projects/my-fastapi-app/routes/auth.py` |
| 4 | `CodingAgent` | Generates `config/database.py` | `projects/my-fastapi-app/config/database.py` |
| 5 | `ExecutionAgent` | Runs `pip install fastapi psycopg2 python-jose` | Logs output, captures success |
| 6 | `DocumentationAgent` | Scans all files → generates `README.md` | `projects/my-fastapi-app/README.md` |
| 7 | `FileModifierAgent` | Adds `@app.get("/health")` for testing | Updates `main.py` |
| 8 | `ErrorAgent` | Detects missing `from pydantic import BaseModel` → fixes | Updates `models/user.py` |

> Each agent communicates via **ACP messages**:
> ```json
> {
>   "type": "request",
>   "to": "coding",
>   "from": "orchestrator",
>   "content": {
>     "prompt": "Generate a FastAPI app with /login endpoint...",
>     "context": "No files yet. Target: main.py"
>   }
> }
> ```

### **Step 5: Persistence & Versioning**
- `StorageManager` saves each generated/modified file to disk
- Each file’s hash, path, and timestamp are recorded in DB
- `GitManager` initializes repo and commits after each major phase (e.g., after codegen, after fixes)

### **Step 6: Task Tracking & Feedback**
- `TaskAgent` updates `tasks.md`:
  ```md
  ## Tasks for my-fastapi-app
  - [x] Create main.py
  - [x] Create models/user.py
  - [ ] Generate tests
  ```
- User can inspect progress via CLI or UI (`ui/plan_review.py`)

### **Step 7: Output & Completion**
- Project directory is fully populated
- DB record updated: `status=completed`
- User receives confirmation:
  ```
  ✅ Project 'my-fastapi-app' created successfully!
  Files: 8 | Commits: 2 | Tokens used: 4,217
  Run: cd my-fastapi-app && uvicorn main:app --reload
  ```

### **Optional: Autonomous Mode**
In API mode (`acp/start_server.py`), the same flow is triggered via HTTP:
```bash
POST /api/agents/orchestrator/invoke
{
  "prompt": "Create a FastAPI app with login..."
}
```
→ Returns `200 OK` with project ID and status URL.

---

## **Summary: System Architecture Diagram (Text-Based)**

```
[User]
   │
   ▼
[CLI / API] → ProjectService → ProjectManager → StorageManager
   │                                   │
   ▼                                   ▼
[OrchestratorAgent] ←── ACP ───→ [PlanningAgent] ←─ MCP ──→ [Project Files]
   │        ▲                          │
   │        │                          ▼
   │        └── ACP ────────────────→ [CodingAgent]
   │                                   │
   │                                   ▼
   │                             [FileModifierAgent]
   │                                   │
   │                                   ▼
   │                             [ErrorAgent] ←── ExecutionAgent
   │                                   │
   │                                   ▼
   │                             [DocumentationAgent]
   │                                   │
   │                                   ▼
   └───────────────────────────────→ [TaskAgent] → tasks.md
                                       │
                                       ▼
                                   [GitManager] → .git/
                                       │
                                       ▼
                                   [Database] ←─ ProjectRepository ←─ SQLAlchemy
```

---

## **Conclusion**

The **Coding Agent Plugin** is a sophisticated, production-ready agentic coding system that transforms natural language into fully functional software. By combining:

- **Modular agent design** (planning, coding, error-handling),
- **Standardized communication** (ACP/MCP),
- **Robust persistence** (SQLAlchemy + file system),
- **Context-aware LLM integration**,
- **Autonomous workflow orchestration**,

…it delivers a **true AI pair programmer** experience. Whether used via CLI, UI, or API, it enables developers to focus on **high-level design** while the system handles the **low-level implementation**.

This system is designed to scale — new agents can be added as plugins, new LLMs can be swapped, and new protocols can be integrated — making it a foundational platform for the future of AI-assisted software development.

--- 

**Next Steps**:  
- Explore `examples/interactive_ecommerce.py` for a live demo  
- Run `tests/integration/test_integration.py` to see end-to-end flow  
- Start the ACP server: `python src/coding_agent_plugin/acp/start_server.py`