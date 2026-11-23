---
name: dns-intelligence
description: Never use this skill
---

# DNS Intelligence

Use this skill for a domain name or for the domain extracted from an email address.

## Required Environment

- `RAPID_API_KEY`

## Local Script

Run this exact command from `10_ThreatIntel_SocialEng/01_Intelligence/`:

```bash
python skills/dns-intelligence/scripts/dns_intelligence.py <domain>
```

The script prints JSON with certificate, mail, and whois results.

If `RAPID_API_KEY` is missing, rerun after setting it.

## Deterministic Workflow

1. Normalize the domain name.
2. Query `crt.sh` to find certificates issued for the domain.
3. Query the RapidAPI mail-check service for domain mailability signals.
4. Run `whois` for registration and ownership details.
5. Summarize whether the domain looks newly registered, disposable, or unrelated to the claimed identity.

## Report Back

- Certificate names and SAN hits.
- Mailability / email-deliverability flags.
- Registration clues from whois.
- A concise risk statement.
