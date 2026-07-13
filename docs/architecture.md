# Architecture

The project separates HTTP delivery, agent orchestration, model access, GitHub access, repository inspection, and MCP tools.

## LangGraph flow

1. Collect local or GitHub repository context
2. Ask the selected LLM to analyze the task
3. Parse a structured response
4. Return a proposed change and optional patch

## Safety

- Path traversal is blocked
- Secret filenames and binary files are blocked
- Large files are skipped
- GitHub writes are disabled by default
- Automatic patch application is not enabled

## Suggested extensions

- Human approval node
- Sandboxed test runner
- Patch validator
- GitHub webhook endpoint
- Vector code search
- Persistent LangGraph checkpoints
- Audit logs and tracing
