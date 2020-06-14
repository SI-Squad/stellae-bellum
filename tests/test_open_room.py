from .client import *

def test_mock_open_room(client):
    rv = client.get('/open-room')
    assert b'Delete Room' in rv.data
    assert b'Share Room' in rv.data
    assert b'Players in Room' in rv.data
    assert b'Room Password' in rv.data
    assert b'Room Name' in rv.data
    assert b'Your Name' in rv.data
    assert b'Open Room' in rv.data