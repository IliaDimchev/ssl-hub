import sqlite3

from config import DB

conn = sqlite3.connect(DB)

rows = conn.execute("""
SELECT
    domain,
    ca,
    cert_exists
FROM domains
""").fetchall()

for domain, ca, cert_exists in rows:

    ignored = 0
    managed = 1
    provider = "unknown"

    if not cert_exists:
        provider = "none"

    elif ca:

        ca_lower = ca.lower()

        if "let's encrypt" in ca_lower:
            provider = "letsencrypt"

        elif "zerossl" in ca_lower:
            provider = "zerossl"

        elif "sectigo" in ca_lower:
            provider = "external"
            ignored = 1
            managed = 0

    conn.execute("""
        UPDATE domains
        SET
            provider=?,
            ignored=?,
            managed=?
        WHERE domain=?
    """,
                 (
                     provider,
                     ignored,
                     managed,
                     domain
                 ))

conn.commit()

print("Sync completed")
