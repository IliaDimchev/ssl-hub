from flask import Flask
from flask import render_template
import sqlite3
import subprocess
from config import DB
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


@app.route("/discover")
def discover():

    subprocess.run([
        PYTHON,
        "/home/ilirbktk/ssl-hub/discover.py"
    ])

    subprocess.run([
        PYTHON,
        "/home/ilirbktk/ssl-hub/discover_cpanel.py"
    ])

    subprocess.run([
        PYTHON,
        "/home/ilirbktk/ssl-hub/discover_sites.py"
    ])

    return redirect("/")

if __name__ == "__main__":
    app.run()
