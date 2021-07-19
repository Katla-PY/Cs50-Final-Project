
import sqlite3

from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

@app.route("/api")
def index():
    return render_template("api.html")


@app.route("/api/add_server")
def add_server():
    server_id = request.args["server-id"]
    server_name = request.args["server-name"]
    
    if not server_id: return None
    if not server_name: return None

    con = sqlite3.connect("./cs50-fp.db")
    cur = con.cursor()

    # checks if server already exists in database and if not it adds it
    if not cur.execute(f"SELECT server_id FROM servers WHERE server_id={server_id}").fetchone():
        cur.execute(f"INSERT INTO servers(server_id, server_name) VALUES({server_id}, '{server_name}')")
        con.commit()
        con.close()
        return (jsonify({"exists": False}), 200)
    return (jsonify({"exists": True}), 200)


@app.route("/api/remove_server")
def remove_server():
    server_id = request.args["server-id"]
    
    if not server_id: return ("", 500)
    
    con = sqlite3.connect("./cs50-fp.db")
    cur = con.cursor()
    
    cur.execute(f"DELETE FROM user_servers WHERE server_id={server_id}")
    cur.execute(f"DELETE FROM user_violations WHERE server_id={server_id}")
    cur.execute(f"DELETE FROM servers WHERE server_id={server_id}")
    
    con.commit()
    con.close()
    
    return ("", 200)


@app.route("/api/add_user")
def add_user():
    user_id = request.args["user-id"]
    user_name = request.args["user-name"]

    # checks that data is not None
    if not user_id: return ("", 500)
    if not user_name: return ("", 500)

    con = sqlite3.connect("./cs50-fp.db")
    cur = con.cursor()
    
    if not cur.execute(f"SELECT user_id FROM users WHERE user_id={user_id}").fetchone():
        cur.execute(f"INSERT INTO users(user_id, user_name) VALUES({user_id}, '{user_name}')")
        con.commit()
        con.close()

    return ("", 200)


@app.route("/api/add_user_server")
def add_user_server():
    user_id = request.args["user-id"]
    server_id = request.args["server-id"]
    
    if not user_id: return ("", 500)
    if not server_id: return ("", 500)
    
    con = sqlite3.connect("./cs50-fp.db")
    cur = con.cursor()

    cur.execute(f"INSERT INTO user_servers(user_id, server_id) VALUES({user_id}, {server_id})")
    con.commit()
    con.close()

    return ("", 200)


@app.route("/api/user_violation")
def user_violation():
    user_id = request.args["user-id"]
    server_id = request.args["server-id"]
    violation_id = request.args["violation-id"]
    reason = request.args["reason"]

    if not user_id: return ("", 500)
    if not server_id: return ("", 500)
    if not violation_id: return ("", 500)
    if not reason: return ("", 500)

    con = sqlite3.connect("./cs50-fp.db")
    cur = con.cursor()

    cur.execute(f"INSERT INTO user_violations(user_id, server_id, violation_id, reason) VALUES({user_id}, {server_id}, {violation_id}, '{reason}')")
    con.commit()
    con.close()

    return ("", 200)

app.run()
