# Public API Documentation for coding-agent-plugin

## 1. What is the Public API?

The **Public API** in the `coding-agent-plugin` project is the externally accessible HTTP REST interface that allows external clients (e.g., web applications, CLI tools, microservices, or UIs) to interact with the agentic coding system. It exposes the core functionality of the AI-powered code generation and project orchestration system through standardized endpoints, enabling seamless integration with other systems without requiring direct Python module imports or in-process execution.

The Public API acts as the **gateway** between the internal multi-agent architecture (Planner, Coder, Orchestrator, ErrorAgent, etc.) and external users or services. It translates HTTP requests into agent communication protocol (ACP) messages, orchestrates multi-step workflows, and returns structured JSON responses containing generated code, project metadata, status updates, or error details.

This API is designed to be:
- **Stateless**: Each request is self-contained and validated.
- **Agent-agnostic**: Clients interact with endpoints, not individual agents.
- **Scalable**: Built on FastAPI with async support for concurrent agent invocations.
- **Secure**: Uses environment-configured authentication and input validation.
- **Standardized**: Follows REST conventions with consistent response schemas.

The Public API enables use cases such as:
- Automated CI/CD pipelines triggering code generation from Jira tickets.
- Web dashboards allowing users to request project creation via forms.
- Third-party tools integrating AI-assisted coding into IDEs or collaboration platforms.

> ⚠️ **Note**: This API is currently in Beta and subject to change. Breaking changes may occur without prior notice. Please monitor release notes and avoid relying on stable behavior in production environments until a stable v1.0 release.

---

## 2. Files Implementing the Public API

The Public API is implemented across the following key files:

| File | Role |
|------|------|
| `src/coding_agent_plugin/acp/server.py` | **Core API server** — Defines FastAPI routes, request validation, and agent routing logic. |
| `src/coding_agent_plugin/acp/start_server.py` | **Server entrypoint** — Initializes and launches the Uvicorn ASGI server. |
| `src/coding_agent_plugin/acp/client.py` | **Client utilities** — Provides HTTP and in-process clients to communicate with the API (used internally and for testing). |
| `src/coding_agent_plugin/acp/__init__.py` | **Public API module initializer** — Exports only the client module for external use, hiding internal server logic. |
| `src/coding_agent_plugin/models/project.py` | **Schema definitions** — Pydantic models for request/response validation (e.g., `ProjectCreate`, `ProjectResponse`). |
| `src/coding_agent_plugin/schemas/project.py` | **Database schema** — Used by the API to map request data to ORM models. |
| `src/coding_agent_plugin/services/project.py` | **Business logic** — Handles project creation, retrieval, and validation logic invoked by API endpoints. |
| `src/coding_agent_plugin/services/llm_service.py` | **LLM integration** — Used by API endpoints to invoke LLMs for code generation. |
| `src/coding_agent_plugin/services/prompt_service.py` | **Prompt templating** — Provides standardized system prompts for agents invoked via the API. |
| `tests/test_public_api.py` | **Integration tests** — Validates API endpoints, health checks, agent invocation, and error handling. |
| `examples/test_public_api.py` | **Usage example** — Demonstrates how to interact with the Public API using HTTP clients. |

> 💡 **Note**: The Public API is distinct from the internal ACP (Agent Communication Protocol) used between agents. While ACP is a message-passing protocol for agent-to-agent communication, the Public API is an HTTP-based interface for external clients.

---

## 3. Detailed Logic and Flow of the Public API

### 3.1. Architecture Overview

The Public API follows a **layered architecture**:

```
External Client (HTTP)
        ↓
[FastAPI Server] ← (Routes, Validation, Auth)
        ↓
[OrchestratorAgent] ← (Routes task to appropriate agent)
        ↓
[PlanningAgent / CodingAgent / FileModifier / etc.]
        ↓
[ProjectService / StorageManager / MCP / GitManager]
        ↓
[Database / Filesystem / Git Repo]
        ↓
[JSON Response to Client]
```

### 3.2. Request Flow (Step-by-Step)

