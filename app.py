from flask import Flask, render_template, request, session, redirect, url_for
from flask_socketio import join_room, leave_room, send, SocketIO
import random
from string import ascii_uppercase

# basic setup
app = Flask(__name__)
app.config["SECRET_KEY"] = "hehe"
socketio = SocketIO(app)


# index page
@app.route("/", methods=["GET", "POST"])
def index():
    return render_template("index.html")


# run server
socketio.run(app, debug=True, allow_unsafe_werkzeug=True)
