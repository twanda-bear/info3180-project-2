"""
Flask Documentation:     https://flask.palletsprojects.com/
Jinja2 Documentation:    https://jinja.palletsprojects.com/
Werkzeug Documentation:  https://werkzeug.palletsprojects.com/
This file creates your application.
"""
from datetime import  datetime, timedelta
from functools import wraps

import jwt
from flask_login import logout_user
from werkzeug.security import check_password_hash
from werkzeug.utils import secure_filename
from . import db

from app import app, login_manager
from flask import render_template, request, jsonify, send_file, g
import os

from app.forms import RegisterForm, LoginForm, PostForm
from .models import Users, Posts

###
# Routing for your application.
###

ACTIVE = {}

#code from demo
def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.headers.get('Authorization', None) # or request.cookies.get('token', None)

        if not auth:
            return jsonify({'code': 'authorization_header_missing', 'description': 'Authorization header is expected'}), 401

        parts = auth.split()

        if parts[0].lower() != 'bearer':
            return jsonify({'code': 'invalid_header', 'description': 'Authorization header must start with Bearer'}), 401
        elif len(parts) == 1:
            return jsonify({'code': 'invalid_header', 'description': 'Token not found'}), 401
        elif len(parts) > 2:
            return jsonify({'code': 'invalid_header', 'description': 'Authorization header must be Bearer + \s + token'}), 401

        token = parts[1]
        try:
            payload = jwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"])

        except jwt.ExpiredSignatureError:
            return jsonify({'code': 'token_expired', 'description': 'token is expired'}), 401
        except jwt.DecodeError:
            return jsonify({'code': 'token_invalid_signature', 'description': 'Token signature is invalid'}), 401

        g.current_user = user = payload
        return f(*args, **kwargs)
    return decorated

@app.route("/api/v1/generate-token")
def generate_token():
    timestamp = datetime.utcnow()
    payload = {
        "sub": 1, "iat": timestamp, "exp": timestamp + timedelta(minutes=3)
    }

    token = jwt.encode(payload, app.config['SECRET_KEY'], algorithm='HS256')

    return jsonify(token=token)


@login_manager.user_loader
def load_user(uid):
    user = db.session.execute(db.select(Users).filter_by(id=uid)).scalar()
    if user is not None:
        ACTIVE[id] = user
    return user


@app.route('/')
def index():
    return jsonify(message="This is the beginning of our API")


@app.route('/api/ve/register', methods=['POST'])
# Accept user information and saves it to the database
def register():
    if request.method == "POST":
        try:
            register_form = RegisterForm()
            username = register_form.username.data
            password = register_form.password.data
            firstname = register_form.firstname.data
            lastname = register_form.lastname.data
            email = register_form.email.data
            location = register_form.location.data
            biography = register_form.biography.data
            profile_photo = request.files['profile_photo']

            filename = secure_filename(profile_photo.filename)
            profile_photo.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

            #check back

        except Exception as e:
            db.session.rollback()
            print(e)
            return jsonify(error="There was an error registering user: " + str(e)), 400
    return jsonify(errors='This request Method is not valid'), 405

@app.route('/api/v1/auth/login', methods=['POST'])
# Accepts login credentials as username and password
def login():
    if request.method == "POST":
        try:
            login_form = LoginForm()
            username = login_form.username.data
            password = login_form.password.data
            dated = datetime.utcnow()
            #expire =
            #
            user = Users.query.filter_by(username=username).first()
            print(user)

            if user is not None and check_password_hash(user.password, password):
                ###
                return jsonify(status= 'success', message= 'You have successfully logged in')
            return jsonify(errors= "Invalid username or password")
        except Exception as e:
            print (e)
            return jsonify(errors="The was an error processing your request"), 500
    return jsonify(errors="Method request Invalid")


@app.route('/api/v1/auth/logout', methods=['POST'])
# Logs out user
def logout():
    token = request.headers.get('Authorization', None).split(" ")
    try:
        if user_authorized() and len(token) == 2 and token[0].lower() == "bearer":
            payload = jwt.decode(token[1], app.config['SECRET_KEY'], algorithms=['HS256'])
            user = ACTIVE.get(payload.get('sub'), None)
            if user is not None:
                ACTIVE.pop(user.id)
            logout_user()
        return jsonify(status="success", message="User sucessfully logged out."), 200
    except Exception as e:
        print(e)
        return jsonify(errors='An error occurred while processing your request'), 500

@app.route('/api/v1/users/<user_id>/posts', method=['POST'])
# Used for adding post to user feed
def feed_post(user_id):
    post_form = PostForm

    if request.method=="POST" and post_form.validate_on_submit:
        try:
            photo = request.files["photo"] or post_form.photo.data
            caption = post_form.caption.data.strip()

            pic_file = secure_filename(photo.filename)
            parts = pic_file.split(".")
            name = parts[0]
            extension = parts[len(parts)-1]
            filename = name + "_" + datetime.strftime(datetime.now(), "%Y-%m-%dT%H-%M-%S") + f".{extension}"

            post = Posts(caption=caption, photo=filename, user_id=user_id)

            db.session.add(post)
            db.session.commit()
            photo.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return jsonify(status="success", message="New Post Successfully Created"), 200
        except Exception as e:
            db.session.rollback()
            print(e)
            return jsonify(errors=f"Creating New Post Unsuccessful: {e}")
    else:
        return jsonify(errors="Your Request is Unavailable"), 405

"""
@app.route('/api/v1/users/<user_id>/posts', method=['GET'])
# Return a user's post
def return_post(user_id):
    if request.method=="GET":
        try:
            hold = Posts.query.filter_by(user_id=user_id).all()
            posts = []
            for p in hold:
                p_details = {"id":post.id, }
                posts.append(p_details)
""""
###
# #The functions below should be applicable to all Flask apps.
###

# Here we define a function to collect form errors from Flask-WTF
# which we can later use
def form_errors(form):
    error_messages = []
    """Collects form errors"""
    for field, errors in form.errors.items():
        for error in errors:
            message = u"Error in the %s field - %s" % (
                    getattr(form, field).label.text,
                    error
                )
            error_messages.append(message)

    return error_messages

@app.route('/<file_name>.txt')
def send_text_file(file_name):
    """Send your static text file."""
    file_dot_text = file_name + '.txt'
    return app.send_static_file(file_dot_text)


@app.after_request
def add_header(response):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also tell the browser not to cache the rendered page. If we wanted
    to we could change max-age to 600 seconds which would be 10 minutes.
    """
    response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
    response.headers['Cache-Control'] = 'public, max-age=0'
    return response


@app.errorhandler(404)
def page_not_found(error):
    """Custom 404 page."""
    return render_template('404.html'), 404