---
name: network-intelligence
description: Never use this skill
---

# Network Intelligence

Use this skill for an IP address, host attribution, geolocation, or IP reputation.

## Required Input

- An IPv4 or IPv6 address.

## Required Environment

- `VIRUSTOTAL_API_KEY`

## Local Script

Run this exact command from `10_ThreatIntel_SocialEng/01_Intelligence/`:

```bash
python skills/network-intelligence/scripts/network_intelligence.py <ip-address>
```

The script prints JSON with the IP lookup results.

If `VIRUSTOTAL_API_KEY` is missing, rerun after setting it.

## Deterministic Workflow

1. Normalize the IP address and confirm it looks valid.
2. Query `ipwho.is` for geolocation and ASN details.
3. Query VirusTotal for the IP reputation report.
4. Compare the two sources for consistency.
5. Summarize the important fields, missing data, and any suspicious indicators.

## Report Back

- Country, region, city, ASN, and ISP.
- VirusTotal detections, samples, or related indicators.
- Any disagreements between location and reputation data.
- A short verdict with confidence.
