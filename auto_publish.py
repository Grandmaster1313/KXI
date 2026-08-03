import subprocess
from datetime import datetime


# ==========================================================
# Execute a Git command
# ==========================================================

def run(command):
    print(f">>> {command}")

    result = subprocess.run(
        command,
        shell=True,
        capture_output=True,
        text=True
    )

    if result.stdout.strip():
        print(result.stdout)

    if result.stderr.strip():
        print(result.stderr)

    return result


# ==========================================================
# Publish dashboard
# ==========================================================

def publish():

    print("=" * 60)
    print("CLEON AUTO PUBLISH")
    print("=" * 60)

    # ------------------------------------------------------
    # Check for changes
    # ------------------------------------------------------

    status = run("git status --porcelain")

    if status.returncode != 0:
        print("ERROR: Unable to read Git status.")
        return False

    if status.stdout.strip() == "":
        print("No changes detected.")
        return False

    # ------------------------------------------------------
    # Stage changes
    # ------------------------------------------------------

    add = run("git add .")

    if add.returncode != 0:
        print("ERROR: git add failed.")
        return False

    # ------------------------------------------------------
    # Commit
    # ------------------------------------------------------

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    commit = run(
        f'git commit -m "CLEON Dashboard {timestamp} CST"'
    )

    # Nothing to commit is OK

    if commit.returncode != 0:

        combined = (
            commit.stdout.lower() +
            commit.stderr.lower()
        )

        if "nothing to commit" in combined:
            print("Nothing new to publish.")
            return False

        print("ERROR: git commit failed.")
        return False

    # ------------------------------------------------------
    # Synchronize with GitHub
    # ------------------------------------------------------

    pull = run("git pull --rebase")

    if pull.returncode != 0:
        print("ERROR: git pull failed.")
        return False

    # ------------------------------------------------------
    # Push
    # ------------------------------------------------------

    push = run("git push")

    if push.returncode != 0:
        print("ERROR: git push failed.")
        return False

    print("=" * 60)
    print("GitHub successfully updated.")
    print("=" * 60)

    return True


# ==========================================================
# Stand-alone execution
# ==========================================================

if __name__ == "__main__":
    publish()