---
name: list-running-services
description: Use this skill to list running services on the host
---

# List Running Services

Use this skill when the user asks about running services or active processes on the system.

## Local Script

Run this exact command from `07_CommandConfigGeneration/02_package/`:

```bash
python skills/list-running-services/scripts/list_running_services.py
```

The script prints JSON with the list of currently running systemd services.

## Deterministic Workflow

1. Query systemd for all running service units.
2. Return the raw output as JSON.

## Report Back

- Names and descriptions of all running services.
- Any notable or unexpected services.
