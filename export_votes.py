"""Export votes from the database in BLT format (standard for STV counters).

Usage:
    python export_votes.py                  # reads local votes.db
    python export_votes.py /data/votes.db   # reads a specific path

To get the DB from Fly.io:
    fly ssh sftp get /data/votes.db votes.db
"""

import json
import sqlite3
import sys

CANDIDATES = [
    (1953, "Long(ish) Running Semi-Autonomous Agents (formerly Project Vend)"),
    (1924, "Submit an entry for some kind of competition"),
    (1925, "Cribbage pegging"),
    (1964, "Build Your Own Language"),
    (1965, "RoombAI (second attempt)"),
    (1967, "GitWho: Finding social networks in Turing's GitHub"),
    (1970, "Find Alan"),
    (1971, '"Mission Impossible" eye-tracking projection screen'),
    (1974, "Guixify all the things!"),
    (1972, "Big-Screen-ify past and present hack week projects"),
    (1975, "Securely deploy and configure OpenClaw personal assistant AI agent"),
]

NUM_SEATS = 5

issue_to_blt = {issue: i + 1 for i, (issue, _) in enumerate(CANDIDATES)}

db_path = sys.argv[1] if len(sys.argv) > 1 else "votes.db"
db = sqlite3.connect(db_path)
rows = db.execute("SELECT ranking FROM votes ORDER BY id").fetchall()
db.close()

print(f"{len(CANDIDATES)} {NUM_SEATS}")
for (ranking_json,) in rows:
    prefs = [str(issue_to_blt[n]) for n in json.loads(ranking_json)]
    print("1 " + " ".join(prefs) + " 0")
print("0")
for issue, title in CANDIDATES:
    print(f'"#{issue} {title}"')
print('"Hack Week STV Vote"')
