from app.models import User


def test_new_user():
    """
    GIVEN a User model
    WHEN a new User is created
    THEN check the email, hashed_password, and role fields are defined correctly
    """
    user = User(email, username)
    assert user.email == 'test@gmail.com'
    assert user.hashed_password != password_hash
    assert user.role == 'user'