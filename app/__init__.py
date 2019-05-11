from flask import Flask, send_from_directory
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
import os



app = Flask(__name__)
app.config.from_object(Config)

dirname = os.path.dirname(os.path.abspath(__file__))
UPLOAD_FOLDER = dirname + "/static/user-images/"
ALLOWED_FILES = ["png", "jpeg", "jpg"]
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
app.config["ALLOWED_FILES"] = ALLOWED_FILES
db = SQLAlchemy(app)
migrate = Migrate(app, db)
login = LoginManager(app)
login.login_view = "login"


from app import routes, models