import json

DOMAINS_FILE = "/home/ilirbktk/ssl-hub/data/domains.json"


def load_domains():
    with open(DOMAINS_FILE, "r") as f:
        return json.load(f)


def save_domains(data):
    with open(DOMAINS_FILE, "w") as f:
        json.dump(data, f, indent=4)