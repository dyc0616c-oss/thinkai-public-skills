#!/usr/bin/env python3
import argparse, json, re, subprocess
from pathlib import Path

SECRET_NAMES = re.compile(r"(?i)(^|/)(\.env|id_rsa|id_ed25519|credentials|secrets?\.json|.*\.pem)$")

def git(repo, *args):
    return subprocess.run(["git", "-C", str(repo), *args], text=True, capture_output=True, check=False)

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--repo", default=".")
    p.add_argument("--policy", default=".skill-git-policy.json")
    args = p.parse_args()
    repo = Path(args.repo).resolve()
    if git(repo, "rev-parse", "--is-inside-work-tree").stdout.strip() != "true":
        raise SystemExit("not a git work tree")
    policy_path = repo / args.policy
    policy = {"protected_branches": ["main", "master"], "allowed_branch_patterns": [r"^(feat|feature|fix|bugfix|hotfix|docs|chore)/.+$"], "require_identity": True}
    if policy_path.exists():
        policy.update(json.loads(policy_path.read_text(encoding="utf-8")))
    branch = git(repo, "branch", "--show-current").stdout.strip()
    status_lines = [x for x in git(repo, "status", "--porcelain=v1").stdout.splitlines() if x]
    name = git(repo, "config", "user.name").stdout.strip()
    email = git(repo, "config", "user.email").stdout.strip()
    issues = []
    if branch in policy["protected_branches"] and status_lines:
        issues.append({"level": "warning", "code": "dirty-protected-branch", "message": f"{branch} has local changes"})
    if branch and branch not in policy["protected_branches"] and not any(re.match(x, branch) for x in policy["allowed_branch_patterns"]):
        issues.append({"level": "info", "code": "branch-pattern", "message": f"branch does not match configured patterns: {branch}"})
    if policy.get("require_identity") and (not name or not email):
        issues.append({"level": "warning", "code": "identity-missing", "message": "git user.name or user.email is missing"})
    for line in status_lines:
        path = line[3:].strip().strip('"')
        if SECRET_NAMES.search(path):
            issues.append({"level": "high", "code": "possible-secret-file", "message": f"sensitive-looking uncommitted file: {path}"})
    result = {"repo": str(repo), "branch": branch, "identity": {"name": name, "email": email}, "changed_files": len(status_lines), "issues": issues, "mutations": []}
    print(json.dumps(result, ensure_ascii=False, indent=2))
    raise SystemExit(1 if any(x["level"] == "high" for x in issues) else 0)

if __name__ == "__main__":
    main()
