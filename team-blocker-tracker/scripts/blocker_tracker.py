#!/usr/bin/env python3
import argparse, csv, json, sqlite3
from datetime import datetime, timedelta, timezone
from pathlib import Path

def now():
    return datetime.now(timezone.utc)

def connect(path):
    db = sqlite3.connect(Path(path).expanduser().resolve())
    db.row_factory = sqlite3.Row
    db.execute("""CREATE TABLE IF NOT EXISTS blockers(
      id INTEGER PRIMARY KEY, title TEXT NOT NULL, owner TEXT NOT NULL,
      priority TEXT NOT NULL, dedup_key TEXT NOT NULL,
      created_at TEXT NOT NULL, due_at TEXT NOT NULL,
      status TEXT NOT NULL DEFAULT 'open', resolved_at TEXT, resolution TEXT)""")
    db.execute("CREATE UNIQUE INDEX IF NOT EXISTS one_open_blocker_per_key ON blockers(dedup_key) WHERE status='open'")
    return db

def enriched(row):
    data = dict(row)
    data["overdue"] = data["status"] == "open" and datetime.fromisoformat(data["due_at"]) < now()
    return data

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--db", default=".team-blockers.sqlite3")
    sub = p.add_subparsers(dest="cmd", required=True)
    add = sub.add_parser("add")
    add.add_argument("--title", required=True)
    add.add_argument("--owner", required=True)
    add.add_argument("--priority", choices=["P0","P1","P2","P3"], default="P2")
    add.add_argument("--sla-hours", type=int, required=True)
    add.add_argument("--dedup-key", required=True)
    listing = sub.add_parser("list")
    listing.add_argument("--status", choices=["open","resolved","all"], default="open")
    resolve = sub.add_parser("resolve")
    resolve.add_argument("id", type=int)
    resolve.add_argument("--note", required=True)
    export = sub.add_parser("export")
    export.add_argument("--output", required=True)
    args = p.parse_args()
    db = connect(args.db)
    if args.cmd == "add":
        created, due = now(), now() + timedelta(hours=args.sla_hours)
        existing = db.execute("SELECT * FROM blockers WHERE dedup_key=? AND status='open'", (args.dedup_key,)).fetchone()
        if existing:
            result = {"created": False, "reason": "duplicate", "blocker": enriched(existing)}
        else:
            cur = db.execute("INSERT INTO blockers(title,owner,priority,dedup_key,created_at,due_at) VALUES(?,?,?,?,?,?)",
                (args.title, args.owner, args.priority, args.dedup_key, created.isoformat(), due.isoformat()))
            db.commit()
            result = {"created": True, "id": cur.lastrowid, "due_at": due.isoformat()}
    elif args.cmd == "list":
        query = "SELECT * FROM blockers"
        params = ()
        if args.status != "all":
            query += " WHERE status=?"
            params = (args.status,)
        result = [enriched(r) for r in db.execute(query + " ORDER BY id DESC", params)]
    elif args.cmd == "resolve":
        cur = db.execute("UPDATE blockers SET status='resolved',resolved_at=?,resolution=? WHERE id=? AND status='open'", (now().isoformat(), args.note, args.id))
        db.commit()
        result = {"resolved": cur.rowcount, "id": args.id}
    else:
        rows = [enriched(r) for r in db.execute("SELECT * FROM blockers ORDER BY id")]
        out = Path(args.output).expanduser().resolve()
        fields = ["id","title","owner","priority","created_at","due_at","status","resolved_at","resolution","overdue"]
        with out.open("w", newline="", encoding="utf-8-sig") as f:
            writer = csv.DictWriter(f, fieldnames=fields)
            writer.writeheader()
            writer.writerows([{k: r.get(k) for k in fields} for r in rows])
        result = {"exported": len(rows), "output": str(out)}
    print(json.dumps(result, ensure_ascii=False, indent=2, default=str))

if __name__ == "__main__":
    main()
