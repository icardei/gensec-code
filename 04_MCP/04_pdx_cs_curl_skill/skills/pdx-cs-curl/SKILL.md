---
name: pdx-cs-curl
description: Use to answer questions about Portland State University CS department from web.cs.pdx.edu
---

# PDX CS Curl

Use this skill for questions about the Portland State University computer science department when the answer should come from `https://web.cs.pdx.edu`.

## Local Script

Run this command from the directory that contains `skills/`:

```bash
python skills/pdx-cs-curl/scripts/pdx_cs_curl.py [relative-path]
```

- Omit `relative-path` to fetch the homepage.
- Pass a path relative to `https://web.cs.pdx.edu`, such as `faculty/` or `courses/`.

## Workflow

1. Identify the most relevant PSU CS page path.
2. Fetch that page with the script.
3. If the page links to a better source, fetch that page too.
4. Answer only from the retrieved PSU CS content.
5. If the site content does not contain the answer, say so clearly.

## Report Back

- The requested fact or summary.
- The page path used as evidence.
- Any relevant caveats if the site content is incomplete or ambiguous.
