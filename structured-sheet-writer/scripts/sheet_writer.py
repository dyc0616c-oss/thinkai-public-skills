#!/usr/bin/env python3
import argparse, csv, json
from pathlib import Path

def load_records(path):
    path = Path(path)
    if path.suffix.lower() == ".json":
        data = json.loads(path.read_text(encoding="utf-8"))
        return data if isinstance(data, list) else data["records"]
    with path.open(newline="", encoding="utf-8-sig") as f:
        return list(csv.DictReader(f))

def key_for(row, keys):
    return tuple(str(row.get(k, "")).strip() for k in keys)

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--input", required=True)
    p.add_argument("--target", required=True)
    p.add_argument("--schema", required=True)
    p.add_argument("--key", action="append", required=True)
    p.add_argument("--apply", action="store_true")
    args = p.parse_args()
    schema = json.loads(Path(args.schema).read_text(encoding="utf-8"))
    columns = schema["columns"]
    incoming = load_records(args.input)
    unknown = sorted({k for row in incoming for k in row if k not in columns})
    if unknown:
        raise SystemExit(f"unknown columns: {unknown}")
    normalized = [{col: row.get(col, "") for col in columns} for row in incoming]
    seen, duplicates = set(), []
    for row in normalized:
        k = key_for(row, args.key)
        if not all(k) or k in seen:
            duplicates.append(k)
        seen.add(k)
    if duplicates:
        raise SystemExit(f"duplicate or empty incoming keys: {duplicates}")
    target = Path(args.target).resolve()
    existing = []
    if target.exists():
        with target.open(newline="", encoding="utf-8-sig") as f:
            existing = list(csv.DictReader(f))
    index = {key_for(row, args.key): i for i, row in enumerate(existing)}
    inserts, updates = 0, 0
    for row in normalized:
        k = key_for(row, args.key)
        if k in index:
            existing[index[k]] = row
            updates += 1
        else:
            existing.append(row)
            index[k] = len(existing) - 1
            inserts += 1
    plan = {"target": str(target), "columns": columns, "keys": args.key, "incoming": len(normalized), "inserts": inserts, "updates": updates, "apply": args.apply}
    if args.apply:
        target.parent.mkdir(parents=True, exist_ok=True)
        with target.open("w", newline="", encoding="utf-8-sig") as f:
            writer = csv.DictWriter(f, fieldnames=columns)
            writer.writeheader()
            writer.writerows(existing)
    print(json.dumps(plan, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    main()
