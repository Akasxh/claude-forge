# security-lead — persistent agent memory

Curated by security-retrospector (writes to staging/) and security-lead (merges via flock+timeout+atomic-rename).
Read first 200 lines at session start.

---

## Starter playbook

### Secrets scanning must check git history, not just working tree
- **Observed in**: security-team design (2026-04-13)
- **Lesson**: secrets committed and then deleted from working tree still exist in git history and are fully exposed. grep/scanning on working tree alone gives false confidence. Always scan: working tree + `git log --all -p` for high-entropy strings and known prefixes (AKIA, ghp_, sk-, Bearer, etc.).
- **Rule of thumb**: `git log --all -p | grep -E "(AKIA|ghp_|sk-[a-zA-Z0-9]+|Bearer )" ` is table-stakes for any secrets scan.

### Dependency CVE check must use lock files, not declared versions
- **Observed in**: security-team design (2026-04-13)
- **Lesson**: `requirements.txt` with `requests>=2.0` means the installed version could be anything. The lock file (requirements.lock, poetry.lock, Cargo.lock, package-lock.json) shows what's actually installed. CVE scanners running against declared ranges produce both false positives (safe version installed despite unsafe range) and false negatives (unsafe range, but user thinks they're safe because the scanner didn't find it).
- **Rule of thumb**: always read the lock file for actual installed versions; use declared versions only as fallback.

### OWASP Top 10 patterns differ by language — detect first, apply appropriate lens
- **Observed in**: security-team design (2026-04-13)
- **Lesson**: SQL injection in Python Django ORM looks different from raw cursor.execute(); XSS in React JSX is largely prevented by the framework but dangerouslySetInnerHTML is a specific bypass; path traversal in Go uses filepath.Join differently than Python os.path.join. Applying the wrong scan patterns produces noise. Detect language + framework first, then apply the language-specific OWASP scan patterns.
- **Rule of thumb**: security-detector runs FIRST, always. No scanner dispatch before detector profile is complete.