#### Step 1: HTTP Request Received
An external client sends an HTTP POST request to one of the exposed endpoints, e.g.:

```http
POST /api/v1/projects/create
Content-Type: application/json

{
  "name": "my-fastapi-app",
  "description": "A task management system with SQLite",
  "stack": "fastapi",
  "features": ["auth", "database", "swagger"],
  "user_id": "user_123"
}
```

#### Step 2: Request Validation
The FastAPI server uses Pydantic models (`ProjectCreate`) to validate the request body. Invalid requests return a `422 Unprocessable Entity` with detailed error messages.

#### Step 3: Authentication & Authorization (Optional)
If configured (via `AUTH_ENABLED=true`), the API checks for a valid API key in the `Authorization` header. This is implemented in middleware or dependency injection.

#### Step 4: Route to OrchestratorAgent
The endpoint handler (defined in `acp/server.py`) delegates the request to the `OrchestratorAgent` instance, which is initialized once at server startup and reused across requests.

```python
# Example route in acp/server.py
@app.post("/api/v1/projects/create")
async def create_project(project: ProjectCreate):
    result = await orchestrator_agent.execute_task(
        task_type="create_project",
        context=project.dict()
    )
    return result
```

#### Step 5: Orchestrator Agent Coordinates Workflow
The `OrchestratorAgent` (from `agents/orchestrator.py`) dynamically:
- Parses the request context (e.g., stack, features).
- Uses `PlanningAgent` to generate a task plan (e.g., “Create FastAPI app → Add auth → Setup DB”).
- Routes each task to the appropriate agent:
  - `PlanningAgent` → generates task list
  - `CodingAgent` → generates `main.py`, `models.py`, `routes.py`
  - `FileModifier` → updates configuration files
  - `ErrorAgent` → fixes syntax or logic errors
  - `ExecutionAgent` → runs `pip install` or `python main.py`
  - `GitManager` → initializes repo and commits changes
  - `StorageManager` → saves files to disk and records metadata in DB
  - `ProjectService` → persists project metadata to database

#### Step 6: Agent Communication via ACP
Internally, agents communicate using the **Agent Communication Protocol (ACP)**, implemented via `src/acp/` and `src/coding_agent_plugin/acp/`. The Orchestrator sends messages to agents using HTTP POST to local endpoints (e.g., `http://localhost:8000/agents/planning`) or via in-process direct calls (for performance).

> The ACP message format is defined in `tests/acp_sdk/models/models.py`:
> ```python
> class Message(BaseModel):
>     id: str
>     sender: str
>     receiver: str
>     content: List[MessagePart]
> ```

#### Step 7: Response Aggregation
The Orchestrator collects results from each agent, validates outputs, and compiles a final response:

```json
{
  "status": "success",
  "project_id": "proj_abc123",
  "name": "my-fastapi-app",
  "files_created": ["main.py", "models/user.py", "routes/auth.py", "requirements.txt"],
  "git_commit": "a1b2c3d",
  "execution_logs": ["pip install fastapi", "python main.py"],
  "error_count": 0,
  "metadata": {
    "llm_model": "gpt-4-turbo",
    "total_tokens": 2847,
    "duration_seconds": 14.3
  }
}
```

#### Step 8: Response Sent to Client
The final JSON response is returned over HTTP with a `200 OK` status. Errors (e.g., LLM timeout, file permission denied) are returned as `400` or `500` with structured error details.

---

### 3.3. Key Endpoints

