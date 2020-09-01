from flask import jsonify
from flask import render_template
from flask import request
from flask import redirect
from application import app
from application.models import *

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