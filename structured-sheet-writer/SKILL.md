---
name: structured-sheet-writer
description: Preview and safely upsert JSON or CSV records into a local CSV table using a declared schema and key fields. Use when turning structured data into a spreadsheet-compatible table, checking inserts versus updates, or preparing a reviewed write plan before optional Google Sheets integration.
---

# Structured Sheet Writer

Use `scripts/sheet_writer.py`.

1. Require an input file, output CSV, schema JSON, and one or more key fields.
2. Run without `--apply` first. Show inserts, updates, conflicts, target, and column mapping.
3. Apply only after the user reviews the plan.
4. Reject duplicate keys inside the incoming batch.
5. Never read credentials or contact Google by default. The public v1 core is local CSV; add remote adapters only after a separate permission review.

```bash
python3 scripts/sheet_writer.py --input records.json --target table.csv --schema references/schema.example.json --key id
python3 scripts/sheet_writer.py --input records.json --target table.csv --schema references/schema.example.json --key id --apply
```
