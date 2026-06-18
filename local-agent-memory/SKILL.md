---
name: local-agent-memory
description: Store, search, export, expire, and delete project-scoped Agent memories in a local SQLite database. Use when a user asks to remember project facts, retrieve prior decisions, inspect stored memories, enforce retention, or remove local memory without sending data to a remote service.
---

# Local Agent Memory

Use `scripts/memory_store.py`. Keep each project in a separate workspace.

1. Resolve a stable workspace name from the current project or ask the user.
2. Store data under the selected directory; default to `.agent-memory/`.
3. Redact likely secrets before writing.
4. Use keyword search by default. Do not scan unrelated directories.
5. Show the database path after mutations.
6. Require an exact ID for deletion.

```bash
python3 scripts/memory_store.py --workspace demo add --title "API choice" --content "Use REST"
python3 scripts/memory_store.py --workspace demo search "REST"
python3 scripts/memory_store.py --workspace demo list
python3 scripts/memory_store.py --workspace demo delete 1
python3 scripts/memory_store.py --workspace demo export --output memories.json
```

Never ingest `~/.claude`, browser profiles, hidden credential folders, or an entire home directory without explicit scope.
