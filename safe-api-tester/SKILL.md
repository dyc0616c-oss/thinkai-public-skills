---
name: safe-api-tester
description: Run allowlisted HTTP API checks from CSV and generate a local redacted HTML report. Use when testing localhost, development, or explicitly approved API endpoints; default to GET and HEAD, block write methods and non-allowlisted hosts unless the user deliberately enables them.
---

# Safe API Tester

Use `scripts/api_tester.py`.

1. Start with `localhost` or explicit `--allow-host` values.
2. Keep GET/HEAD only unless the user explicitly requests writes.
3. For POST/PUT/PATCH/DELETE, require both `--allow-write` and `--confirm-write I_UNDERSTAND`.
4. Never add automatic SQL injection, XSS, fuzzing, or credential attacks.
5. Save reports locally and redact authorization, cookie, token, password, and secret fields.
6. Do not send reports through email or chat automatically.

CSV columns: `name,method,url,expected_status,body`.

```bash
python3 scripts/api_tester.py tests.csv --allow-host localhost --report report.html
```
