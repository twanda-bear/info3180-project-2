# Add any form classes for Flask-WTF here
"""Create a form class called MovieForm that
has three (3) fields and appropriate validation rules. A String field called
'title' for the Movie Title, TextArea field called 'description' that
requires a user to fill in a brief description or summary of the movie and a
FileField called 'poster' that only allows images of a movie poster to be
uploaded. """
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, FileField
from wtforms.validators import DataRequired, Length, Regexp

class MovieForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired(), Length(min=1, max=83)])
    description = TextAreaField('Description', validators=[DataRequired(), Length(min=1, max=500)])
    poster = FileField('Poster', validators=[DataRequired()])