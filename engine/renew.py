import subprocess

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
