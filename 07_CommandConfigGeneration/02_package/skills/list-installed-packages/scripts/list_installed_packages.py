from __future__ import annotations

import json
import subprocess
import sys


def main() -> int:
    result = subprocess.run(
        ["dpkg-query", "-W", "-f=${Package} ${Version}\n"],
        capture_output=True,
        text=True,
        check=False,
    )
    packages = []
    for line in result.stdout.splitlines():
        parts = line.split(None, 1)
        if len(parts) == 2:
            packages.append({"name": parts[0], "version": parts[1]})
    output = {
        "count": len(packages),
        "packages": packages,
    }
    print(json.dumps(output, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
