
import os
import subprocess
import sys

# Set credentials securely
os.environ["TWINE_USERNAME"] = "barham-agha"
os.environ["TWINE_PASSWORD"] = "X.nm2r,?jr_F3h_"
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
