from server import db

class Cell(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    piece_id = db.Column(db.Integer, db.ForeignKey('piece.id'))
    board_id = db.Column(db.Integer, db.ForeignKey('board.id'))
    row = db.Column(db.Integer, nullable=False)
    column = db.Column(db.Integer, nullable=False)
    damaged = db.Column(db.Boolean, nullable=False, default=False)
    revealed = db.Column(db.Boolean, nullable=False, default=False)

    def __repr__(self):
        return "<Cell: id={}, piece_id={}, board_id={}, row={}, column={}, damaged={}, revealed={}>".format(self.id, self.piece_id, self.board_id, self.row, self.column, self.damaged, self.revealed)


class Piece(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    piece_type = db.Column(db.String(255), nullable=False)
    cell_count = db.Column(db.Integer, nullable=False)
    board_id = db.Column(db.Integer, db.ForeignKey('board.id'))

    def __repr__(self):
        return "<Piece: id={}, piece_type={}, cell_count={}, board_id={}>".format(self.id, self.piece_type, self.cell_count, self.board_id)


class Board(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    owner_id = db.Column(db.Integer, db.ForeignKey('player.id'))

    def __repr__(self):
        return "<Board: id={}, owner_id={}>".format(self.id, self.owner_id)


class Player(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    color = db.Column(db.String(255), nullable=False)
    game_id = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return "<Player: id={}, name={}, color={}, game_id={}>".format(self.id, self.name, self.color, self.game_id)


class Game(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    room_name = db.Column(db.String(255), nullable=False)
    room_password = db.Column(db.String(255), nullable=False)

    def __repr__(self):
        return "<Game: id={}, room_name={}, room_password={}>".format(self.id, self.room_name, self.room_password)


class Card(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    player = db.Column(db.Integer, db.ForeignKey('player.id'))
    cardtype = db.Column(db.Integer, db.ForeignKey('cardtype.id'))


class Cardtype(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.String(255), nullable=False)    