from flask import json
from base64 import b64encode
from app.models import User, Role, Post, Comment


def get_api_headers(email, password):
    return {
        'Authorization': 'Basic ' + b64encode(
            (email + ':' + password).encode('utf-8')).decode('utf-8'),
        'Accept': 'application/json',
        'Content-Type': 'application/json'
    }


def test_404(app):
    client = app.test_client()
    response = client.get(
        '/wrong/url',
        headers=get_api_headers('email', 'password'))
    assert response.status_code == 404

    if response.status_code != 404:
        json_response = json.loads(response.get_data(as_text=True))
        assert (json_response['error'] == 'not found')


def test_token_auth(client, db):
    db.create_all()
    u = User(email='john@example.com', username='Dron')
    u.set_password('1234')
    db.session.add(u)
    db.session.commit()

    # перевірка не правильного токена
    response = client.post(
        '/api/tokens/',
        headers=get_api_headers('bad-token', ''))
    assert response.status_code == 401

    # get a token
    response = client.post(
        '/api/tokens/',
        headers=get_api_headers('john@example.com', '1234'))
    assert response.status_code == 200
    json_response = json.loads(response.get_data(as_text=True))
    assert (json_response.get('token'))
    token = json_response['token']

    # need fix !
    response = client.get(
        '/api/posts/',
        headers=get_api_headers(token, ''))
    assert response.status_code == 200



       
