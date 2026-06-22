import os
import subprocess

ACME_HOME = os.path.expanduser("~/.acme.sh")


def install(domain):

    cert = f"{ACME_HOME}/{domain}_ecc/fullchain.cer"
    key = f"{ACME_HOME}/{domain}_ecc/{domain}.key"

    result = subprocess.run(
        [
            "uapi",
            "SSL",
            "install_ssl",
            f"domain={domain}",
            f"cert={open(cert).read()}",
            f"key={open(key).read()}",
        ],
        capture_output=True,
        text=True
    )

    return result
