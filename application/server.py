import os

from flask import Flask
from flask import jsonify
from flask import render_template
from flask import request
from flask import redirect
import random

from flask_sqlalchemy import SQLAlchemy

project_dir = os.path.dirname(os.path.abspath(__file__))
database_file = "sqlite:///{}".format(os.path.join(project_dir, "gamedatabase.db"))

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = database_file
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

import models

@app.route('/', methods=["GET", "POST"])
def home():
    return render_template("home.html")

@app.route('/gameover', methods=["GET", "POST"])
def gameover():
    return render_template("gameover.html")

@app.route('/gameroom', methods=["GET", "POST"])
def gameroom():
    return render_template("gameroom.html")

@app.route('/build', methods=["GET", "POST"])
def build():
    return render_template("build.html")

@app.route('/create-room', methods=["GET", "POST"])
def create_room():
    return render_template("create-room.html")

@app.route('/enter-room', methods=["GET", "POST"])
def enter_room():
    return render_template("enter-room.html")

@app.route('/waiting-room', methods=["GET", "POST"])
def waiting_room():
    return render_template("waiting-room.html")

@app.route('/open-room', methods=["GET", "POST"])
def open_room():
    return render_template("open-room.html")


@app.route('/create-room-form', methods=["POST"])
def handle_create_room_form():
    """
    This endpoint should be accessed from the create-room page.
    The page should send the data using a form.
    """
    if request.method == 'POST':
        name = request.form.get('name')
        room_name = request.form.get('room-name')
        room_password = request.form.get('room-password')
        confirmed_password = request.form.get('confirmed-room-password')

        if room_password == confirmed_password:
            # TODO: Add user to database
            # TODO: Add room to database
            return redirect('/waiting-room')
        else:
            return redirect('/create-room')
    else:
        return redirect('/create-room')


@app.route('/join-room-form', methods=["POST"])
def handle_join_room_form():
    """
    This endpoint should be accessed from the join-room page.
    The page should send the data using a form.
    """
    if request.method == 'POST':
        name = request.form.get('name')
        room_name = request.form.get('room-name')
        room_password = request.form.get('room-password')

        # TODO: Look for room in database

        if room_password == "correct": # TODO: Verify password is correct
            return redirect('/waiting-room')
        else:
            return redirect('/enter-room')
    else:
        return redirect('/enter-room')


@app.route('/update-room-participants', methods=["POST"])
def update_room_participants():
    """
    This endpoint should be called from the waiting-room page on an interval
    Every response should be the latest list of participants in the room
    """
    mock_participants = ["Alec", "Alex", "Marissa", "Mayo", "Yan"]
    if request.method == 'POST':
        room_name = request.form.get('room-name')

        # TODO: Get the participants in the room from the database

        participants = []
        for participant in mock_participants:
            roll = random.randint(0,1)
            if roll == 1 and participant not in participants:
                participants.append(participant)

        return jsonify(participants)
        

@app.route('/create-board-endpoint', methods=["POST"])
def create_board_endpoint():
    """
    This endpoint should be called from the create-board page.
    """
    if request.method == 'POST':
        print(request.json)
        content = request.json
        name = content["name"]
        coordinates = content["coordinates"]

        # TODO: Create all the cells
        # TODO: Create all the pieces
        # TODO: Create the board

        return redirect("/gameroom")



if __name__ == "__main__":
    app.run(debug=True)
