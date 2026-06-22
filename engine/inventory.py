import subprocess
from config import PYTHON

COMMANDS = [

    [PYTHON,
     "/home/ilirbktk/ssl-hub/discover_sites.py"],

    [PYTHON,
     "/home/ilirbktk/ssl-hub/discover.py"],

    [PYTHON,
     "/home/ilirbktk/ssl-hub/discover_cpanel.py"],

    [PYTHON,
     "-m",
     "engine.sync"]

]

for cmd in COMMANDS:

    print("Running:", " ".join(cmd))

    result = subprocess.run(
        cmd,
        cwd="/home/ilirbktk/ssl-hub",
        capture_output=True,
        text=True
    )

    print(result.stdout)

    if result.stderr:
        print(result.stderr)
