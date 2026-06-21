from flask import Flask
from flask import render_template
import sqlite3
from config import DB


app = Flask(__name__)

@app.route("/")
def index():

    conn = sqlite3.connect(DB)

    rows = conn.execute("""
        SELECT *
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

if __name__ == "__main__":
    app.run()
