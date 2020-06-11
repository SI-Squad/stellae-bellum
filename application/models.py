from server import db

class Cell(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    piece_id = db.Column(db.Integer, db.ForeignKey('piece.id'))
    board_id = db.Column(db.Integer, db.ForeignKey('board.id'))
    row = db.Column(db.Integer, nullable=False)
    column = db.Column(db.Integer, nullable=False)
    damaged = db.Column(db.Boolean, nullable=False, default=False)
    revealed = db.Column(db.Boolean, nullable=False, default=False)


class Piece(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    peicetype = db.Column(db.String(255), nullable=False)
    cellCount = db.Column(db.Integer, nullable=False)
    cells = db.relationship('Cell', backref='piece')
    board_id = db.Column(db.Integer, db.ForeignKey('board.id'))


class Board(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    owner_id = db.Column(db.Integer, db.ForeignKey('player.id'))
    pieces = db.relationship('Piece', backref='board')
    cells = db.relationship('Cell', backref='board')


class Player(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    color = db.Column(db.String(255), nullable=False)
    board = db.relationship('Board', backref='player') 
    cards = db.relationship('Card', backref='player')


class Game(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    players = db.relationship('Player', backref='Game')
    name = db.Column(db.String(255), nullable=False)
    password = db.Column(db.String(255), nullable=False)


class Card(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    player = db.Column(db.Integer, db.ForeignKey('player.id'))
    cardtype = db.Column(db.Integer, db.ForeignKey('cardtype.id'))


class Cardtype(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.String(255), nullable=False)
    cards = db.relationship('Card', backref='cardtype')
    