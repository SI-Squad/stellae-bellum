from flask import render_template
from flask import jsonify
from flask import request
from application import app
from application.models import *

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

@app.route('/update-room-participants', methods=["POST"])
def update_room_participants():
    """
    This endpoint should be called from the waiting-room page on an interval
    Every response should be the latest list of participants in the room
    """
    if request.method == 'POST':
        room_name = request.values.get('room-name')

        game = db.session.query(Game).filter_by(room_name=room_name).first()
        if (game == None):
            return "Oopsies. Looks like something went wrong"
        else:     
            players = db.session.query(Player).filter_by(game_id=game.id).all()

            participants = [player.name for player in players]

            return jsonify(participants)