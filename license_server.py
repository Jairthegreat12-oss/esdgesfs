

/*
================================================================================
||                                                                            ||
||                      LICENSE SERVER (PYTHON - FLASK)                         ||
||                                                                            ||
================================================================================

This Python script runs a simple web server that acts as our license key
validator. You would run this on a server, and the C# game would communicate
with it over the internet.

--------------------------------------------------------------------------------
-- File: license_server.py
--------------------------------------------------------------------------------
*/

from flask import Flask, request, jsonify
import sqlite3
import uuid

app = Flask(__name__)
DB_FILE = "licenses.db"

# --- Database Setup ---
def init_db():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    # A simple table: key is the unique license, is_used is a flag
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS license_keys (
            key TEXT PRIMARY KEY,
            is_used INTEGER DEFAULT 0,
            customer_id TEXT
        )
    ''')
    conn.commit()
    conn.close()

# --- API Endpoints ---

# This is for YOU, the developer, to generate keys. Not for the public.
@app.route('/generate_key', methods=['POST'])
def generate_key():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    new_key = str(uuid.uuid4()) # Generate a random UUID as the key
    cursor.execute("INSERT INTO license_keys (key) VALUES (?)", (new_key,))
    conn.commit()
    conn.close()
    print(f"Generated new key: {new_key}")
    return jsonify({"status": "success", "key": new_key})

# This is the public endpoint your GAME will call.
@app.route('/validate_key', methods=['GET'])
def validate_key():
    key_to_check = request.args.get('key')
    if not key_to_check:
        return jsonify({"status": "error", "message": "No key provided"}), 400

    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM license_keys WHERE key=?", (key_to_check,))
    result = cursor.fetchone()
    conn.close()

    if result:
        return jsonify({"status": "valid"})
    else:
        return jsonify({"status": "invalid"}), 404

if __name__ == '__main__':
    init_db()
    # To generate your first key, you can run a separate script or use a tool
    # like Postman to send a POST request to /generate_key
    print("License server is running. Use /generate_key (POST) to create keys.")
    print("Use /validate_key?key=... (GET) to check them.")
    app.run(port=5000, debug=True)

/*
