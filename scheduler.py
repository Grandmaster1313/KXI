import subprocess
import sys
import time
from pathlib import Path
from datetime import datetime

# ----------------------------------------------------
# KXI Scheduler
# ----------------------------------------------------

ROOT = Path(__file__).resolve().parent
DASHBOARD_SCRIPT = ROOT / "gold_dashboard.py"

print("=" * 60)
print("KXI HEARTBEAT MONITOR STARTED")
print("=" * 60)
print(f"Scheduler Folder : {ROOT}")
print(f"Dashboard Script : {DASHBOARD_SCRIPT}")
print()

while True:

    start = time.time()

    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S CST")

    print("=" * 60)
    print(f"[{now}] Update started")

    try:

        result = subprocess.run(
            [sys.executable, str(DASHBOARD_SCRIPT)],
            cwd=str(ROOT),
            timeout=60,
            capture_output=True,
            text=True
        )

        elapsed = time.time() - start

        if result.returncode == 0:

            print(f"✓ Dashboard updated successfully ({elapsed:.2f} sec)")

        else:

            print(f"✗ Dashboard failed (Exit Code {result.returncode})")

        if result.stdout.strip():
            print("\n----- Dashboard Output -----")
            print(result.stdout.strip())

        if result.stderr.strip():
            print("\n----- Dashboard Errors -----")
            print(result.stderr.strip())

    except subprocess.TimeoutExpired:

        print("✗ ERROR: Dashboard update timed out after 60 seconds.")

    except Exception as e:

        print(f"✗ ERROR: {e}")

    next_run = datetime.now().strftime("%H:%M:%S CST")

    print()
    print("Heartbeat : OK")
    print(f"Next update : {next_run} + 30 sec")
    print("=" * 60)
    print()

    time.sleep(30)