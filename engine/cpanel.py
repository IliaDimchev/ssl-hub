import json
import subprocess


def installed_hosts():

    output = subprocess.check_output(
        [
            "uapi",
            "--output=json",
            "SSL",
            "installed_hosts"
        ],
        text=True
    )

    return json.loads(output)


def list_certs():

    output = subprocess.check_output(
        [
            "uapi",
            "--output=json",
            "SSL",
            "list_certs"
        ],
        text=True
    )

    return json.loads(output)
