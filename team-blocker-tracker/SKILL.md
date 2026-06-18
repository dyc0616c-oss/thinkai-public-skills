---
name: team-blocker-tracker
description: Record, deduplicate, list, resolve, and export small-team blockers with local SLA tracking in SQLite. Use when a user wants a local impediment register, overdue review, monthly retrospective data, or a safe alternative to an always-on Telegram reminder bot; notifications and AI rewriting remain disabled by default.
---

# Team Blocker Tracker

Use `scripts/blocker_tracker.py`.

1. Keep the core local. Do not send messages or call AI.
2. Create blockers with a deduplication key and explicit SLA hours.
3. Show overdue state from stored timestamps.
4. Resolve by exact blocker ID.
5. Export only requested fields; do not include tokens or chat IDs.

```bash
python3 scripts/blocker_tracker.py --db blockers.sqlite3 add --title "API blocked" --owner Alice --priority P1 --sla-hours 24 --dedup-key api-42
python3 scripts/blocker_tracker.py --db blockers.sqlite3 list
python3 scripts/blocker_tracker.py --db blockers.sqlite3 resolve 1 --note "Access granted"
python3 scripts/blocker_tracker.py --db blockers.sqlite3 export --output blockers.csv
```
