# Add any form classes for Flask-WTF here
from flask_wtf import FlaskForm, file
from wtforms import StringField, TextAreaField, EmailField, PasswordField
from flask_wtf.file import FileField, FileRequired, FileAllowed, FileSize
from wtforms.validators import InputRequired, DataRequired, Length


class PostForm(FlaskForm):
    caption = StringField('Caption', validators=[InputRequired(), Length(min=2, max=200)])
    photo = FileField('Photo', validators=[FileRequired(), FileSize(max=80000), FileAllowed(["png", "jpg"], message="Only Image Files Permitted")])


class RegisterForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired(), Length(min=5, max=80)])
    password = PasswordField('Password', validators=[InputRequired(), Length(min=6, max=60)])
    firstname = StringField('First Name', validators=[InputRequired(), Length(min=2, max=(128))])
    lastname = StringField('Last Name', validators=[InputRequired(), Length(min=2, max=(128))])
    email = EmailField('Email', validators=[InputRequired(), Length(min=2, max=80)])
    location = StringField('Lcation', validators=[InputRequired(), Length(min=2, max=128)])
    biography = TextAreaField('Biography', validators=[DataRequired(), Length(min=2, max=200)])
    profile_photo = FileField('Profile Photo', validators=[FileRequired(), FileSize(max_size=80000), FileAllowed(["png", "jpg"], message="Only Image File Permitted")])


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired(), Length(min=5, max=80)])
    password = PasswordField('Password', validators=[InputRequired(), Length(min=6, max=60)])


