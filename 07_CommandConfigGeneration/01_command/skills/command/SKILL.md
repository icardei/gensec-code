---
name: command
description: Runs an arbitrary command and returns its output
---

# Command

Use this skill to execute a shell command and capture its output.

## Local Script

Run this exact command from `07_CommandConfigGeneration/01_command/`:

```bash
python skills/command/scripts/command.py <command> [args...]
```

The script prints stdout, stderr, and the return code.

## Deterministic Workflow

1. Split the requested command into program and arguments.
2. Run `python skills/command/scripts/command.py <program> [args...]`.
3. Report stdout, stderr, and return code to the user.
