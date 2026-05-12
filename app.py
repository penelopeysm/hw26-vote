import sqlite3
import json
import os
from flask import Flask, render_template, request, jsonify, g

app = Flask(__name__)

DATABASE = os.environ.get("DATABASE_PATH", "votes.db")
VOTE_PASSWORD = os.environ.get("VOTE_PASSWORD", "changeme")

CANDIDATES = [
    {"number": 1953, "title": "Long(ish) Running Semi-Autonomous Agents (formerly Project Vend)"},
    {"number": 1924, "title": "Submit an entry for some kind of competition"},
    {"number": 1925, "title": "Cribbage pegging"},
    {"number": 1964, "title": "Build Your Own Language"},
    {"number": 1965, "title": "RoombAI (second attempt)"},
    {"number": 1967, "title": "GitWho: Finding social networks in Turing's GitHub"},
    {"number": 1970, "title": "Find Alan"},
    {"number": 1971, "title": '"Mission Impossible" eye-tracking projection screen'},
    {"number": 1974, "title": "Guixify all the things!"},
    {"number": 1972, "title": "Big-Screen-ify past and present hack week projects"},
    {"number": 1975, "title": "Securely deploy and configure OpenClaw personal assistant AI agent"},
]


def get_db():
    if "db" not in g:
        g.db = sqlite3.connect(DATABASE)
        g.db.row_factory = sqlite3.Row
    return g.db


@app.teardown_appcontext
def close_db(exception):
    db = g.pop("db", None)
    if db is not None:
        db.close()


def init_db():
    db = sqlite3.connect(DATABASE)
    db.execute(
        """
        CREATE TABLE IF NOT EXISTS votes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            ranking TEXT NOT NULL,
            submitted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """
    )
    db.commit()
    db.close()


with app.app_context():
    init_db()


@app.route("/")
def index():
    return render_template("index.html", candidates=CANDIDATES)


@app.route("/vote", methods=["POST"])
def vote():
    data = request.get_json()
    password = data.get("password", "")
    ranking = data.get("ranking", [])

    if password != VOTE_PASSWORD:
        return jsonify({"error": "Incorrect password."}), 403

    if not ranking:
        return jsonify({"error": "Please rank at least one candidate."}), 400

    valid_numbers = {c["number"] for c in CANDIDATES}
    if not all(n in valid_numbers for n in ranking):
        return jsonify({"error": "Invalid candidate in ranking."}), 400

    if len(ranking) != len(set(ranking)):
        return jsonify({"error": "Duplicate candidates in ranking."}), 400

    db = get_db()
    db.execute(
        "INSERT INTO votes (ranking) VALUES (?)",
        (json.dumps(ranking),),
    )
    db.commit()

    return jsonify({"ok": True})


if __name__ == "__main__":
    app.run(debug=True, port=5468)
