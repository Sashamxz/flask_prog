from app import db
from app.models import  Post, Subscribe, User, Comment, Permission, Like , ContactUs, Role





def test_contactmodel_save(app):
    with app.app_context():
        Role.insert_roles()
        contact = User(username="John", email="john@gmail.com",)
        contact.set_password('1324')
        db.session.add(contact)
        db.session.commit()
        assert User.query.filter(User.email == 'john_doe@gmail.com')
        assert contact.password_hash != '1234'
        assert contact.can(Permission.MODERATE) == False


def test_register_and_login(app):
    # register a new account
    client = app.test_client()
    response = client.post('/auth/register', data={
        'email': 'john@example.com',
        'username': 'john',
        'password': '1234',
        'password2': '1234'
    })
    
    assert response.status_code == 302

    # login with the new account
    response = client.post('/auth/login', data={
        'email': 'john@example.com',
        'password': '1324'
    }, follow_redirects=True)
    assert response.status_code == 200


def test_home_page(app):
     client = app.test_client()
     response = client.get('/')
     assert response.status_code == 200


def test_db(app):
    with app.app_context():
        db.session.remove()
        db.drop_all()
       