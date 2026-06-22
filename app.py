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
        domain,
        wordpress,
        cert_exists,
        source,
        ca,
        renew_at,
        ignored
    FROM domains
    ORDER BY domain
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


@app.route("/sync")
def sync():

    subprocess.run(
        [
            PYTHON,
            "/home/ilirbktk/ssl-hub/engine/sync.py"
        ]
    )

    return redirect("/")

if __name__ == "__main__":
    app.run()
