from flask import Flask
from .config import Config
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import CSRFProtect
import os
from flask_wtf.csrf import CSRFProtect

app = Flask(__name__)
app.config.from_object(Config)
app.secret_key = os.environ.get('FLASK_SECRET_KEY', 'default_secret_key')

csrf = CSRFProtect(app)

db = SQLAlchemy(app)
migrate = Migrate(app, db)
from app import views