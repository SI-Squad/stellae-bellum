from .client import *

def test_mock_create_room(client):
    rv = client.get('/create-room')
    assert b'Return Home' in rv.data
    assert b'Create Room' in rv.data
    assert b'Confirm Room Password' in rv.data
    assert b'Room Password' in rv.data
    assert b'Room Name' in rv.data
    assert b'Your Name' in rv.data