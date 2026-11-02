from __future__ import annotations

import json
import subprocess
import sys


def main() -> int:
    if len(sys.argv) != 2:
        print(json.dumps({"error": "usage: list_package_vulnerabilities.py <package-name>"}))
        return 2

    package = sys.argv[1].strip()
    result = subprocess.run(
        ["apt", "changelog", package],
        capture_output=True,
        text=True,
        check=False,
    )
    output = {
        "package": package,
        "returncode": result.returncode,
        "stdout": result.stdout,
        "stderr": result.stderr,
    }
    print(json.dumps(output, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
