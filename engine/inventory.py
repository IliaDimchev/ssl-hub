from config import PYTHON
from pathlib import Path
import subprocess

ROOT = Path(__file__).resolve().parent.parent

scripts = [
    ROOT / "discover_sites.py",
    ROOT / "discover.py",
    ROOT / "discover_cpanel.py",
]

for script in scripts:

    print(f"Running {script}")

    subprocess.run(
        [
            PYTHON,
            str(script)
        ],
        cwd=ROOT
    )

subprocess.run(
    [
        PYTHON,
        "-m",
        "engine.sync"
    ],
    cwd=ROOT
)

print("Inventory completed")