
import sqlite3
from flask import Flask, render_template, request, jsonify
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

PATH_TO_DB = "./cs50-fp.db"

app = Flask(__name__)

limiter = Limiter(app, key_func=get_remote_address)

@app.route("/api")
def index():
    return render_template("api.html")


@app.route("/api/add_server", methods=["POST"])
@limiter.limit("5/second")
def add_server():
    server_id = request.form["server-id"]
    server_name = request.form["server-name"]
    
    if not server_id: return None
    if not server_name: return None

    con = sqlite3.connect(PATH_TO_DB)
    cur = con.cursor()

    # checks if server already exists in database and if not it adds it
    if not cur.execute(f"SELECT server_id FROM servers WHERE server_id={server_id}").fetchone():
        cur.execute(f"INSERT INTO servers(server_id, server_name) VALUES({server_id}, '{server_name}')")
        con.commit()
        con.close()
        return jsonify({"exists": False}), 200
    return jsonify({"exists": True}), 200


@app.route("/api/remove_server", methods=["POST"])
@limiter.limit("5/second")
def remove_server():
    server_id = request.form["server-id"]
    
    if not server_id: return "", 500
    
    con = sqlite3.connect(PATH_TO_DB)
    cur = con.cursor()
    
    cur.execute(f"DELETE FROM user_servers WHERE server_id={server_id}")
    cur.execute(f"DELETE FROM user_violations WHERE server_id={server_id}")
    cur.execute(f"DELETE FROM servers WHERE server_id={server_id}")
    
    con.commit()
    con.close()
    
    return "", 200


@app.route("/api/add_server_users", methods=["POST"])
@limiter.limit("5/second")
def add_server_users():
    users = request.json["users"]

    # checks that data is not None
    if not users: return "", 500

    con = sqlite3.connect(PATH_TO_DB)
    cur = con.cursor()
    
    for user in users:
        if not cur.execute(f"SELECT user_id FROM users WHERE user_id={user[0]}").fetchone():
            cur.execute(f"INSERT INTO users(user_id, user_name) VALUES({user[0]}, '{user[1]}')")
    
    con.commit()
    con.close()

    return "", 200


@app.route("/api/add_user_server", methods=["POST"])
@limiter.limit("5/second")
def add_user_server():
    data = request.json

    if not data: return "", 500

    server_id = data["server-id"]
    users = data["users"]

    con = sqlite3.connect(PATH_TO_DB)
    cur = con.cursor()

    for user in users:
        cur.execute(f"INSERT INTO user_servers(user_id, server_id) VALUES({user[0]}, {server_id})")

    con.commit()
    con.close()

    return "", 200


@app.route("/api/user_violation", methods=["POST"])
@limiter.limit("5/second")
def user_violation():
    user_id = request.form["user-id"]
    server_id = request.form["server-id"]
    violation_id = request.form["violation-id"]
    reason = request.form["reason"]

    if not user_id: return "", 500
    if not server_id: return "", 500
    if not violation_id: return "", 500
    if not reason: return "", 500

    con = sqlite3.connect(PATH_TO_DB)
    cur = con.cursor()

    cur.execute(
        f"INSERT INTO user_violations(user_id, server_id, violation_id, reason) VALUES({user_id}, {server_id}, {violation_id}, '{reason}')"
    )

    warn_count = cur.execute(
        f"SELECT COUNT(violation_id) FROM user_violations WHERE user_id={user_id} AND server_id={server_id} AND violation_id=1"
    ).fetchone()

    con.commit()
    con.close()

    return jsonify({"warns": warn_count[0]}), 200


def db_setup(ptdb: str, schema: str):
    con = sqlite3.connect(ptdb)
    cur = con.cursor()
    cur.executescript(schema)
    con.commit()
    con.close()


if __name__=="__main__":
    
    try:
        open(PATH_TO_DB, "r").close()
    except FileNotFoundError:
        open(PATH_TO_DB, "w").close()
        
        with open("./schema.sql", "r") as f:
            schema = f.read()
        
        db_setup(PATH_TO_DB, schema)
    
    app.run()
