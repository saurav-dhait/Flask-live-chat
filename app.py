from flask import Flask, render_template, request, session, redirect, url_for
from flask_socketio import join_room, leave_room, send, SocketIO
import random
from string import ascii_uppercase

# basic setup
app = Flask(__name__)
app.config["SECRET_KEY"] = "hehe"
socketio = SocketIO(app)

# rooms dictionary stores information about a particular room code like member count and messages.
rooms = {}


# index/landing page route
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

        if create_button == "1":
            room_code = generate_room_code(4)
            rooms[room_code] = {"members": 0, "messages": []}
        if (join_button == "1") and (code not in rooms):
            return redirect(url_for("failure", error="Room does not exist."))

        session["room"] = room_code
        session["name"] = name
        return redirect("/room")
    return render_template("index.html")


# Failure route is for displaying errors during usage of the web app
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


# room route renders the room page
@app.route("/room", methods=["POST", "GET"])
def room():
    room_code = session.get("room")
    if room_code is None or session.get("name") is None or room_code not in rooms:
        return redirect(url_for("failure", error="Room Credentials missing."))
    return render_template("room.html", room=room_code, messages=rooms[room_code]["messages"])


def generate_room_code(n):
    """
    :param n: n is an integer
    :return: Random combination of n upper case characters
    """
    code = ""
    while True:
        for _ in range(n):
            code += random.choice(ascii_uppercase)
        if code not in rooms:
            break
    return code


#
@socketio.on("connect")
def connect(auth):
    """
    connect function establishes the connection to room as soon as room page is rendered.
    """
    room = session.get("room")
    name = session.get("name")
    if (not room) or (not name):
        return redirect(url_for("failure", error="Room Credentials missing."))
    if room not in rooms:
        leave_room(room)
        return
    join_room(room)
    send({"name": name, "message": "has entered the chat."}, to=room)
    rooms[room]["members"] += 1
    print(f"{name} joined room {room}.")


@socketio.on("disconnect")
def disconnect():
    """
    executes a number of operations as soon as client is disconnected

    """
    room = session.get("room")
    name = session.get("name")
    leave_room(room)
    if room in rooms:
        rooms[room]["members"] -= 1
        if rooms[room]["members"] <= 0:
            del rooms[room]
    send({"name": name, "message": "has left the chat."}, to=room)
    print(f"{name} has left room {room}.")


@socketio.on("message")
def message(data):
    """
    handles sending of messages to room
    """
    room = session.get("room")
    name = session.get("name")
    if room not in rooms:
        return
    content = {
        "name": name,
        "message": data["data"]
    }
    send(content, to=room)
    rooms[room]["messages"].append(content)
    print(f"{name} said : {data['data']}.")


# run server
socketio.run(app, debug=True, allow_unsafe_werkzeug=True)
