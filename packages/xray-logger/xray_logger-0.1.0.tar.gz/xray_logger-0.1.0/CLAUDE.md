# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

X-Ray SDK & API - A decision-reasoning observability system for multi-step pipelines. Captures **why** decisions were made (candidates, filters, scores, reasoning), not just what functions ran.

## Architecture

Two packages with clear separation:

- **xray_sdk/** - Python SDK for instrumenting pipelines
  - Uses `contextvars` for Run/Step context propagation across async boundaries
  - Async buffered transport with fail-open semantics (never block/crash pipelines)
  - Decorators (`@step`, `@instrument_class`) and middleware for ergonomic instrumentation

- **xray_api/** - FastAPI backend for storage and queries
  - SQLAlchemy ORM with SQLite (dev) / PostgreSQL (prod)
  - Two tables: Run and Step (no separate Candidate table - stored in Step.metadata)

## Key Design Decisions

- `input_count`/`output_count` stored as columns; `removed_ratio` computed at query time
- Payload strategy: `detail="summary"` (default) captures counts + samples; `detail="full"` captures complete data with truncation
- SDK must be fail-open: backend unavailability must never affect instrumented pipelines

## Data Flow

```
User Code → @step decorator → XRayClient (contextvars) → Transport (async buffer) → HTTP POST → API → Store → DB
```

## Git Commits

- Do NOT add "Co-Authored-By: Claude" to commit messages
- Do NOT add any AI attribution in commits
- Do NOT add "Generated with Claude Code" to commits
- Use standard commit message format

## TaskMaster Workflow

When starting work on a new TaskMaster task, follow this workflow:

### 1. Read the Task
```bash
# Use TaskMaster MCP to get task details
mcp-cli call task-master-ai/get_task '{"id": "2", "projectRoot": "/path/to/project"}'
```

### 2. Create GitHub Issue
Use GitHub MCP to create an issue for the task:
```bash
mcp-cli call github/issue_write '{
  "method": "create",
  "owner": "mohit-nagaraj",
  "repo": "oc-assignment",
  "title": "Task 2: Implement SDK Transport Layer",
  "body": "## Description\n[Task details from TaskMaster]\n\n## Subtasks\n- [ ] Subtask 1\n- [ ] Subtask 2"
}'
```

### 3. Create Feature Branch
```bash
git checkout -b feat/task-2-sdk-transport
```

### 4. Plan & Implement
- Use plan mode for complex tasks
- Implement changes following the task subtasks
- Write tests as you go
- Commit frequently with descriptive messages

### 5. Create Pull Request
Use GitHub MCP to create PR to main:
```bash
mcp-cli call github/create_pull_request '{
  "owner": "mohit-nagaraj",
  "repo": "oc-assignment",
  "title": "feat(task-2): Implement SDK Transport Layer",
  "body": "## Summary\n[Changes made]\n\n## Test Plan\n[How to test]\n\nCloses #[issue-number]",
  "head": "feat/task-2-sdk-transport",
  "base": "main"
}'
```

### 6. Mark Task Complete
```bash
mcp-cli call task-master-ai/set_task_status '{"id": "2", "status": "done", "projectRoot": "/path/to/project"}'
```

## Task Master AI Instructions
**Import Task Master's development workflow commands and guidelines, treat as if import is in the main CLAUDE.md file.**
@./.taskmaster/CLAUDE.md
