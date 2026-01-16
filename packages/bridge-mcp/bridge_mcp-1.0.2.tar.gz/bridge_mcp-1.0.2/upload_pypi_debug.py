
import os
import subprocess
import sys

# Set credentials securely
os.environ["TWINE_USERNAME"] = "barham-agha"
os.environ["TWINE_PASSWORD"] = "X.nm2r,?jr_F3h_"
os.environ["TWINE_NON_INTERACTIVE"] = "1"

print("Starting upload to PyPI...")
with open("pypi_upload_log.txt", "w") as f:
    try:
        # Run twine upload
        cmd = [sys.executable, "-m", "twine", "upload", "dist/*", "--skip-existing", "--verbose"]
        result = subprocess.run(cmd, check=True, capture_output=True, text=True)
        f.write("Upload successful!\n")
        f.write(result.stdout)
        print("Upload successful!")
    except subprocess.CalledProcessError as e:
        f.write("Upload FAILED!\n")
        f.write("STDOUT:\n")
        f.write(e.stdout)
        f.write("\nSTDERR:\n")
        f.write(e.stderr)
        print("Upload FAILED! Check pypi_upload_log.txt")
        sys.exit(1)
