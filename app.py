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
    if request.method == "POST":
        name = request.form.get("name")
        code = request.form.get("code")
        join_button = request.form.get("join_button", False)
        create_button = request.form.get("create_button", False)

    print(request.form)
    return render_template("index.html")


@app.route("/failure", methods=["GET", "POST"])
def failure():
    fail_string = "No fail string."
    if request.method == "POST":
        back_button = request.form.get("back_button", False)

        if back_button == "1":
            return redirect("/")
    return render_template("failure.html", fail_string=fail_string)


# run server
socketio.run(app, debug=True, allow_unsafe_werkzeug=True)
