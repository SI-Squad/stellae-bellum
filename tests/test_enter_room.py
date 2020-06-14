from .client import *

def test_mock_enter_room(client):
    rv = client.get('/enter-room')
    assert b'Return Home' in rv.data
    assert b'Enter Room' in rv.data
    assert b'Room Password' in rv.data
    assert b'Room Name' in rv.data
    assert b'Your Name' in rv.data