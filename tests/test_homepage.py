from .client import *

def test_mock_homepage(client):
    rv = client.get('/')
    assert b'Stellae Bellum' in rv.data