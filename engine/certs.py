import ssl
import socket
from datetime import datetime


def days_left(domain):

    context = ssl.create_default_context()

    with socket.create_connection((domain, 443)) as sock:

        with context.wrap_socket(
            sock,
            server_hostname=domain
        ) as ssock:

            cert = ssock.getpeercert()

    expires = datetime.strptime(
        cert["notAfter"],
        "%b %d %H:%M:%S %Y %Z"
    )

    return (expires - datetime.utcnow()).days