from flask import current_app, request, url_for
from enum import unique
from datetime import datetime
import re
from . import db
from flask_security import UserMixin, RoleMixin


post_tags = db.Table(
    'post_tags', db.Column(
        'post_id', db.Integer, db.ForeignKey('post.id')), db.Column(
            'tag_id', db.Integer, db.ForeignKey('tag.id')))


class Permission:
    FOLLOW = 1
    COMMENT = 2
    WRITE = 4
    MODERATE = 8
    ADMIN = 16


def slugify(stringg):
    pattern = r'[^\w+]'
    return re.sub(pattern, '-', stringg)


class Post(db.Model):
    # __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(140))
    slug = db.Column(db.String(140), unique=True)
    body = db.Column(db.Text)
    created = db.Column(db.DateTime, default=datetime.now)

    def __init__(self, *args, **kwargs):
        super(Post, self).__init__(*args, **kwargs)
        self.generate_slug()

    tags = db.relationship(
        'Tag',
        secondary=post_tags,
        backref=db.backref(
            'posts',
            lazy='dynamic'))

    def generate_slug(self):
        if self.title:
            self.slug = slugify(self.title)

    def __repr__(self):
        return '<Post id: {}, title: {}>'.format(self.id, self.title)


class Tag(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32), nullable=False)
    slug = db.Column(db.String(140), unique=True)

    def __init__(self, *args, **kwargs):
        super(Tag, self).__init__(*args, **kwargs)
        self.slug = slugify(self.name)

    def __repr__(self):
        return '{}'.format(self.name)


roles_users = db.Table(
    'roles_users',
    db.Column(
        'user_id',
        db.Integer(),
        db.ForeignKey('user.id')),
    db.Column(
        'role_id',
        db.Integer(),
        db.ForeignKey('role.id')))


class User(db.Model, UserMixin):
    # __tablename__ = 'user'
    id = db.Column(db.Integer(), primary_key=True)
    email = db.Column(db.String(64), unique=True)
    password = db.Column(db.String(64), unique=True)
    active = db.Column(db.Boolean(), default=False, index=True)
    roles = db.relationship(
        'Role',
        secondary=roles_users,
        backref=db.backref(
            'users',
            lazy='dynamic'))


class Role(db.Model, RoleMixin):
    # __tablename__ = 'roles'
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(64), unique=True)
    description = db.Column(db.String(255))


class Subscribe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(64), unique=True)
    time = db.Column(db.DateTime, default=datetime.now)


# class Message(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     text = db.Column(db.String(1024), nullable=False)

#     def __init__(self, text,tags):
#         self.text = text.stript()
#         self.tags = [
#            Tag(text=tag.strip()) for tag in tags.split(',')
#         ]


# class Role(db.Model, Role):
#     __tablename__ = 'roles'
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(64), unique=True)
#     default = db.Column(db.Boolean, default=False, index=True)
#     permissions = db.Column(db.Integer)
#     users = db.relationship('User', backref='role', lazy='dynamic')

#     def __init__(self, **kwargs):
#         super(Role, self).__init__(**kwargs)
#         if self.permissions is None:
#             self.permissions = 0

#     @staticmethod
#     def insert_roles():
#         roles = {
#             'User': [Permission.FOLLOW, Permission.COMMENT, Permission.WRITE],
#             'Moderator': [Permission.FOLLOW, Permission.COMMENT,
#                           Permission.WRITE, Permission.MODERATE],
#             'Administrator': [Permission.FOLLOW, Permission.COMMENT,
#                               Permission.WRITE, Permission.MODERATE,
#                               Permission.ADMIN],
#             }
#         default_role = 'User'
#         for r in roles:
#             role = Role.query.filter_by(name=r).first()
#             if role is None:
#                 role = Role(name=r)
#             role.reset_permissions()
#             for perm in roles[r]:
#                 role.add_permission(perm)
#             role.default = (role.name == default_role)
#             db.session.add(role)
#         db.session.commit()

#     def add_permission(self, perm):
#         if not self.has_permission(perm):
#             self.permissions += perm

#     def remove_permission(self, perm):
#         if self.has_permission(perm):
#             self.permissions -= perm

#     def reset_permissions(self):
#         self.permissions = 0

#     def has_permission(self, perm):
#         return self.permissions & perm == perm

#     def __repr__(self):
#         return '<Role %r>' % self.name

    # def __init__(self, **kwargs):
    #     super(Role, self).__init__(**kwargs)
    #     if self.permissions is None:
    #         self.permissions = 0

    # @staticmethod
    # def insert_roles():
    #     roles = {
    #         'User': [Permission.FOLLOW, Permission.COMMENT, Permission.WRITE],
    #         'Moderator': [Permission.FOLLOW, Permission.COMMENT,
    #                       Permission.WRITE, Permission.MODERATE],
    #         'Administrator': [Permission.FOLLOW, Permission.COMMENT,
    #                           Permission.WRITE, Permission.MODERATE,
    #                           Permission.ADMIN],
    #         }
    #     default_role = 'User'
    #     for r in roles:
    #         role = Role.query.filter_by(name=r).first()
    #         if role is None:
    #             role = Role(name=r)
    #         role.reset_permissions()
    #         for perm in roles[r]:
    #             role.add_permission(perm)
    #         role.default = (role.name == default_role)
    #         db.session.add(role)
    #     db.session.commit()

    # def add_permission(self, perm):
    #     if not self.has_permission(perm):
    #         self.permissions += perm

    # def remove_permission(self, perm):
    #     if self.has_permission(perm):
    #         self.permissions -= perm

    # def reset_permissions(self):
    #     self.permissions = 0

    # def has_permission(self, perm):
    #     return self.permissions & perm == perm

    # def __repr__(self):
    #     return '<Role %r>' % self.name
