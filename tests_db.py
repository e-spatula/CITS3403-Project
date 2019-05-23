import os, unittest
from app import app, db
from app.models import User, Poll, Votes, Responses
from sqlalchemy import MetaData
import datetime

class RelationshipsTestCase(unittest.TestCase):

    def setUp(self):
        basedir = os.path.abspath(os.path.dirname(__file__))
        app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + os.path.join(basedir, "test.db")
        self.app = app.test_client() # create virtual test env
        db.create_all()
        # TODO: set password hashes to use the method.
        s1 = User(username = "Eddie", email = "Eddie@gmail.com", password_hash = "hello")
        s2 = User(username = "Dave", email = "Dave@gmail.com", password_hash = "helloworld")
        poll1 = Poll(title = "My First Poll", user_id = 1, expiry_date = datetime.datetime.now())
        resp1 =  Responses(value = datetime.datetime.now(), poll_id  = 1)
        vote1 = Votes(response_id = 1, user_id = 1, poll_id = 1)
        vote2 = Votes(response_id = 1, user_id = 2, poll_id = 1)

        db.session.add(s1)
        db.session.add(s2)
        db.session.add(poll1)
        db.session.add(resp1)
        db.session.add(vote1)
        db.session.add(vote2)
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
    

    def test_user_details(self): 
        user = User.query.get(1)
        self.assertEqual(user.username,"Eddie")
        self.assertEqual(user.email, "Eddie@gmail.com")
        self.assertEqual(user.password_hash, "hello")
    
    def test_user_relationships(self):
        user = User.query.get(1)
        self.assertEqual(user.polls[0].title, "My First Poll")
        self.assertEqual(user.votes[0].poll_id, 1)
    
    def test_poll_relationships(self):
        poll = Poll.query.get(1)
        self.assertEqual(poll.poll_votes[0].user_id, 1)
        self.assertEqual(poll.poll_options[0].poll_id, 1)
    
    def test_responses_relationships(self):
        response = Responses.query.get(1)
        self.assertEqual(response.votes[0].user_id,1)
        self.assertEqual(response.votes[1].user_id,2)
    
    def test_votes_relationships(self):
        vote1 = Votes.query.get(1)
        vote2 = Votes.query.get(2)
        self.assertEqual(vote1.responses.poll_id, 1)
        self.assertEqual(vote1.responses.poll_id, 1)

if __name__ == "main":
    unittest.main()


