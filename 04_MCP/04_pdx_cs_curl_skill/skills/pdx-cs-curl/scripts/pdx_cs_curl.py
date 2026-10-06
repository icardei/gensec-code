from __future__ import annotations

import subprocess
import sys
from urllib.parse import urljoin, urlparse


BASE_URL = "https://web.cs.pdx.edu/"


def main() -> int:
    if len(sys.argv) > 2:
        print("usage: pdx_cs_curl.py [relative-path]", file=sys.stderr)
        return 2

    relative_path = sys.argv[1] if len(sys.argv) == 2 else ""
    parsed = urlparse(relative_path)
    if parsed.scheme or parsed.netloc:
        print("relative-path must not be an absolute URL", file=sys.stderr)
        return 2

    relative_path = parsed.path.lstrip("/")
    if any(part == ".." for part in relative_path.split("/")):
        print("relative-path must not contain '..' segments", file=sys.stderr)
        return 2

    url = urljoin(BASE_URL, relative_path)

    result = subprocess.run(
        ["curl", "--silent", "--show-error", "--fail", "--location", url],
        capture_output=True,
        text=True,
    )

    if result.returncode != 0:
        message = result.stderr.strip() or f"curl failed with exit code {result.returncode}"
        print(message, file=sys.stderr)
        return result.returncode

    print(result.stdout, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
