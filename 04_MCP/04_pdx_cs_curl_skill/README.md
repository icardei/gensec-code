# PDX CS Curl

This exercise now uses a local skill plus an interactive agent client.

## Files

- `skills/pdx-cs-curl/SKILL.md`
- `skills/pdx-cs-curl/scripts/pdx_cs_curl.py`
- `pdx_cs_curl_client.py`

## Setup

```bash
pip install -r requirements.txt
```

## Run

From this directory:

```bash
python pdx_cs_curl_client.py
```

Then ask questions about the Portland State University computer science department.

The agent uses the `pdx-cs-curl` skill to fetch pages from `https://web.cs.pdx.edu`.
