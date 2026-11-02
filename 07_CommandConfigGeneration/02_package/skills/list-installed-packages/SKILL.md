---
name: list-installed-packages
description: Use this skill to list installed packages and their versions on the host
---

# List Installed Packages

Use this skill when the user asks about installed software, package versions, or what is installed on the system.

## Local Script

Run this exact command from `07_CommandConfigGeneration/02_package/`:

```bash
python skills/list-installed-packages/scripts/list_installed_packages.py
```

The script prints JSON with all installed packages and their versions.

## Deterministic Workflow

1. Query dpkg for all installed packages and versions.
2. Return the raw output as JSON.

## Report Back

- Names and versions of all installed packages.
- Highlight any packages that look outdated or unusual.
