from app import db
from datetime import datetime
from sqlalchemy.sql import func


results = db.Table("results", 
    db.Column("response_id", db.Integer, db.ForeignKey("responses.id")),
    db.Column("vote_id",db.Integer, db.ForeignKey("votes.id"))
     )

class User(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(64), index = True, unique = True)
    email = db.Column(db.String(128), index = True, unique = True, nullable = False)
    password_hash = db.Column(db.String(128))
    is_admin = db.Column(db.Boolean(), default = False)
    polls = db.relationship("Poll", backref = "author", lazy = "dynamic")
    votes = db.relationship("Votes", backref = "voter", lazy = "dynamic")

    
    def __repr__(self):
        return("User<{}>".format(self.username))

class Poll(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(64), nullable = False)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    create_date = db.Column(db.DateTime, index = True, server_default = func.now())
    expiry_date = db.Column(db.DateTime, index = True)
    poll_votes = db.relationship("Votes", backref = "poll", lazy = "dynamic")
    poll_options = db.relationship("Responses", backref = "poll", lazy = "dynamic")

    def __init__(self, title, user_id):
        self.title = title
        self.user_id = user_id
        self.date = date if date else datetime.utcnow() + datetime.timedelta(days = 30)
    def __repr__(self):
        return("Poll{}".format(self.title))

class Responses(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    value = db.Column(db.DateTime, index = True, nullable = False)
    poll_id = db.Column(db.Integer, db.ForeignKey("poll.id"))
    votes = db.relationship("Votes", secondary = results, back_populates = "responses")
    

    def __repr__(self):
        return("Response {}, made on poll {}".format(self.value, self.poll_id))

class Votes(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    response_id = db.Column(db.Integer, db.ForeignKey("responses.id"))
    time = db.Column(db.DateTime, server_default = func.now())
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    poll_id = db.Column(db.Integer, db.ForeignKey("poll.id"))
    responses = db.relationship("Responses", secondary = results, back_populates = "votes")


    def __repr__(self):
        return("Vote {} placed at {}".format(self.id, self.time))