The Public API exposes the following core endpoints (defined in `acp/server.py`):

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/v1/health` | `GET` | Returns `{"status": "healthy"}`. Used for liveness probes. |
| `/api/v1/projects/create` | `POST` | Creates a new project from a natural language prompt or structured spec. |
| `/api/v1/projects/{project_id}` | `GET` | Retrieves project metadata and file list. |
| `/api/v1/projects/{project_id}/files` | `GET` | Lists all files in the project. |
| `/api/v1/projects/{project_id}/files/{filename}` | `GET` | Retrieves the content of a specific file. |
| `/api/v1/agents/{agent_name}/invoke` | `POST` | Directly invoke a specific agent (e.g., `planning`, `coding`) with custom input. |
| `/api/v1/projects/list` | `GET` | Lists all projects owned by a user (if auth is enabled). |
| `/api/v1/projects/{project_id}/delete` | `DELETE` | Deletes project files and database record. |

> ⚠️ **Note**: Direct agent invocation (`/agents/{agent_name}/invoke`) is primarily for debugging and advanced use cases. Production clients should use `/projects/create` for end-to-end workflows.

> ⚠️ **Beta Note**: Endpoint paths, request/response schemas, and behavior may change in future Beta releases. Always validate against the latest API documentation.

---

### 3.4. Error Handling

The Public API implements robust error handling:

| Error Type | HTTP Status | Response Example |
|------------|-------------|------------------|
| Invalid JSON | `400` | `{"detail": "Invalid JSON payload"}` |
| Missing required field | `422` | `{"detail": [{"loc": ["body", "name"], "msg": "field required"}]}` |
| Agent timeout | `504` | `{"error": "Agent 'coding' failed to respond within 30s"}` |
| File system permission denied | `500` | `{"error": "Cannot write to project directory: permission denied"}` |
| LLM API failure | `502` | `{"error": "OpenAI API returned 429: rate limit exceeded"}` |
| Project not found | `404` | `{"error": "Project with ID 'proj_xyz' not found"}` |

All errors include a unique `request_id` for tracing and logging.

---

### 3.5. Security & Configuration

- **Authentication**: Optional API key via `API_KEY` environment variable. If set, all endpoints require `Authorization: Bearer <key>`.
- **Rate Limiting**: Not implemented by default, but can be added via FastAPI middleware (e.g., `slowapi`).
- **CORS**: Configured via `CORS_ORIGINS` env var (default: `*` for development).
- **Logging**: All requests and responses are logged via `src/coding_agent_plugin/core/logging.py` with Rich formatting.
- **TLS**: Not enabled by default; intended to be terminated by a reverse proxy (e.g., Nginx, Traefik).

---

### 3.6. Example Usage

#### Using `curl` to create a project:

```bash
curl -X POST http://localhost:8000/api/v1/projects/create \
  -H "Content-Type: application/json" \
  -d '{
    "name": "todo-app",
    "stack": "fastapi",
    "features": ["sqlite", "auth", "swagger"]
  }'
```

#### Using Python `httpx`:

```python
import httpx

async def create_project():
    async with httpx.AsyncClient() as client:
        response = await client.post(
            "http://localhost:8000/api/v1/projects/create",
            json={
                "name": "my-service",
                "stack": "fastapi",
                "features": ["database", "auth"]
            }
        )
        print(response.json())

# Output:
# {
#   "status": "success",
#   "project_id": "proj_789",
#   "files_created": ["main.py", "models.py", "routes/auth.py"],
#   "git_commit": "d4e5f6"
# }
```

---

## Summary

The **Public API** is the critical interface that transforms the internal multi-agent AI coding system into a usable, scalable service. It abstracts away the complexity of agent orchestration, LLM calls, and file system operations, exposing a clean, RESTful interface for external integration. Built on FastAPI and ACP, it ensures reliability, performance, and extensibility — making the `coding-agent-plugin` not just a Python library, but a production-ready AI coding service.

For developers integrating with this API, the recommended approach is to:
1. Use `/api/v1/projects/create` for end-to-end project generation.
2. Monitor `/api/v1/health` for uptime.
3. Use `/api/v1/agents/{name}/invoke` only for debugging or advanced customization.
4. Always validate responses against the provided Pydantic schemas.

> 📌 **Pro Tip**: The `examples/test_public_api.py` script provides a complete working example of interacting with the Public API — use it as a reference for your own integrations.

> ⚠️ **Beta Notice**: This API is currently in Beta and subject to change. Breaking changes may occur without prior notice. Please monitor release notes and avoid relying on stable behavior in production environments until a stable v1.0 release.