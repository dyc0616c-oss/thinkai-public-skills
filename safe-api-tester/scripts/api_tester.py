#!/usr/bin/env python3
import argparse, csv, html, json, re, urllib.error, urllib.parse, urllib.request
from pathlib import Path

SAFE_METHODS = {"GET", "HEAD"}
WRITE_METHODS = {"POST", "PUT", "PATCH", "DELETE"}
SENSITIVE = re.compile(r"(?i)(authorization|cookie|token|password|secret|api[_-]?key)")

def redact(value):
    text = value if isinstance(value, str) else json.dumps(value, ensure_ascii=False)
    text = re.sub(r"(?i)(bearer\s+)[A-Za-z0-9._~+/=-]+", r"\1[REDACTED]", text)
    text = re.sub(r'(?i)(["\']?(?:token|password|secret|api[_-]?key)["\']?\s*[:=]\s*)["\']?[^,\s}"\']+', r'\1[REDACTED]', text)
    return text[:20000]

def allowed_host(host, allowlist):
    host = (host or "").lower().rstrip(".")
    return any(host == item or host.endswith("." + item) for item in allowlist)

def run_case(row, allowlist, timeout, allow_write, confirm):
    method = row.get("method", "GET").upper().strip()
    url = row["url"].strip()
    parsed = urllib.parse.urlparse(url)
    if parsed.scheme not in {"http", "https"}:
        return {"name": row.get("name", url), "ok": False, "error": "scheme blocked"}
    if not allowed_host(parsed.hostname, allowlist):
        return {"name": row.get("name", url), "ok": False, "error": f"host blocked: {parsed.hostname}"}
    if method not in SAFE_METHODS:
        if method not in WRITE_METHODS or not allow_write or confirm != "I_UNDERSTAND":
            return {"name": row.get("name", url), "ok": False, "error": f"method blocked: {method}"}
    data = row.get("body", "").encode() if row.get("body") else None
    request = urllib.request.Request(url, data=data, method=method, headers={"User-Agent": "ThinkAI-Safe-API-Tester/1.0", "Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:
            body = response.read(1024 * 1024).decode("utf-8", "replace")
            status = response.status
    except urllib.error.HTTPError as exc:
        status = exc.code
        body = exc.read(1024 * 1024).decode("utf-8", "replace")
    except Exception as exc:
        return {"name": row.get("name", url), "method": method, "url": url, "ok": False, "error": str(exc)}
    expected = int(row.get("expected_status") or 200)
    return {"name": row.get("name", url), "method": method, "url": url, "status": status, "expected": expected, "ok": status == expected, "body": redact(body)}

def render(results):
    rows = []
    for r in results:
        rows.append("<tr>" + "".join(f"<td>{html.escape(str(r.get(k,'')))}</td>" for k in ("name","method","url","status","expected","ok","error")) + "</tr>")
    details = "".join(f"<details><summary>{html.escape(str(r.get('name')))}</summary><pre>{html.escape(r.get('body',''))}</pre></details>" for r in results if r.get("body"))
    return "<!doctype html><meta charset='utf-8'><title>API Test Report</title><h1>API Test Report</h1><table border='1'><tr><th>Name</th><th>Method</th><th>URL</th><th>Status</th><th>Expected</th><th>Pass</th><th>Error</th></tr>" + "".join(rows) + "</table>" + details

def main():
    p = argparse.ArgumentParser()
    p.add_argument("csv_file")
    p.add_argument("--allow-host", action="append", default=["localhost", "127.0.0.1"])
    p.add_argument("--timeout", type=float, default=10)
    p.add_argument("--allow-write", action="store_true")
    p.add_argument("--confirm-write", default="")
    p.add_argument("--report", default="api-test-report.html")
    args = p.parse_args()
    allowlist = {x.lower().strip(".") for x in args.allow_host}
    with open(args.csv_file, newline="", encoding="utf-8-sig") as f:
        results = [run_case(row, allowlist, args.timeout, args.allow_write, args.confirm_write) for row in csv.DictReader(f)]
    out = Path(args.report).resolve()
    out.write_text(render(results), encoding="utf-8")
    print(json.dumps({"passed": sum(bool(x.get("ok")) for x in results), "total": len(results), "report": str(out)}, ensure_ascii=False))

if __name__ == "__main__":
    main()
