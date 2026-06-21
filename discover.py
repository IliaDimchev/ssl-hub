import sqlite3
import subprocess
from config import DB, ACME

conn = sqlite3.connect(DB)

output = subprocess.check_output(
    [ACME, "--list"],
    text=True
)

lines = output.strip().splitlines()

for line in lines[1:]:

    parts = line.split()

    if len(parts) < 7:
        continue

    domain = parts[0]
    keylength = parts[1]
    ca = parts[-3]
    renew = parts[-1]

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
                keylength=?,
                ca=?,
                renew_at=?,
                cert_exists=1
            WHERE domain=?
            """,
            (
                keylength,
                ca,
                renew,
                domain
            )
        )

    else:

        conn.execute(
            """
            INSERT INTO domains
            (
                domain,
                keylength,
                ca,
                renew_at,
                cert_exists
            )
            VALUES
            (?, ?, ?, ?, 1)
            """,
            (
                domain,
                keylength,
                ca,
                renew
            )
        )

conn.commit()

print("Discovery completed")
