# import pytest
# from app.models import User, Role, Permission, Post, Tag, slugify


# def test_user_password_hashing():
#     u = User(username='john')
#     u.set_password('cat')
#     assert u.check_password('cat')
#     assert not u.check_password('dog')


# def test_user_permissions():
#     u = User(email='john@example.com')
#     r = Role(name='Moderator')
#     r.add_permission(Permission.COMMENT)
#     r.add_permission(Permission.WRITE)
#     assert not u.can(Permission.WRITE)
#     assert not u.can(Permission.COMMENT)
#     u.role = r
#     assert u.can(Permission.COMMENT)
#     assert u.can(Permission.WRITE)


# def test_user_likes():
#     u1 = User(username='john', email='john@example.com')
#     u2 = User(username='susan', email='susan@example.com')
#     p = Post(title='test post', body='test post body', user=u1)
#     assert not u1.has_liked_post(p)
#     assert not u2.has_liked_post(p)
#     u1.like_post(p)
#     assert u1.has_liked_post(p)
#     assert not u2.has_liked_post(p)
#     u1.unlike_post(p)
#     assert not u1.has_liked_post(p)


# def test_slugify():
#     assert slugify('Hello, world!') == 'Hello-world'
#     assert slugify('The quick brown fox') == 'The-quick-brown-fox'
#     assert slugify('The_quick_brown_fox') == 'The_quick_brown_fox'


# @pytest.mark.parametrize('roles', [
#     ('User', Permission.FOLLOW | Permission.COMMENT, True),
#     ('Moderator', Permission.FOLLOW | Permission.COMMENT | Permission.WRITE |
#        Permission.MODERATE, False),
#     ('Administrator', Permission.FOLLOW | Permission.COMMENT | Permission.WRITE |
#       Permission.MODERATE | Permission.ADMIN, False),
# ])
# def test_roles(roles):
#     r = Role(name=roles[0], permissions=roles[1])
#     assert r.name == roles[0]
#     assert r.permissions == roles[1]
#     assert r.default == roles[2]


# def test_tag_repr():
#     t = Tag(name='test')
#     assert str(t) == '<Tag test>'


# def test_post_tags(db):
#     u = User(username='john', email='john@example.com')
#     db.session.add(u)
#     db.session.commit()
#     p1 = Post(title='test post', body='test post body', user=u)
#     p2 = Post(title='another test post', body='another test post body', user=u)
#     db.session.add_all([p1, p2])
#     db.session.commit()
#     t1 = Tag(name='test')
#     t2 = Tag(name='another')
#     db.session.add_all([t1, t2])
#     db.session.commit()
#     p1.tags.append(t1)
#     p1.tags.append(t2)
#     p2.tags.append(t1)
#     db.session.commit()
#     assert p1.tags.count() == 2
#     assert p2.tags.count() == 1
#     assert t1.posts.count() == 2
#     assert t2.posts.count() == 1
