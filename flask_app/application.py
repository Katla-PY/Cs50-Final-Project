
import sqlite3

from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

@app.route("/api")
def index():
    return render_template("api.html")


@app.route("/api/server_setup")
def setup():
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


@app.route("/api/add_user")
def add_user():
    user_id = request.args["user-id"]
    user_name = request.args["user-name"]

    # checks that data is not None
    if not user_id: 
        print("no user-id")
        return ("", 500)
    if not user_name:
        print("no user-name")
        return ("", 500)

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
    
    con = sqlite3.connect("./flask_app/cs50-fp.db")
    cur = con.cursor()

    cur.execute(f"INSERT INTO user_servers(user_id, server_id) VALUES({user_id}, {server_id})")
    con.commit()
    con.close()

    return ("", 200)

@app.route("/api/kick_user")
def kick_user():
    pass

@app.route("/api/ban_user")
def ban_user():
    pass

app.run()
