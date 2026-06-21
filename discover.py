import subprocess
import sqlite3
import os
from config import DB
from config import ACME

ACME = os.path.expanduser("~/.acme.sh/acme.sh")

DB = "/home/ilirbktk/ssl-hub/database/sslhub.db"

IGNORED = [
    "bulshop.bg"
]

conn = sqlite3.connect(DB)

conn.execute("""
CREATE TABLE IF NOT EXISTS domains (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    domain TEXT UNIQUE,
    keylength TEXT,
    san_domains TEXT,
    ca TEXT,
    created_at TEXT,
    renew_at TEXT,
    managed INTEGER DEFAULT 1
)
""")

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
    created = parts[-2]
    renew = parts[-1]

    ignored = 1 if domain in IGNORED else 0

    conn.execute("""
    INSERT OR REPLACE INTO domains
    (
        domain,
        keylength,
        ca,
        created_at,
        renew_at
    )
    VALUES
    (?, ?, ?, ?, ?)
    """,
                 (
                     domain,
                     keylength,
                     ca,
                     created,
                     renew
                 ))

conn.commit()

print("Discovery completed")
