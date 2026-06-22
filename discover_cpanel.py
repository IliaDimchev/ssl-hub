import json
import sqlite3
import subprocess

from engine.config import DB

conn = sqlite3.connect(DB)
cur = conn.cursor()

result = subprocess.run(
    [
        "uapi",
        "--output=json",
        "SSL",
        "installed_hosts"
    ],
    capture_output=True,
    text=True
)

data = json.loads(result.stdout)

hosts = (
    data
    .get("result", {})
    .get("data", [])
)

for host in hosts:

    cert = host.get("certificate", {})

    domains = host.get("domains", [])

    issuer_org = cert.get(
        "issuer.organizationName"
    )

    issuer_cn = cert.get(
        "issuer.commonName"
    )

    renew_at = cert.get(
        "not_after"
    )

    for domain in domains:

        cur.execute(
            """
            SELECT id
            FROM domains
            WHERE domain=?
            """,
            (domain,)
        )

        row = cur.fetchone()

        if not row:
            continue

        domain_id = row[0]

        cur.execute(
            """
            DELETE FROM certificates
            WHERE domain_id=?
            AND source='cpanel'
            """,
            (domain_id,)
        )

        cur.execute(
            """
            INSERT INTO certificates
            (
                domain_id,
                source,
                ca,
                issuer,
                renew_at,
                cert_exists,
                last_seen
            )
            VALUES
            (
                ?,?,?,?,?,?,
                datetime('now')
            )
            """,
            (
                domain_id,
                "cpanel",
                issuer_org,
                issuer_cn,
                renew_at,
                1
            )
        )

conn.commit()
conn.close()

print("cPanel discovery completed")
