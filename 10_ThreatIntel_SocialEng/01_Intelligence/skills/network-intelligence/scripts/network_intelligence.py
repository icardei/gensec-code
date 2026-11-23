from __future__ import annotations

import json
import os
import sys

import requests


def main() -> int:
    if len(sys.argv) != 2:
        print(json.dumps({"error": "usage: network_intelligence.py <ip-address>"}))
        return 2

    address = sys.argv[1].strip()
    virustotal_api_key = os.getenv("VIRUSTOTAL_API_KEY")

    output: dict[str, object] = {"address": address}

    ipwho = requests.get(f"http://ipwho.is/{address}", timeout=30)
    output["ipwhois"] = ipwho.json() if ipwho.ok else {"error": ipwho.text}

    if virustotal_api_key:
        vt = requests.get(
            f"https://www.virustotal.com/api/v3/ip_addresses/{address}",
            headers={"x-apikey": virustotal_api_key},
            timeout=30,
        )
        output["virustotal"] = vt.json() if vt.ok else {"error": vt.text}
    else:
        output["virustotal"] = {"error": "VIRUSTOTAL_API_KEY not set"}

    print(json.dumps(output, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
