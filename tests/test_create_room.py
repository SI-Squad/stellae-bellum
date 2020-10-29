from .client import *
from flask import Flask, url_for, request
import json
import time

def test_mock_create_room(client):
    rv = client.get('/create-room')
    assert b'Return Home' in rv.data
    assert b'Create Room' in rv.data
    assert b'Confirm Room Password' in rv.data
    assert b'Room Password' in rv.data
    assert b'Room Name' in rv.data
    assert b'Your Name' in rv.data

def test_create_room_form_success(client):
    mock_request_data = {
        'name': 'Test Name',
        'room-name': str(time.time()),
        'room-password': 'p@ssw0rd',
        'confirmed-room-password': 'p@ssw0rd'
    }
    rv = client.post('/create-room-form', data=mock_request_data, follow_redirects=True, content_type='multipart/form-data')
    assert rv.status_code == 200 #sucessful status code
    print(rv.data)
    assert request.path == url_for('open_room') #page redirected to new page

def test_create_room_form_name_failure(client):
    #no name entered
    mock_request_data = {
        'name': '',
        'room-name': str(time.time()),
        'room-password': 'p@ssw0rd',
        'confirmed-room-password': 'p@ssw0rd'
    }
    rv = client.post('/create-room-form', data=mock_request_data, follow_redirects=True)
    assert b'Please enter a name' in rv.data

def test_create_room_form_room_name_failure(client):
    #no room name ented
    mock_request_data = {
        'name': 'Test Name',
        'room-name': '',
        'room-password': 'p@ssw0rd',
        'confirmed-room-password': 'p@ssw0rd'
    }
    rv = client.post('/create-room-form', data=mock_request_data, follow_redirects=True)
    assert b'Room needs a name' in rv.data
    #room name taken
    #code here

def test_create_room_form_room_name_failure(client):
    #room name taken
    room_name = str(time.time())
    mock_request_data_init = {
        'name': 'Test Name Init',
        'room-name': room_name,
        'room-password': 'p@ssw0rdI',
        'confirmed-room-password': 'p@ssw0rdI'
    }
    rv = client.post('/create-room-form', data=mock_request_data_init, follow_redirects=True)
    mock_request_data = {
        'name': 'Test Name',
        'room-name': room_name,
        'room-password': 'p@ssw0rd',
        'confirmed-room-password': 'p@ssw0rd'
    }
    rv = client.post('/create-room-form', data=mock_request_data, follow_redirects=True)
    assert b'Room name already taken' in rv.data

def test_create_room_form_password_failure(client):
    #no password entered
    mock_request_data = {
        'name': 'Test Name',
        'room-name': str(time.time()),
        'room-password': '',
        'confirmed-room-password': 'p@ssw0rd'
    }
    rv = client.post('/create-room-form', data=mock_request_data, follow_redirects=True)
    print(rv.data)
    assert b'Password required' in rv.data
def test_create_room_form_password_failure_two(client):
    #no confirmed password entered
    mock_request_data = {
        'name': 'Test Name',
        'room-name': str(time.time()),
        'room-password': 'p@ssw0rd',
        'confirmed-room-password': ''
    }
    rv = client.post('/create-room-form', data=mock_request_data, follow_redirects=True)
    assert b'Please confirm password' in rv.data
def test_create_room_form_password_failure_three(client):
    #passwords do not match
    mock_request_data = {
        'name': 'Test Name',
        'room-name': str(time.time()),
        'room-password': 'p@ssw0rd',
        'confirmed-room-password': 'Pa$$wOrd'
    }
    rv = client.post('/create-room-form', data=mock_request_data, follow_redirects=True)
    assert b'Passwords do not match' in rv.data
