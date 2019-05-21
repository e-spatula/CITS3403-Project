from app import app, db, login, USER_UPLOAD_FOLDER, POLL_UPLOAD_FOLDER
from datetime import datetime, timedelta
from sqlalchemy.sql import func
from werkzeug.security import check_password_hash, generate_password_hash
from flask_login import UserMixin
from flask import url_for
from hashlib import md5
import os
from time import time
import jwt 


@login.user_loader
def user_loader(id):
    return(User.query.get(int(id)))

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(64), index = True, unique = True)
    email = db.Column(db.String(128), index = True, unique = True, nullable = False)
    password_hash = db.Column(db.String(128), nullable = False)
    is_admin = db.Column(db.Boolean(), default = False)
    description = db.Column(db.String(240))
    last_seen = db.Column(db.DateTime, default = func.now())
    polls = db.relationship("Poll", backref = "author", lazy = "dynamic", cascade = "all,delete")
    votes = db.relationship("Votes", backref = "voter", lazy = "dynamic", cascade = "all,delete")

    def get_reset_password_token(self, expires_in = 600):
        return(jwt.encode(
            {"reset_password": self.id, "exp" : time() + expires_in},
            app.config["SECRET_KEY"], algorithm = "HS256").decode("utf-8"))

    @staticmethod
    def verify_reset_token(token):
        try:
            id = jwt.decode(token, app.config["SECRET_KEY"], algorithms = ["HS256"])["reset_password"]

        except:
            return
    
        return(User.query.get(id))

    def delete(self):
        for file in os.listdir(USER_UPLOAD_FOLDER):
            file_id = file.split(".")[0] 
            if(file_id == self.username):
                path = USER_UPLOAD_FOLDER + file
                os.remove(path)
        db.session.delete(self)
        db.session.commit()

    def avatar(self, size):
        for file in os.listdir(USER_UPLOAD_FOLDER):
            file_id = file.split(".")[0] 
            if(file_id == self.username):
                return(url_for("static", filename = "user-images/" + file))
        digest = md5(self.email.lower().encode("utf-8")).hexdigest()
        return(("https://www.gravatar.com/avatar/{}?d=retro&s={}").format(digest, size))

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return(check_password_hash(self.password_hash, password))
    def get_name(self):
        return(self.username)
    def get_admin(self):
        return(self.is_admin)
    def set_admin(self, status):
        self.is_admin = status
        db.session.commit()
    def __repr__(self):
        return("User<{}>".format(self.username))
     

class Poll(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(64), nullable = False)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id", onupdate = "CASCADE", ondelete = "CASCADE"))
    description = db.Column(db.String(240))
    create_date = db.Column(db.DateTime, index = True, server_default = func.now())
    expiry_date = db.Column(db.DateTime, index = True, nullable = False, default = datetime.utcnow() + timedelta(days = 30))
    option_limit = db.Column(db.Integer, nullable = False, default = -1)
    poll_votes = db.relationship("Votes", backref = "poll", lazy = "dynamic", cascade = "all,delete")
    poll_options = db.relationship("Responses", backref = "poll", lazy = "dynamic", cascade = "all,delete")

    def delete(self):
        for file in os.listdir(POLL_UPLOAD_FOLDER):
            file_id = file.split(".")[0] 
            if(file_id == self.id):
                path = POLL_UPLOAD_FOLDER + file
                os.remove(path)
        db.session.delete(self)
        db.session.commit()


    def get_display_picture(self):
        for file in os.listdir(POLL_UPLOAD_FOLDER):
            file_id = file.split(".")[0] 
            if(file_id == str(self.id)):
                return(url_for("static", filename = "poll-images/" + file))
        # image credit https://www.flaticon.com/free-icon/ballot-box_1750198 
        return(url_for("static", filename = "images/ballot-box.png"))

    def has_expired(self):
        return(self.expiry_date < datetime.utcnow())

    def __repr__(self):
        return("Poll <{}>".format(self.title))

class Responses(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    value = db.Column(db.DateTime, index = True, nullable = False)
    poll_id = db.Column(db.Integer, db.ForeignKey("poll.id", onupdate = "CASCADE", ondelete = "CASCADE"))
    
    def __repr__(self):
        return("{}".format(self.value))
    def get_value(self, id):
        value = Poll.query.get(id)
        return(str(value))

    def get_count(self):
        count = list(Votes.query.filter_by(response_id = self.id))
        return(len(count))

class Votes(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    response_id = db.Column(db.Integer, db.ForeignKey("responses.id", onupdate = "CASCADE", ondelete = "CASCADE"))
    time = db.Column(db.DateTime, server_default = func.now())
    user_id = db.Column(db.Integer, db.ForeignKey("user.id", onupdate = "CASCADE", ondelete = "CASCADE"))
    poll_id = db.Column(db.Integer, db.ForeignKey("poll.id", onupdate = "CASCADE", ondelete = "CASCADE"))


    def __repr__(self):
        return("Vote {} placed at {} on poll {} with value {}".format(self.id, self.time, self.poll_id, self.response_id))

