---
name: git-safety-check
description: Perform a read-only Git repository safety and policy audit before commits, pushes, branch changes, or merge requests. Use when checking protected branches, dirty state, identity configuration, untracked secrets, and project-specific branch rules without modifying Git state or contacting an internal service.
---

# Git Safety Check

Run `scripts/git_safety_check.py` in the target repository.

- Use only read-only Git commands.
- Load optional rules from `.skill-git-policy.json`.
- Report issues by default; never block, commit, push, merge, checkout, or change Git config.
- Do not query employee directories or validate organization-specific identities remotely.

```bash
python3 scripts/git_safety_check.py --repo /path/to/repo
```
