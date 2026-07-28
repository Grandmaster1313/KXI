import subprocess
from datetime import datetime


def run(command):
    print(f">>> {command}")
    return subprocess.run(
        command,
        shell=True,
        capture_output=True,
        text=True
    )


# ---------------------------------------------------
# Check if anything actually changed
# ---------------------------------------------------

status = run("git status --porcelain")

if status.stdout.strip() == "":
    print("No changes detected. Skipping Git publish.")
    exit(0)


# ---------------------------------------------------
# Publish only when changes exist
# ---------------------------------------------------

timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")

run("git add .")

run(f'git commit -m "Auto update {timestamp}"')

run("git pull --rebase")

push = run("git push")


# ---------------------------------------------------
# Display Git output
# ---------------------------------------------------

if push.stdout.strip():
    print(push.stdout)

if push.stderr.strip():
    print(push.stderr)