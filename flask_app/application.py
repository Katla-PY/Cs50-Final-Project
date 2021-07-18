
import sqlite3

from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/server_setup")
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
        return (jsonify({"exists": False}), 200)
    return (jsonify({"exists": True}), 200)

@app.route("/server_setup_users")
def setup_users():
    user_id = request.args["user-id"]
    server_id = request.args["server-id"]
    
    if not user_id: return None
    if not server_id: return None

    con = sqlite3.connect("./cs50-fp.db")
    cur = con.cursor()

    cur.execute(f"INSERT INTO users(user_id, server_id) VALUES({user_id}, {server_id})")
    con.commit()

    return ("", 200)

app.run()
