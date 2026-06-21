from flask import Flask
from engine.domains import load_domains
from engine.certs import days_left

app = Flask(__name__)


@app.route("/")
def dashboard():

    domains = load_domains()

    rows = []

    for item in domains["domains"]:

        try:
            days = days_left(
                item["domain"]
            )

        except Exception:

            days = "?"

        rows.append({
            "domain": item["domain"],
            "days": days
        })

    html = "<h1>SSL Hub</h1>"

    html += "<table border='1'>"

    for row in rows:

        html += (
            f"<tr>"
            f"<td>{row['domain']}</td>"
            f"<td>{row['days']}</td>"
            f"</tr>"
        )

    html += "</table>"

    return html


if __name__ == "__main__":
    app.run()