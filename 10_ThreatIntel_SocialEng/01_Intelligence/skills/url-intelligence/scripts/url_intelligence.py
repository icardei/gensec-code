from __future__ import annotations

import json
import os
import sys

import requests


def main() -> int:
    if len(sys.argv) != 2:
        print(json.dumps({"error": "usage: url_intelligence.py <url>"}))
        return 2

    url = sys.argv[1].strip()
    google_api_key = os.getenv("GOOGLE_API_KEY")
    virustotal_api_key = os.getenv("VIRUSTOTAL_API_KEY")

    output: dict[str, object] = {"url": url}

    if google_api_key:
        safe = requests.post(
            f"https://safebrowsing.googleapis.com/v4/threatMatches:find?key={google_api_key}",
            json={
                "client": {"clientId": "PSU", "clientVersion": "1.0"},
                "threatInfo": {
                    "threatTypes": [
                        "MALWARE",
                        "SOCIAL_ENGINEERING",
                        "UNWANTED_SOFTWARE",
                        "POTENTIALLY_HARMFUL_APPLICATION",
                    ],
                    "platformTypes": ["ANY_PLATFORM"],
                    "threatEntryTypes": ["URL"],
                    "threatEntries": [{"url": url}],
                },
            },
            timeout=30,
        )
        output["safe_browsing"] = safe.json() if safe.ok else {"error": safe.text}
    else:
        output["safe_browsing"] = {"error": "GOOGLE_API_KEY not set"}

    if virustotal_api_key:
        vt_submit = requests.post(
            "https://www.virustotal.com/api/v3/urls",
            headers={"x-apikey": virustotal_api_key},
            data={"url": url},
            timeout=30,
        )
        if vt_submit.ok:
            vt_data = vt_submit.json()
            link = vt_data.get("data", {}).get("links", {}).get("self") if isinstance(vt_data, dict) else None
            if link:
                vt_report = requests.get(link, headers={"x-apikey": virustotal_api_key}, timeout=30)
                output["virustotal"] = vt_report.json() if vt_report.ok else {"error": vt_report.text}
            else:
                output["virustotal"] = vt_data
        else:
            output["virustotal"] = {"error": vt_submit.text}
    else:
        output["virustotal"] = {"error": "VIRUSTOTAL_API_KEY not set"}

    phishtank = requests.post(
        "https://checkurl.phishtank.com/checkurl/",
        headers={"User-Agent": f"phishtank/{os.getenv('USER', 'unknown')}"},
        data={"format": "json", "url": url},
        timeout=30,
    )
    output["phishtank"] = phishtank.json() if phishtank.ok else {"error": phishtank.text}

    print(json.dumps(output, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
