
import os
import subprocess
import sys

# Set credentials securely
os.environ["TWINE_USERNAME"] = "__token__"
os.environ["TWINE_PASSWORD"] = "pypi-AgEIcHlwaS5vcmcCJDgwMjdiZWI1LWU0OTEtNDZkZC04ZTU3LTQzNDA0YzA5MjE4MgACKlszLCIwMTAwMTg3Ny1mYTBkLTQyMTMtYmIwOC04OTJjYjZiMDUwZDEiXQAABiB0-Uw54L91Zqn6HWzTGVOdyYMEz_4Ocwo-dhAc7rAcLQ"
os.environ["TWINE_NON_INTERACTIVE"] = "1"

print("Starting upload to PyPI...")
try:
    # Run twine upload
    cmd = [sys.executable, "-m", "twine", "upload", "dist/*", "--skip-existing", "--verbose"]
    result = subprocess.run(cmd, check=True, capture_output=True, text=True)
    print("Upload successful!")
    print(result.stdout)
except subprocess.CalledProcessError as e:
    print("Upload FAILED!")
    print("STDOUT:", e.stdout)
    print("STDERR:", e.stderr)
    sys.exit(1)
