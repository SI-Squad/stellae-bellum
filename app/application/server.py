from flask import Flask
from flask import jsonify
from flask import render_template
from flask import request
from flask import redirect
from application import app
import random

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy(app)

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
            room_name_exists = db.session.query(Game).filter_by(room_name=room_name).first()
            if room_name_exists != None:
                return render_template("/create-room.html", error="Room name already taken")
              

       
            game_object = Game(room_name=room_name, room_password=room_password)
            db.session.add(game_object)
            db.session.commit()

            # color = randrange(1,255) DOES NOT RANDOMIZE COLOR PER PLAYER
            newp = Player(name=name, color="#CCFF00", game_id=game_object.id)
            db.session.add(newp)
            db.session.commit()

            players = db.session.query(Player).all() # these four lines are for testing purposes
            print(players)
            games = db.session.query(Game).all()
            print(games)
            return redirect('/open-room')
        else:
            return render_template("/create-room.html", error="Passwords do not match")
    else:
        return redirect('/create-room')


@app.route('/join-room-form', methods=["POST"])
def handle_join_room_form():
    """
    This endpoint should be accessed from the join-room page.
    The page should send the data using a form.
    """
    print("What")
    if request.method == 'POST':
        name = request.form.get('name')
        room_name = request.form.get('room-name')
        room_password = request.form.get('room-password')

        if name == None or name == "":
            return render_template("/enter-room.html", error="All fields must be filled")
        elif room_name == None or room_name == "":
            return render_template("/enter-room.html", error="Room requires a name")
        elif room_password == None or room_password == "":
            return render_template("/enter-room.html", error="Password required")
        
        game = db.session.query(Game).filter_by(room_name=room_name).first()
        if game == None or game == "":
            return render_template("/enter-room.html", error="Game with that name does not exist")
        if room_password != game.room_password:
            return render_template("/enter-room.html", error="Incorrect password")
        elif room_password == game.room_password:
            newp = Player(name=name, color="#CCFF00", game_id=game.id)
            db.session.add(newp)
            db.session.commit()

            players = db.session.query(Player).all() # these four lines are for testing purposes
            print(players)
            games = db.session.query(Game).all()
            print(games)
            return redirect('/waiting-room')
    else:
        return redirect('/enter-room')


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

        player = db.session.query(Player).filter_by(name=name).first()
        if player == None:
            return "Oopsies. Something went wrong :("

        board_object = Board(owner_id=player.id)
        db.session.add(board_object)
        db.session.commit()

        for row in range(10):
            for col in range(10):
                cell_object = Cell(board_id=board_object.id, row=row, column=col)
                db.session.add(cell_object)
                db.session.commit()

        for ship in ships:
            ship_type = ship["type"]
            player_cells = ship["cells"]

            ship_object = Piece(piece_type=ship_type, cell_count=len(player_cells), board_id=board_object.id)
            db.session.add(ship_object)
            db.session.commit()

            for cell in player_cells:
                empty_cell = db.session.query(Cell).filter_by(board_id=board_object.id, row=cell["row"], column=cell["col"]).first()
                empty_cell.piece_id = ship_object.id
                db.session.commit()

        # The following lines are for debugging/understanding purposes
        boards = db.session.query(Board).all()
        ships = db.session.query(Piece).all()
        cells = db.session.query(Cell).all()
        print(boards)
        print(ships)
        print(cells)

        resp = jsonify(success=True)
        return resp # The client will handle redirecting to the right page


@app.route('/get-board', methods=["POST"])
def get_board():
    if request.method == 'POST':
        content = request.get_json(force=True)
        username = content["name"]
        respose = get_board_helper(username)
        return respose

def get_board_helper(username):
    player = db.session.query(Player).filter_by(name=username).first()
    board = db.session.query(Board).filter_by(owner_id=player.id).first()

    if board == None:
        return {}
    else:
        response = {
            "board" : []
        }
        for i in range(10):
            row = []
            for j in range(10):
                cell = db.session.query(Cell).filter_by(board_id=board.id, row=i, column=j).first()
                if cell.damaged and cell.revealed:
                    row.append("X")
                elif cell.damaged:
                    row.append("#")
                elif cell.revealed:
                    row.append("O")
                else:
                    row.append(".")
            response["board"].append(row)
        return response


@app.route('/get-competitors-boards', methods=["POST"])
def get_competitors_board():
    if request.method == 'POST':
        content = request.get_json(force=True)
        room_name = content['room-name']
        username = content['username']    

        game = db.session.query(Game).filter_by(room_name=room_name).first()   
        players = db.session.query(Player).filter_by(game_id=game.id).all()
        participants = [player.name for player in players]

        boards = dict()
        participants.remove(username)
        for participant in participants:
            boards[participant] = get_board_helper(participant)
        print(boards)
        return jsonify(boards)

if __name__ == "__main__":
    app.run(debug=True)
