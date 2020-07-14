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

        if name == None or name == "":
            return render_template("/create-room.html", error="All fields must be filled")
        elif room_name == None or room_name == "":
            return render_template("/create-room.html", error="Room needs a name")
        elif room_password == None or room_password == "":
            return render_template("/create-room.html", error="Password required")
        elif confirmed_password == None or confirmed_password == "":
            return render_template("/create-room.html", error="Please confirm password")
        elif room_password == confirmed_password:
            room_name_exists = models.Game.query.filter_by(room_name=models.Game().room_name).first()
            if room_name_exists != None:
                return render_template("/create-room.html", error="Room name already taken")
                
            return redirect('/waiting-room')

            # TODO: Add game/room to database
            # TODO: Add user to database (this will require using the game's id)
            #return redirect('/waiting-room')
        else:
            return render_template("/create-room.html", error="Passwords do not match")
    


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
            # TODO: create a new player in the database (you'll need the game's id)
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
        content = request.get_json(force=True)
        print(content)
        name = content["name"]
        ships = content["ships"]

        # TODO: Add player id when it becomes available
        board_object = models.Board()
        db.session.add(board_object)
        db.session.commit()

        for row in range(10):
            for col in range(10):
                cell_object = models.Cell(board_id=board_object.id, row=row, column=col)
                db.session.add(cell_object)
                db.session.commit()

        for ship in ships:
            ship_type = ship["type"]
            player_cells = ship["cells"]

            ship_object = models.Piece(piece_type=ship_type, cell_count=len(player_cells), board_id=board_object.id)
            db.session.add(ship_object)
            db.session.commit()

            for cell in player_cells:
                empty_cell = models.Cell.query.filter_by(board_id=board_object.id, row=cell["row"], column=cell["col"]).first()
                empty_cell.piece_id = ship_object.id
                db.session.commit()

        # The following lines are for debugging/understanding purposes
        boards = models.Board.query.all()
        ships = models.Piece.query.all()
        cells = models.Cell.query.all()
        print(boards)
        print(ships)
        print(cells)

        return redirect("/gameroom")



if __name__ == "__main__":
    app.run(debug=True)
