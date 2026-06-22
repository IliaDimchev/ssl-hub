from config import DB
import sqlite3

conn = sqlite3.connect(DB)
cur = conn.cursor()

cur.execute("""
DELETE FROM certificates
WHERE last_seen < datetime('now','-30 days')
""")

cur.execute("""
UPDATE domains
SET cert_exists=0
""")

cur.execute("""
UPDATE domains
SET cert_exists=1
WHERE EXISTS (
    SELECT 1
    FROM certificates c
    WHERE c.domain_id = domains.id
    AND c.cert_exists = 1
)
""")

conn.commit()
conn.close()

print("Sync completed")