# Add any model classes for Flask-SQLAlchemy here
from . import db
from werkzeug.security import generate_password_hash
from datetime import datetime


class Posts(db.Model):
    __tablename__ = 'posts'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    caption = db.Column(db.String(200))
    photo = db.Column(db.String(200))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    # user = db.relationship('Users', backref=db.backref('posts', lazy=True))
    created_on = db.Column(db.DateTime, default=datetime.now)

    def __init__(self, caption, photo, user_id):
        self.caption = caption
        self.photo = photo
        self.user_id = user_id

    def photo_path(self):
        if self.photo:
            return f'uploads/{self.photo}'
        else:
            return None


class Likes(db.Model):
    __tablename__ = 'likes'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'))
    # post = db.relationship('Posts', backref=db.backref('likes', lazy=True))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    # user = db.relationship('Users', backref=db.backref('likes', lazy=True))

    def __init__(self, post_id, user_id):
        self.post_id = post_id
        self.user_id = user_id




class Follows(db.Model):
    __tablename__ = "follows"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    follower_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    # follower = db.relationship('Users', backref=db.backref('follows', lazy=True))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    # user = db.relationship('Users', backref=db.backref('likes', lazy=True))

    def __init__(self, follower_id, user_id):
        self.follower_id = follower_id
        self.user_id = user_id


class Users(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(100))
    password = db.Column(db.String(128), unique=True)
    firstname = db.Column(db.String(80))
    lastname = db.Column(db.String(80))
    email = db.Column(db.String(128))
    location = db.Column(db.String(200))
    biography = db.Column(db.String(200))
    profile_photo = db.Column(db.String(200))
    joined_on = db.Column(db.DateTime, default=datetime.now)

    def __init__(self, username, password, firstname, lastname, email, location, biography, profile_photo):
        self.username = username
        self.password = generate_password_hash(password, method="pbkdf2:sha256")
        self.firstname = firstname
        self.lastname = lastname
        self.email = email
        self.location = location
        self.biography = biography
        self.profile_photo = profile_photo

    def photo_path(self):
        if self.profile_photo:
            return f'/uploads/{self.profile_photo}'
        else:
            return None

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        try:
            return #unicode(self, id) #python 2 support
        except NameError:
            return str(self.id)  # python 3 support

    def __repr__(self):
        return f'<User {self.id} - {self.username}>'