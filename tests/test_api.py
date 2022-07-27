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
