from flask import jsonify
from sqlalchemy import text


def login(engine, username, password):
    conn = engine.connect()
    query = text("SELECT * FROM users WHERE username = :username AND password = :password")
    result = conn.execute(query, username=username, password=password)
    if result.rowcount == 0:
        return jsonify({"message": "Invalid username or password"}), 401
    else:
        return jsonify({"message": "Logged in successfully"}), 200