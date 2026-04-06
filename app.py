from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3, database

app = Flask(__name__)
CORS(app)
database.init_db()

@app.route("/register", methods=["POST"])
def register():
    data = request.json
    try:
        conn = sqlite3.connect("students.db")
        conn.execute("""
            INSERT INTO students (name, email, phone, roll_number, department, year, event)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (data["name"], data["email"], data["phone"],
              data.get("roll_number"), data.get("department"),
              data.get("year"), data["event"]))
        conn.commit()
        conn.close()
        return jsonify({"success": True, "message": "Registered successfully!"})
    except sqlite3.IntegrityError:
        return jsonify({"success": False, "message": "Email already registered!"}), 400

@app.route("/students", methods=["GET"])
def get_students():
    conn = sqlite3.connect("students.db")
    conn.row_factory = sqlite3.Row
    rows = conn.execute("SELECT * FROM students ORDER BY registered_at DESC").fetchall()
    conn.close()
    return jsonify([dict(r) for r in rows])

if __name__ == "__main__":
    app.run(debug=True, port=5000)