import sqlite3
from pathlib import Path
from config import DB

HOME = Path("/home/ilirbktk")

conn = sqlite3.connect(DB)

for item in HOME.iterdir():

    if not item.is_dir():
        continue

    wp = item / "wp-config.php"

    if not wp.exists():
        continue

    domain = item.name
    webroot = str(item)

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
                wordpress=1,
                webroot=?
            WHERE domain=?
            """,
            (
                webroot,
                domain
            )
        )

    else:

        conn.execute(
            """
            INSERT INTO domains
            (
                domain,
                webroot,
                wordpress
            )
            VALUES
            (?, ?, 1)
            """,
            (
                domain,
                webroot
            )
        )

conn.commit()

print("Sites discovered")
