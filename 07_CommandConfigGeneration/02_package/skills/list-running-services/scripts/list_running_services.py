from __future__ import annotations

import json
import subprocess
import sys


def main() -> int:
    result = subprocess.run(
        ["systemctl", "list-units", "--type=service", "--state=running"],
        capture_output=True,
        text=True,
        check=False,
    )
    output = {
        "returncode": result.returncode,
        "stdout": result.stdout,
        "stderr": result.stderr,
    }
    print(json.dumps(output, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
