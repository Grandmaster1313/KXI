import subprocess
from datetime import datetime

def run(cmd):
    print(f">>> {cmd}")
    subprocess.run(cmd, shell=True)

timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")

run("git add .")
run(f'git commit -m "Auto update {timestamp}"')
run("git pull --rebase")
run("git push")