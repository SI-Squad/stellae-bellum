from flask import request
from flask import jsonify
from application import app
from application.models import *

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