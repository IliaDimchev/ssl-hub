import json
import sqlite3
import subprocess

from config import DB

conn = sqlite3.connect(DB)

output = subprocess.check_output(
    [
        "uapi",
        "--output=json",
        "SSL",
        "installed_hosts"
    ],
    text=True
)

data = json.loads(output)

hosts = (
    data
    .get("result", {})
    .get("data", [])
)

for host in hosts:

    domain = host.get("servername")

    if not domain:
        continue

    cert = host.get("certificate", {})

    issuer = cert.get(
        "issuer.organizationName"
    )

    issuer_cn = cert.get(
        "issuer.commonName"
    )

    not_after = cert.get(
        "not_after"
    )

    cursor = conn.execute(
        """
        SELECT id
        FROM domains
        WHERE domain=?
        """,
        (domain,)
    )

    row = cursor.fetchone()

    if row:

        conn.execute(
            """
            UPDATE domains
            SET
                cert_exists=1,
                source='cpanel',
                ca=?,
                issuer=?,
                renew_at=?,
                last_seen=datetime('now')
            WHERE domain=?
            """,
            (
                issuer,
                issuer_cn,
                not_after,
                domain
            )
        )

    else:

        conn.execute(
            """
            INSERT INTO domains
            (
                domain,
                cert_exists,
                ca,
                renew_at
            )
            VALUES
            (?,1,?,?)
            """,
            (
                domain,
                issuer,
                not_after
            )
        )

conn.commit()

print("cPanel discovery completed")
