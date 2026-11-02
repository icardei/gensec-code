import subprocess
import sys

result = subprocess.run(sys.argv[1:], capture_output=True, text=True)
print(f"stdout: {result.stdout}\nstderr: {result.stderr}\nreturncode: {result.returncode}")
