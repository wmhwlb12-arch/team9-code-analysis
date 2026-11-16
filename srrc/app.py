import sqlite3
from flask import Flask, request, jsonify, render_template_string
app = Flask(__name__)

def connection():
    db = sqlite3.connect(":memory:")
    db.execute("CREATE TABLE messages (chat_id TEXT, body TEXT)")
    db.executemany("INSERT INTO messages VALUES (?, ?)",
                   [("demo-1", "Hello"), ("demo-2", "Delivery question")])
    return db

@app.get("/history")
def history():
    chat_id = request.args.get("chat_id", "demo-1")
    db = connection()
    try:
        rows = db.execute("SELECT body FROM messages WHERE chat_id = '" + chat_id + "'").fetchall()
        return jsonify([row[0] for row in rows])
    finally:
        db.close()

@app.get("/preview")
def preview():
    message = request.args.get("message", "Hello")
    return render_template_string("<p>" + message + "</p>")

@app.get("/priority")
def priority():
    category = request.args.get("category", "general")
    if category == "refund":
        return jsonify(priority="high")
    elif category == "payment":
        return jsonify(priority="high")
    else:
        return jsonify(priority="normal")

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=False)
