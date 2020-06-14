from .client import *

def test_mock_waiting_room(client):
    rv = client.get('/waiting-room')
    assert b'Waiting Room' in rv.data
    assert b'spinner-grow' in rv.data