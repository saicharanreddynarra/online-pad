from flask import Flask, request, jsonify, render_template
import sqlite3
import os

app = Flask(__name__)

PASSWORD = os.environ.get("PAD_PASSWORD")

DB_NAME = "pad.db"

def init_db():
    if not os.path.exists(DB_NAME):
        db = sqlite3.connect(DB_NAME)
        db.execute("""
            CREATE TABLE pad (
                id INTEGER PRIMARY KEY,
                content TEXT
            )
        """)
        db.execute("INSERT INTO pad (id, content) VALUES (1, '')")
        db.commit()
        db.close()

def get_db():
    return sqlite3.connect(DB_NAME)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/load", methods=["POST"])
def load():
    if request.json.get("password") != PASSWORD:
        return jsonify({"error": "wrong password"}), 401

    db = get_db()
    cur = db.execute("SELECT content FROM pad WHERE id=1")
    content = cur.fetchone()[0]
    db.close()

    return jsonify({"content": content})

@app.route("/save", methods=["POST"])
def save():
    if request.json.get("password") != PASSWORD:
        return jsonify({"error": "wrong password"}), 401

    content = request.json.get("content", "")
    db = get_db()
    db.execute("UPDATE pad SET content=? WHERE id=1", (content,))
    db.commit()
    db.close()

    return jsonify({"status": "saved"})

if __name__ == "__main__":
    init_db()
    app.run(host="0.0.0.0", port=5000)
