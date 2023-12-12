from flask import Flask, render_template, request, session, redirect, url_for
from flask_socketio import join_room, leave_room, send, SocketIO
import random
from string import ascii_uppercase

# basic setup
app = Flask(__name__)
app.config["SECRET_KEY"] = "hehe"
socketio = SocketIO(app)

rooms = {}


# index page
@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        name = request.form.get("name")
        code = request.form.get("code")
        join_button = request.form.get("join_button", False)
        create_button = request.form.get("create_button", False)

        if not name:
            return redirect(url_for("failure", error="Name not provided."))
        if (not code) and (join_button == "1"):
            return redirect(url_for("failure", error="Code not provided."))

        room_code = code
        print("ffff")
        if create_button == "1":
            room_code = generate_room_code(4)
            rooms[room_code] = {"members": 0, "messages": []}
        if (join_button == "1") and (code not in rooms):
            return redirect(url_for("failure", error="Room does not exist."))

        session["room"] = room_code
        session["name"] = name
        return redirect("/room")
    return render_template("index.html")


@app.route("/failure", methods=["GET", "POST"])
def failure():
    fail_string = request.args.get("error")
    if request.method == "POST":
        back_button = request.form.get("back_button", False)
        name = request.args.get("name")
        code = request.args.get("code")
        if back_button == "1":
            return redirect("/")
    return render_template("failure.html", fail_string=fail_string)


@app.route("/room", methods=["POST", "GET"])
def room():
    room_code = session.get("room")
    # if room_code is None or session.get("name") is None or room_code not in rooms:
    #     return redirect(url_for("failure", error="Room Credentials missing."))
    return render_template("room.html")


def generate_room_code(n):
    code = ""
    while True:
        for _ in range(n):
            code += random.choice(ascii_uppercase)
        if code not in rooms:
            break
    return code


# run server
socketio.run(app, debug=True, allow_unsafe_werkzeug=True)
