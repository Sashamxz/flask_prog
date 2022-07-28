import json
import re
from base64 import b64encode
from app import create_app, db
from app.models import User, Role, Post, Comment




def get_api_headers(username, password):
  return {
        'Authorization': 'Basic ' + b64encode(
            (username + ':' + password).encode('utf-8')).decode('utf-8'),
        'Accept': 'application/json',
        'Content-Type': 'application/json'
    }



def test_404(app):
    client = app.test_client()
    response = client.get(
        '/wrong/url',
        headers=get_api_headers('email', 'password'))
    assert(response.status_code, 404)
    
    if response.status_code != 404:
        json_response = json.loads(response.get_data(as_text=True))
    
        assert(json_response['error'], 'not found')



def test_token_auth(app):
    client = app.test_client()
    r = Role.query.filter_by(name='User').first()
    assert (r) == None
    u = User(email='john@example.com', password='1324', confirmed=True,
                role=r)
    db.session.add(u)
    db.session.commit()
     # перевірка не правильного токена
    response = client.get(
        '/api/posts/',
        headers=get_api_headers('bad-token', ''))
    assert(response.status_code, 401)

    # get a token
    response = client.post(
        '/api/tokens/',
        headers=get_api_headers('john@example.com', '1234'))
    assert(response.status_code, 200)
    json_response = json.loads(response.get_data(as_text=True))
    assert(json_response.get('token'))
    token = json_response['token']

    # issue a request with the token
    response = client.get(
        '/api/posts/',
        headers=get_api_headers(token, ''))
    assert(response.status_code, 200)
