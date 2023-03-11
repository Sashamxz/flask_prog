from app.models import Post, Subscribe, User, Comment, Permission, Like, ContactUs, Role


def test_login_page(client):
    response = client.get('/auth/login')
    assert response.status_code == 200
    assert b'Login' in response.data


def test_login(client, db):
    user = User(username='test', email='test@example.com')
    user.set_password('password')
    db.session.add(user)
    db.session.commit()

    response = client.post('/auth/login', data={
        'email': 'test@example.com',
        'password': 'password',
        'remember_me': False
    }, follow_redirects=True)
    assert response.status_code == 200


# def test_register_and_login(app):
#     # register a new account
#     client = app.test_client()
#     response = client.post('/auth/register', data={
#         'email': 'john@example.com',
#         'username': 'john',
#         'password': '1234',
#         'password2': '1234'
#     })

#     assert response.status_code == 302

#     # login with the new account
#     response = client.post('/auth/login', data={
#         'email': 'john@example.com',
#         'password': '1324'
#     }, follow_redirects=True)
#     assert response.status_code == 200


def test_home_page(app):
    client = app.test_client()
    response = client.get('/')
    assert response.status_code == 200


def test_export_posts(app, db):
    with app.app_context():
        contact = User(username="Johffn", email="zontick99@gmail.com",)
        contact.launch_task('export_posts', ('Exporting posts...'))

        db.session.commit()
        assert contact.tasks is not None
