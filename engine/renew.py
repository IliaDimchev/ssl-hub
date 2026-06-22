from config import ACME
import subprocess

import os
import sys

ROOT = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)

sys.path.insert(0, ROOT)


from config import ACME


def renew(domain):

    result = subprocess.run(
        [
            ACME,
            "--renew",
            "-d",
            domain
        ],
        capture_output=True,
        text=True
    )

    return result
