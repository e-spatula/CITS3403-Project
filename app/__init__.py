from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_moment import Moment
from flask_mail import Mail, Message
import os



app = Flask(__name__)
app.config.from_object(Config)

dirname = os.path.dirname(os.path.abspath(__file__))
USER_UPLOAD_FOLDER = dirname + "/static/user-images/"
POLL_UPLOAD_FOLDER = dirname + "/static/poll-images/"
ALLOWED_FILES = ["png", "jpeg", "jpg"]
ADMIN_PIN = "0000"
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
app.config ["MAIL_SERVER"] = "smtp.googlemail.com"
app.config ["MAIL_PORT"] = 587
app.config ["MAIL_USE_TLS"] =  True 
app.config ["MAIL_USERNAME"] = "flaskpolly@gmail.com"
app.config ["MAIL_DEFAULT_SENDER"] = "flaskpolly@gmail.com"
app.config ["MAIL_PASSWORD"] = os.environ.get("MAIL_PASSWORD")


mail = Mail(app)
moment = Moment(app)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
login = LoginManager(app)
login.login_view = "login"


from app import routes, models, errors
