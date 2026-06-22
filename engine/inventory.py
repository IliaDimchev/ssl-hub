import subprocess

from config import PYTHON


SCRIPTS = [
    "/home/ilirbktk/ssl-hub/discover_sites.py",
    "/home/ilirbktk/ssl-hub/discover.py",
    "/home/ilirbktk/ssl-hub/discover_cpanel.py",
    "/home/ilirbktk/ssl-hub/engine/sync.py",
]


for script in SCRIPTS:

    print("Running:", script)

    result = subprocess.run(
        [PYTHON, script],
        capture_output=True,
        text=True
    )

    print(result.stdout)

    if result.stderr:
        print(result.stderr)

print("Inventory completed")
