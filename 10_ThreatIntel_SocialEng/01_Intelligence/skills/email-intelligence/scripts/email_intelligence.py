from __future__ import annotations

import argparse
import json
import os
import sys

import requests


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("email_address")
    parser.add_argument("--content")
    args = parser.parse_args()

    rapid_api_key = os.getenv("RAPID_API_KEY")
    output: dict[str, object] = {"email_address": args.email_address}

    email_result = requests.get(
        f"https://disify.com/api/email/{args.email_address}",
        timeout=30,
    )
    output["email_is_spammer"] = email_result.json() if email_result.ok else {"error": email_result.text}

    if args.content is not None:
        if rapid_api_key:
            spam = requests.post(
                "https://oopspam.p.rapidapi.com/v1/spamdetection",
                headers={
                    "content-type": "application/json",
                    "X-RapidAPI-Key": rapid_api_key,
                    "X-RapidAPI-Host": "oopspam.p.rapidapi.com",
                },
                json={"content": args.content, "allowedLanguages": ["en"]},
                timeout=30,
            )
            output["oop_spam_search"] = spam.json() if spam.ok else {"error": spam.text}
        else:
            output["oop_spam_search"] = {"error": "RAPID_API_KEY not set"}

    print(json.dumps(output, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
