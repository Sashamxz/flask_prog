from flask_wtf import FlaskForm 
from wtforms import StringField, TextAreaField, BooleanField, SelectField, SubmitField
from wtforms.validators import DataRequired, Length, Email, Regexp




class PostForm(FlaskForm):
    title = StringField("Title")
    body = TextAreaField("Body")


class CommentForm(FlaskForm):
    body = StringField('Enter your comment', validators=[DataRequired()])
    submit = SubmitField('Submit')