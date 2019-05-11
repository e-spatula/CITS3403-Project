from app import db, login, UPLOAD_FOLDER
from datetime import datetime, timedelta
from sqlalchemy.sql import func
from werkzeug.security import check_password_hash, generate_password_hash
from flask_login import UserMixin
from flask import url_for
from hashlib import md5
import os

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
    polls = db.relationship("Poll", backref = "author", lazy = "dynamic")
    votes = db.relationship("Votes", backref = "voter", lazy = "dynamic")

    def avatar(self, size):
        for file in os.listdir(UPLOAD_FOLDER):
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
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    description = db.Column(db.String(240))
    create_date = db.Column(db.DateTime, index = True, server_default = func.now())
    expiry_date = db.Column(db.DateTime, index = True, nullable = False, default = datetime.utcnow() + timedelta(days = 1))
    poll_votes = db.relationship("Votes", backref = "poll", lazy = "dynamic")
    poll_options = db.relationship("Responses", backref = "poll", lazy = "dynamic")

    def __repr__(self):
        return("Poll <{}>".format(self.title))

class Responses(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    value = db.Column(db.DateTime, index = True, nullable = False)
    poll_id = db.Column(db.Integer, db.ForeignKey("poll.id"))
    

    def __repr__(self):
        return("Response {}, made on poll {}".format(self.value, self.poll_id))

class Votes(db.Model):
    response_id = db.Column(db.Integer, db.ForeignKey("responses.id"), primary_key = True)
    time = db.Column(db.DateTime, server_default = func.now())
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), primary_key = True)
    poll_id = db.Column(db.Integer, db.ForeignKey("poll.id"), primary_key = True)


    def __repr__(self):
        return("Vote {} placed at {} with value {}".format(self.id, self.time, self.response_id))

