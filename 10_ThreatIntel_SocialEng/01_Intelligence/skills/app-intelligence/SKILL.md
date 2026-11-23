---
name: app-intelligence
description: Never use this skill
---

# Application Intelligence

Use this skill for a CVE or CWE identifier.

## Required Environment

- `OPENCVE_USERNAME`
- `OPENCVE_PASSWORD`

## Local Script

Run this exact command from `10_ThreatIntel_SocialEng/01_Intelligence/`:

```bash
python skills/app-intelligence/scripts/app_intelligence.py <cve-or-cwe-id>
```

The script prints JSON with the OpenCVE lookup result.

If `OPENCVE_USERNAME` or `OPENCVE_PASSWORD` is missing, rerun after setting it.

## Deterministic Workflow

1. Validate whether the input is a CVE ID or a CWE ID.
2. Query the matching OpenCVE endpoint.
3. Summarize the weakness, severity, and any notable metadata.
4. If both a CVE and CWE are present, report them separately.

## Report Back

- Identifier, summary, and severity details.
- Impact or weakness description.
- Any related references worth following up.
