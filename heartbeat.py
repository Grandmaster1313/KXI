import subprocess
import time
import os
from datetime import datetime
from pathlib import Path
from hashlib import sha256

def play_alert():

    try:

        import winsound

        winsound.MessageBeep(winsound.MB_ICONEXCLAMATION)

    except Exception as e:

        print(f"Alert error: {e}")

# ============================================================
# KXI HEARTBEAT CONFIGURATION
# ============================================================
# ============================================================
# SINGLE INSTANCE PROTECTION
# ============================================================

LOCK_FILE = Path("heartbeat.lock")


def acquire_lock():

    if LOCK_FILE.exists():

        try:

            pid = int(LOCK_FILE.read_text().strip())

            os.kill(pid, 0)

            print("=" * 60)
            print("Heartbeat is already running.")
            print(f"PID: {pid}")
            print("=" * 60)

            raise SystemExit

        except OSError:
            pass

        except ValueError:
            pass

    LOCK_FILE.write_text(str(os.getpid()))


def release_lock():

    if LOCK_FILE.exists():

        try:
            LOCK_FILE.unlink()
        except Exception:
            pass
PYTHON_EXE = r"C:\Users\herna\OneDrive\Documents\KXI\venv312\Scripts\python.exe"

DASHBOARD_SCRIPT = "gold_dashboard.py"
AUTO_PUBLISH_SCRIPT = "auto_publish.py"

LOG_DIR = Path("logs")
LOG_DIR.mkdir(exist_ok=True)

MAX_ERRORS = 3
SLEEP_SECONDS = 30


# ============================================================
# LOG ROTATION
# ============================================================

def get_log_file():

    month = datetime.now().strftime("%Y-%m")

    return LOG_DIR / f"heartbeat_{month}.log"


def cleanup_logs():

    today = datetime.now()

    for file in LOG_DIR.glob("heartbeat_*.log"):

        try:

            file_date = datetime.strptime(
                file.stem.replace("heartbeat_", ""),
                "%Y-%m"
            )

            age_days = (today - file_date).days

            if age_days > 180:

                file.unlink()

                print(f"Deleted old log: {file.name}")

        except Exception:
            pass


# ============================================================
# WRITE LOG
# ============================================================

def write_log(message):

    log_file = get_log_file()

    timestamp = datetime.now().strftime(
        "%Y-%m-%d %H:%M:%S CST"
    )

    with open(log_file, "a", encoding="utf-8") as f:

        f.write(
            f"{timestamp} | {message}\n"
        )


# ============================================================
# STATUS FILE
# ============================================================

def write_status(
    status,
    cycles,
    updates,
    no_changes,
    errors,
    start_time
):

    status_file = Path("heartbeat_status.txt")

    runtime = datetime.now() - start_time

    with open(status_file, "w", encoding="utf-8") as f:

        f.write("KXI HEARTBEAT STATUS\n")
        f.write("====================\n")
        f.write(f"Status: {status}\n")
        f.write(f"Cycles: {cycles}\n")
        f.write(f"Updates: {updates}\n")
        f.write(f"No Changes: {no_changes}\n")
        f.write(f"Errors: {errors}\n")
        f.write(f"Runtime: {runtime}\n")
        f.write(f"Last Check: {datetime.now()}\n")


# ============================================================
# AUTO PUBLISH
# ============================================================

def auto_publish():

    try:

        result = subprocess.run(
            [
                PYTHON_EXE,
                AUTO_PUBLISH_SCRIPT
            ],
            capture_output=True,
            text=True
        )

        if result.returncode == 0:

            print("GitHub auto-publish completed.")

            write_log("GITHUB UPDATED")

        else:

            print("GitHub auto-publish failed.")

            if result.stderr.strip():
                print(result.stderr)

            write_log("GITHUB UPDATE FAILED")

    except Exception as e:

        print(f"Auto publish exception: {e}")

        write_log(f"GITHUB EXCEPTION: {e}")


# ============================================================
# HEARTBEAT ENGINE
# ============================================================

cycles = 0
updates = 0
no_changes = 0
errors = 0

last_macro_state = None

start_time = datetime.now()

cleanup_logs()

print("=" * 60)
print("KXI HEARTBEAT STARTED")
print("=" * 60)
acquire_lock()

try:

    while True:

        cycles += 1

        try:

            result = subprocess.run(
                [
                    PYTHON_EXE,
                    DASHBOARD_SCRIPT
                ],
                capture_output=True,
                text=True
            )

            if result.returncode == 0:

                state_file = Path("macro_bias_state.txt")

                if state_file.exists():

                    current_state = state_file.read_text(
                        encoding="utf-8"
                    ).strip()

                    if last_macro_state is None:

                        print("Initial macro state loaded.")

                        last_macro_state = current_state
                        no_changes += 1

                        write_log("INITIAL MACRO STATE")

                    elif current_state != last_macro_state:

                        updates += 1
                        last_macro_state = current_state

                        print(
                            f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S CST')}] "
                            "MACRO STATE CHANGED"
                        )

                        play_alert()
                        auto_publish()
                        write_log("MACRO STATE CHANGED")

                    else:

                        no_changes += 1
                        write_log("NO MACRO CHANGE")

                else:

                    no_changes += 1
                    write_log("macro_bias_state.txt NOT FOUND")

                errors = 0

            else:

                errors += 1

                print(
                    f"Dashboard error {errors}/{MAX_ERRORS}"
                )

                if result.stderr.strip():
                    print(result.stderr)

                write_log("ERROR")

            write_status(
                "ONLINE",
                cycles,
                updates,
                no_changes,
                errors,
                start_time
            )

        except Exception as e:

            errors += 1

            print(
                f"ERROR {errors}/{MAX_ERRORS}"
            )

            print(e)

            write_log(f"ERROR: {e}")

        print(f"Sleeping {SLEEP_SECONDS} seconds...")

        time.sleep(SLEEP_SECONDS)

except KeyboardInterrupt:

    print()
    print("=" * 60)
    print("KXI HEARTBEAT STOPPED")
    print("=" * 60)

    print(f"Cycles: {cycles}")
    print(f"Updates: {updates}")
    print(f"No Changes: {no_changes}")
    print(f"Errors: {errors}")

    release_lock()

    print("=" * 60)