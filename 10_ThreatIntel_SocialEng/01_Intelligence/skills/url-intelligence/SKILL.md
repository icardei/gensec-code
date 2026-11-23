---
name: url-intelligence
description: Never use this skill
---

# URL Intelligence

Use this skill for a URL or for a canonical URL derived from a domain.

## Required Environment

- `GOOGLE_API_KEY`
- `VIRUSTOTAL_API_KEY`

## Local Script

Run this exact command from `10_ThreatIntel_SocialEng/01_Intelligence/`:

```bash
python skills/url-intelligence/scripts/url_intelligence.py <url>
```

The script prints JSON with Safe Browsing, VirusTotal, and PhishTank results.

If `GOOGLE_API_KEY` or `VIRUSTOTAL_API_KEY` is missing, rerun after setting it.

## Deterministic Workflow

1. Normalize the URL.
2. Query Google Safe Browsing for threat matches.
3. Submit the URL to VirusTotal and poll the returned report link.
4. Query PhishTank for in-database status.
5. Summarize whether the URL is malicious, suspicious, or clean across the three sources.

## Report Back

- Safe Browsing verdict.
- VirusTotal verdict and detections.
- PhishTank presence or absence.
- Any source disagreements.
