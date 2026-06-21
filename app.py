from flask import Flask
from flask import render_template
import sqlite3

app = Flask(__name__)

DB = "/home/ilirbktk/ssl-hub/sslhub.db"


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


if __name__ == "__main__":
    app.run()
