import sqlite3
import subprocess

from config import DB, ACME

conn = sqlite3.connect(DB)
cur = conn.cursor()

result = subprocess.run(
    [ACME, "--list"],
    capture_output=True,
    text=True
)

for line in result.stdout.splitlines():

    line = line.strip()

    if (
        not line
        or line.startswith("Main_Domain")
        or line.startswith("-----")
    ):
        continue

    parts = line.split()

    if len(parts) < 6:
        continue

    domain = parts[0]
    ssl_type = parts[1]
    issuer = parts[3]
    renew_at = parts[5]

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
        AND source='acme'
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
            "acme",
            issuer,
            ssl_type,
            renew_at,
            1
        )
    )

conn.commit()
conn.close()

print("Discovery completed")
