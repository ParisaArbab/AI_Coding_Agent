# AI Coding Agent

Built an AI coding agent using Python, FastAPI, LangGraph, LangChain, MCP, GitHub API, OpenAI/Claude, and Docker. It supports repository Q&A, code review, bug triage, documentation generation, and GitHub issue analysis, then proposes code fixes and pull request workflows with safe, modular tools.


## Features in this project

- GitHub issue analysis and fix proposal
- Repository question answering
- Code review
- Bug triage
- Documentation generation
- LangGraph workflow orchestration
- MCP repository tools
- OpenAI, Claude, and free mock mode
- FastAPI REST API
- GitHub API integration
- Docker deployment
- Safety controls for filesystem and GitHub writes

## Architecture

```text
Client -> FastAPI -> LangGraph Agent
                       |-> Repository tools
                       |-> GitHub API
                       |-> OpenAI / Claude / Mock LLM
                       |-> MCP server
```

The LangGraph workflow has three steps: collect context, analyze, and finalize. The design is intentionally simple so you can add testing, patch application, human approval, and pull request nodes.

## Project structure

```text
app/
  agents/       LangGraph workflow, prompts, parser
  api/          FastAPI routes
  core/         settings, logging, security
  llm/          OpenAI, Claude, mock providers
  models/       request, response, state schemas
  services/     repository and GitHub services
  tools/        LangChain repository tools
mcp_server/     MCP server
workspace/      local repositories inspected by the agent
tests/          unit and API tests
```

## Quick start

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
cp .env.example .env
uvicorn app.main:app --reload
```

Open `http://localhost:8000/docs`.

Mock mode is enabled by default, so no API key is needed.

### OpenAI

```env
LLM_PROVIDER=openai
OPENAI_API_KEY=your_key
OPENAI_MODEL=gpt-4.1-mini
```

### Claude

```env
LLM_PROVIDER=anthropic
ANTHROPIC_API_KEY=your_key
ANTHROPIC_MODEL=claude-sonnet-4-5
```

## Example requests

Repository Q&A:

```bash
curl -X POST http://localhost:8000/api/v1/agent/run \
  -H "Content-Type: application/json" \
  -d '{
    "task_type": "repository_qa",
    "instruction": "Explain the architecture and request flow.",
    "repository_path": "sample_repo"
  }'
```

Code review:

```bash
curl -X POST http://localhost:8000/api/v1/agent/run \
  -H "Content-Type: application/json" \
  -d '{
    "task_type": "code_review",
    "instruction": "Review the code for reliability and security problems.",
    "repository_path": "sample_repo"
  }'
```

GitHub issue analysis:

```bash
curl -X POST http://localhost:8000/api/v1/agent/run \
  -H "Content-Type: application/json" \
  -d '{
    "task_type": "issue_fix",
    "instruction": "Analyze issue 42 and propose a fix.",
    "github_owner": "owner",
    "github_repo": "repo",
    "issue_number": 42
  }'
```

## MCP server

```bash
python -m mcp_server.server
```

MCP tools:

- `list_repository_files`
- `read_repository_file`
- `search_repository`
- `summarize_repository`

Example desktop configuration:

```json
{
  "mcpServers": {
    "coding-agent": {
      "command": "python",
      "args": ["-m", "mcp_server.server"],
      "env": {"WORKSPACE_ROOT": "./workspace"}
    }
  }
}
```

## Docker

```bash
docker compose up --build
```

## Tests

```bash
pytest
ruff check .
```

## Pull request safety

GitHub reading is supported with `GITHUB_TOKEN`. GitHub write methods are included, but writes are blocked unless:

```env
ALLOW_PR_CREATION=true
```

The starter graph does not automatically apply patches. This is intentional. A production agent should require human approval before branch creation, file updates, or pull request submission.



## Resume description

Built an AI coding agent with FastAPI, LangGraph, MCP, GitHub API, and OpenAI/Claude integrations. The system supports repository Q&A, issue analysis, code review, bug triage, documentation generation, and protected pull request workflows using modular tools and Docker deployment.
