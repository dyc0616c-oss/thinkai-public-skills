#!/usr/bin/env python3
import argparse, hashlib, json, re, sqlite3
from datetime import datetime, timedelta, timezone
from pathlib import Path

PATTERNS = [
    re.compile(r"(?i)\b(api[_-]?key|token|password|secret)\b\s*[:=]\s*\S+"),
    re.compile(r"\b\d{6,12}:[A-Za-z0-9_-]{30,}\b"),
    re.compile(r"-----BEGIN [A-Z ]*PRIVATE KEY-----"),
]

def timestamp():
    return datetime.now(timezone.utc).isoformat()

def redact(text):
    for pattern in PATTERNS:
        text = pattern.sub("[REDACTED]", text)
    return text

def database_path(root, workspace):
    slug = re.sub(r"[^a-zA-Z0-9._-]+", "-", workspace).strip("-") or "default"
    digest = hashlib.sha256(workspace.encode()).hexdigest()[:8]
    path = Path(root).expanduser().resolve() / f"{slug[:48]}-{digest}.sqlite3"
    path.parent.mkdir(parents=True, exist_ok=True)
    return path

def connect(path):
    db = sqlite3.connect(path)
    db.row_factory = sqlite3.Row
    db.execute("""CREATE TABLE IF NOT EXISTS memories(
      id INTEGER PRIMARY KEY, title TEXT NOT NULL, content TEXT NOT NULL,
      tags TEXT NOT NULL DEFAULT '[]', created_at TEXT NOT NULL,
      expires_at TEXT, source TEXT NOT NULL DEFAULT 'user')""")
    return db

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--workspace", required=True)
    p.add_argument("--data-dir", default=".agent-memory")
    sub = p.add_subparsers(dest="cmd", required=True)
    add = sub.add_parser("add")
    add.add_argument("--title", required=True)
    add.add_argument("--content", required=True)
    add.add_argument("--tags", default="")
    add.add_argument("--ttl-days", type=int)
    search = sub.add_parser("search")
    search.add_argument("query")
    search.add_argument("--limit", type=int, default=20)
    sub.add_parser("list").add_argument("--limit", type=int, default=50)
    delete = sub.add_parser("delete")
    delete.add_argument("id", type=int)
    export = sub.add_parser("export")
    export.add_argument("--output", required=True)
    sub.add_parser("purge-expired")
    args = p.parse_args()
    path = database_path(args.data_dir, args.workspace)
    db = connect(path)
    if args.cmd == "add":
        expiry = (datetime.now(timezone.utc) + timedelta(days=args.ttl_days)).isoformat() if args.ttl_days else None
        cur = db.execute("INSERT INTO memories(title,content,tags,created_at,expires_at) VALUES(?,?,?,?,?)",
            (redact(args.title), redact(args.content), json.dumps([x.strip() for x in args.tags.split(",") if x.strip()]), timestamp(), expiry))
        db.commit()
        result = {"id": cur.lastrowid, "database": str(path)}
    elif args.cmd in {"search", "list"}:
        if args.cmd == "search":
            q = f"%{args.query}%"
            rows = db.execute("SELECT * FROM memories WHERE (title LIKE ? OR content LIKE ?) AND (expires_at IS NULL OR expires_at>?) ORDER BY id DESC LIMIT ?", (q, q, timestamp(), args.limit))
        else:
            rows = db.execute("SELECT * FROM memories WHERE expires_at IS NULL OR expires_at>? ORDER BY id DESC LIMIT ?", (timestamp(), args.limit))
        result = [dict(r) for r in rows]
    elif args.cmd == "delete":
        cur = db.execute("DELETE FROM memories WHERE id=?", (args.id,))
        db.commit()
        result = {"deleted": cur.rowcount, "database": str(path)}
    elif args.cmd == "export":
        rows = [dict(r) for r in db.execute("SELECT * FROM memories ORDER BY id")]
        out = Path(args.output).expanduser().resolve()
        out.write_text(json.dumps(rows, ensure_ascii=False, indent=2), encoding="utf-8")
        result = {"exported": len(rows), "output": str(out)}
    else:
        cur = db.execute("DELETE FROM memories WHERE expires_at IS NOT NULL AND expires_at<=?", (timestamp(),))
        db.commit()
        result = {"purged": cur.rowcount, "database": str(path)}
    print(json.dumps(result, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    main()
