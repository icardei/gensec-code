from __future__ import annotations

import json
import os
import sys

import requests


def main() -> int:
    if len(sys.argv) != 2:
        print(json.dumps({"error": "usage: app_intelligence.py <cve-or-cwe-id>"}))
        return 2

    identifier = sys.argv[1].strip()
    username = os.getenv("OPENCVE_USERNAME")
    password = os.getenv("OPENCVE_PASSWORD")

    output: dict[str, object] = {"identifier": identifier}

    if not username or not password:
        print(json.dumps({"error": "OPENCVE_USERNAME and OPENCVE_PASSWORD must be set"}))
        return 1

    if identifier.upper().startswith("CVE-"):
        url = f"https://app.opencve.io/api/cve/{identifier}"
    elif identifier.upper().startswith("CWE-"):
        url = f"https://app.opencve.io/api/weaknesses/{identifier}"
    else:
        print(json.dumps({"error": "identifier must start with CVE- or CWE-"}))
        return 2

    response = requests.get(url, auth=(username, password), timeout=30)
    output["result"] = response.json() if response.ok else {"error": response.text}

    print(json.dumps(output, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
