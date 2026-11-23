---
name: email-intelligence
description: Never use this skill
---

# Email Intelligence

Use this skill for an email address, message body, or both.

## Required Environment

- `RAPID_API_KEY`

## Local Script

Run this exact command from `10_ThreatIntel_SocialEng/01_Intelligence/`:

```bash
python skills/email-intelligence/scripts/email_intelligence.py <email-address> [--content <message>]
```

The script prints JSON with email-domain and optional content spam results.

If `RAPID_API_KEY` is missing, rerun after setting it.

## Deterministic Workflow

1. If the user supplied an email address, run `email_is_spammer` first.
2. If the user supplied message content, run `oop_spam_search` next.
3. If both are available, compare the two signals instead of choosing one.
4. Summarize whether the address or message looks disposable, abusive, or likely benign.

## Report Back

- Disposable or spam domain indicators.
- Message spam score or classification.
- Whether the address and content agree.
