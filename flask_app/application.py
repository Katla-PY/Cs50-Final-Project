
from flask import Flask, render_template, request

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/server")
def add_server():
    server_id = request.args.get("server_id")
    if not server_id: return None

app.run()
