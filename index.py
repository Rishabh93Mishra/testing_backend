from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3
import os

app = Flask(__name__)
CORS(app)

DB_FILE = "careers.db"


# ---------- DATABASE ----------
def get_db_connection():
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS careers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            description TEXT NOT NULL,
            interest TEXT NOT NULL,
            cost INTEGER NOT NULL
        )
    """)

    cursor.execute("SELECT COUNT(*) FROM careers")
    if cursor.fetchone()[0] == 0:
        cursor.executemany("""
            INSERT INTO careers (name, description, interest, cost)
            VALUES (?, ?, ?, ?)
        """, [
            ("Web Developer", "Build websites and web apps", "technology", 50000),
            ("Data Analyst", "Analyze data and create reports", "technology", 60000),
            ("Graphic Designer", "Design logos and visuals", "design", 40000),
            ("Digital Marketer", "Online marketing and SEO", "marketing", 30000),
            ("Civil Engineer", "Infrastructure and construction", "engineering", 80000)
        ])

    conn.commit()
    conn.close()


# 🔥 IMPORTANT: run DB init when app loads
init_db()


# ---------- ROUTES ----------
@app.route("/")
def home():
    return "Backend running 🚀"


@app.route("/api/careers", methods=["GET"])
def get_careers():
    interest = request.args.get("interest", "").lower()
    budget = request.args.get("budget", type=int)

    if not interest or budget is None:
        return jsonify({"error": "Missing interest or budget"}), 400

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT name, description, cost
        FROM careers
        WHERE interest = ?
        AND cost <= ?
    """, (interest, budget))

    rows = cursor.fetchall()
    conn.close()

    return jsonify([
        {"name": r["name"], "description": r["description"], "cost": r["cost"]}
        for r in rows
    ])


# ---------- LOCAL RUN ----------
if __name__ == "__main__":
    app.run(debug=True)
