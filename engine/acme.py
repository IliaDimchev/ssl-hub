import subprocess

ACME = "/home/ilirbktk/.acme.sh/acme.sh"


def renew(domain):

    return subprocess.run(
        [
            ACME,
            "--renew",
            "-d",
            domain
        ],
        capture_output=True,
        text=True
    )
