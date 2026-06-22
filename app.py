from flask import Flask, redirect
from flask import render_template
import sqlite3
import subprocess
from config import DB, PYTHON
from engine.acme import renew


app = Flask(__name__)

@app.route("/")
def index():

    conn = sqlite3.connect(DB)


    rows = conn.execute("""
    SELECT
        d.id,
        d.domain,
        d.wordpress,
        d.managed,
        d.ignored,

        COUNT(c.id) AS cert_count,

        MAX(c.renew_at) AS renew_at,

        MAX(c.cert_exists) AS cert_exists

    FROM domains d

    LEFT JOIN certificates c
        ON c.domain_id = d.id

    GROUP BY d.id

    ORDER BY d.domain
    """).fetchall()

    return render_template(
        "index.html",
        domains=rows
    )


@app.route(
    "/renew/<domain>"
)
def renew_domain(domain):

    result = renew(domain)

    return result.stdout


@app.route("/inventory")
def inventory():


    subprocess.run([
        PYTHON,
        "-m",
        "engine.inventory"
    ],
    cwd="/home/ilirbktk/ssl-hub")

    return redirect("/")


@app.route("/ssl")
def ssl_inventory():
    conn = sqlite3.connect(DB)
    conn.row_factory = sqlite3.Row

    rows = conn.execute("""
        SELECT
            d.domain,
            c.source,
            c.ca,
            c.issuer,
            c.renew_at,
            c.last_seen
        FROM certificates c
        JOIN domains d ON d.id = c.domain_id
        ORDER BY d.domain
    """).fetchall()

    conn.close()

    return render_template(
        "ssl.html",
        certificates=rows
    )


@app.route("/sync")
def sync():


    subprocess.run(
        [
            PYTHON,
            "-m",
            "engine.sync"
        ],
        cwd="/home/ilirbktk/ssl-hub"
    )

    return redirect("/")

if __name__ == "__main__":
    app.run()
