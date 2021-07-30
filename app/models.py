from flask import current_app, request, url_for
from enum import unique
from . import db
from datetime import datetime
import re




class Permission:
    FOLLOW = 1
    COMMENT = 2
    WRITE = 4
    MODERATE = 8
    ADMIN = 16


def slugyfy(stringg):
    pattern = r'[^\w+]'
    return re.sub(pattern, '-', stringg)
 

class Post(db.Model):
    # __table_args__ = {'extend_existing': True} 
    id = db.Column(db.Integer, primary_key=True)    
    title = db.Column(db.String(140))   
    slug = db.Column(db.String(140), unique=True)
    body = db.Column(db.Text)
    created = db.Column(db.DateTime, default=datetime.now())


    

    def __init__(self,*args,**kwargs):
        super(Post, self).__init__(*args, **kwargs)
        self.generate_slug()

    
    def generate_slug(self):
        if self.title:
            self.slag = slugyfy(self.title)

    def __repr__(self) -> str:
        return '<Post id: {}, title: {}>'.format(self.id, self.title)

      



# class Message(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     text = db.Column(db.String(1024), nullable=False)
 
#     def __init__(self, text,tags):
#         self.text = text.stript()
#         self.tags = [
#            Tag(text=tag.strip()) for tag in tags.split(',')
#         ]
     

# class Tag(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     text = db.Column(db.String(32), nullable=False)
    
#     message_id = db.Column(db.Integer, db.ForeignKey('massage.id'), nullable=False)
#     message = db.relationship('Message', backref=db.backref('tags', lazy=True))    




