import subprocess
import sys
import time
from pathlib import Path
from datetime import datetime

# -------------------------------------------------------
# KXI Scheduler
# -------------------------------------------------------

ROOT = Path(__file__).resolve().parent

DASHBOARD_SCRIPT = ROOT / "gold_dashboard.py"
AUTO_PUBLISH_SCRIPT = ROOT / "auto_publish.py"

print("=" * 60)
print("KXI HEARTBEAT MONITOR STARTED")
print("=" * 60)
print(f"Scheduler Folder : {ROOT}")
print()

while True:

    start = time.time()

    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S CST")

    print("=" * 60)
    print(f"[{now}] Update started")

    try:

        # ----------------------------
        # Generate dashboard
        # ----------------------------
        result = subprocess.run(
            [sys.executable, str(DASHBOARD_SCRIPT)],
            cwd=str(ROOT),
            timeout=60,
            capture_output=True,
            text=True
        )

        if result.returncode == 0:
            print("✓ Dashboard updated successfully")
        else:
            print(f"✗ Dashboard failed (Exit Code {result.returncode})")

        if result.stdout.strip():
            print("\n----- Dashboard Output -----")
            print(result.stdout.strip())

        if result.stderr.strip():
            print("\n----- Dashboard Errors -----")
            print(result.stderr.strip())

        # ----------------------------
        # Publish to GitHub
        # ----------------------------
        publish = subprocess.run(
            [sys.executable, str(AUTO_PUBLISH_SCRIPT)],
            cwd=str(ROOT),
            timeout=60,
            capture_output=True,
            text=True
        )

        if publish.stdout.strip():
            print("\n----- Git Publish -----")
            print(publish.stdout.strip())

        if publish.stderr.strip():
            print("\n----- Git Publish Errors -----")
            print(publish.stderr.strip())

        elapsed = time.time() - start

        print()
        print(f"Completed in {elapsed:.2f} seconds")

    except Exception as e:
        print()
        print("Scheduler Error:")
        print(e)

    print()
    print("Waiting 30 seconds...")
    print()

    time.sleep(30)