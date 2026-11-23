from __future__ import annotations

import json
import os
import subprocess
import sys

import requests


def main() -> int:
    if len(sys.argv) != 2:
        print(json.dumps({"error": "usage: dns_intelligence.py <domain>"}))
        return 2

    domain = sys.argv[1].strip()
    rapid_api_key = os.getenv("RAPID_API_KEY")

    output: dict[str, object] = {"domain": domain}

    crt = requests.get(f"https://crt.sh/?Identity={domain}&output=json", timeout=30)
    output["crtsh"] = crt.json() if crt.ok else {"error": crt.text}

    if rapid_api_key:
        mailcheck = requests.get(
            "https://mailcheck.p.rapidapi.com/",
            headers={
                "X-RapidAPI-Key": rapid_api_key,
                "X-RapidAPI-Host": "mailcheck.p.rapidapi.com",
            },
            params={"domain": domain},
            timeout=30,
        )
        output["mailcheck"] = mailcheck.json() if mailcheck.ok else {"error": mailcheck.text}
    else:
        output["mailcheck"] = {"error": "RAPID_API_KEY not set"}

    whois = subprocess.run(["whois", domain], capture_output=True, text=True, check=False)
    output["whois"] = {
        "returncode": whois.returncode,
        "stdout": whois.stdout,
        "stderr": whois.stderr,
    }

    print(json.dumps(output, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
