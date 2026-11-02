---
name: list-package-vulnerabilities
description: Use this skill to look up the changelog and vulnerabilities for a specific package
---

# List Package Vulnerabilities

Use this skill when the user asks about vulnerabilities, security issues, or the changelog for a specific package by name.

## Local Script

Run this exact command from `07_CommandConfigGeneration/02_package/`:

```bash
python skills/list-package-vulnerabilities/scripts/list_package_vulnerabilities.py <package-name>
```

The script prints JSON with the apt changelog for the package, including patch authors and security fixes.

## Deterministic Workflow

1. Run `apt changelog` for the given package name.
2. Return the raw changelog output as JSON.

## Report Back

- Security-related changelog entries (look for CVE references).
- Authors of recent updates.
- Whether any known vulnerabilities have been patched.
