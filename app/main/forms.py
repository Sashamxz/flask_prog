from flask_wtf import FlaskForm 
from wtforms import StringField, TextAreaField, BooleanField, SelectField, SubmitField


class PostForm(FlaskForm):
    title = StringField("Title")
    body = TextAreaField("Body")
    