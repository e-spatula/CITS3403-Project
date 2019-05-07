from app import db
from datetime import datetime
from sqlalchemy.sql import func
from werkzeug.security import check_password_hash, generate_password_hash


class User(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(64), index = True, unique = True)
    email = db.Column(db.String(128), index = True, unique = True, nullable = False)
    password_hash = db.Column(db.String(128), nullable = False)
    is_admin = db.Column(db.Boolean(), default = False)
    polls = db.relationship("Poll", backref = "author", lazy = "dynamic")
    votes = db.relationship("Votes", backref = "voter", lazy = "dynamic")

    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return(check_password_hash(self.password_hash, password))

    def __repr__(self):
        return("User<{}>".format(self.username))
     

class Poll(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(64), nullable = False)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    create_date = db.Column(db.DateTime, index = True, server_default = func.now())
    expiry_date = db.Column(db.DateTime, index = True, nullable = False)
    poll_votes = db.relationship("Votes", backref = "poll", lazy = "dynamic")
    poll_options = db.relationship("Responses", backref = "poll", lazy = "dynamic")

    def __init__(self, title, user_id, expiry_date):
        self.title = title
        self.user_id = user_id
        self.expiry_date = expiry_date if expiry_date else datetime.utcnow() + datetime.timedelta(days = 30)
    def __repr__(self):
        return("Poll <{}>".format(self.title))

class Responses(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    value = db.Column(db.DateTime, index = True, nullable = False)
    poll_id = db.Column(db.Integer, db.ForeignKey("poll.id"))
    votes = db.relationship("Votes", back_populates = "responses")
    

    def __repr__(self):
        return("Response {}, made on poll {}".format(self.value, self.poll_id))

class Votes(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    response_id = db.Column(db.Integer, db.ForeignKey("responses.id"))
    time = db.Column(db.DateTime, server_default = func.now())
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    poll_id = db.Column(db.Integer, db.ForeignKey("poll.id"))
    responses = db.relationship("Responses", back_populates = "votes")


    def __repr__(self):
        return("Vote {} placed at {} with value {}".format(self.id, self.time, self.response_id))

