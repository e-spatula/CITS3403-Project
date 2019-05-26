import os, unittest
from app import app, db
from app.models import User, Poll, Votes, Responses
from sqlalchemy import MetaData
from datetime import datetime, timedelta

class RelationshipsTestCase(unittest.TestCase):

    def setUp(self):
        basedir = os.path.abspath(os.path.dirname(__file__))
        app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + os.path.join(basedir, "test.db")
        self.app = app.test_client() # create virtual test env
        db.create_all()
        s1 = User(username = "Eddie", email = "Eddie@gmail.com")
        s1.set_password("Hello")
        s2 = User(username = "Dave", email = "Dave@gmail.com")
        s2.set_password("World")
        poll1 = Poll(title = "My First Poll", user_id = 1, expiry_date = datetime.now())
        poll2 = Poll(title = "Hello World", user_id = 2, expiry_date = datetime.now() + timedelta(days = 30))
        resp1 =  Responses(value = datetime.now(), poll_id  = 1)
        vote1 = Votes(response_id = 1, user_id = 1, poll_id = 1)
        vote2 = Votes(response_id = 1, user_id = 2, poll_id = 1)

        db.session.add(s1)
        db.session.add(s2)
        db.session.add(poll1)
        db.session.add(resp1)
        db.session.add(vote1)
        db.session.add(vote2)
        db.session.add(poll2)
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
    

    def test_user_details(self): 
        user = User.query.get(1)
        self.assertEqual(user.username,"Eddie")
        self.assertEqual(user.email, "Eddie@gmail.com")
        self.assertTrue(user.check_password("Hello"))
        self.assertFalse(user.check_password("World"))
    
    def test_user_relationships(self):
        user = User.query.get(1)
        self.assertEqual(user.polls[0].title, "My First Poll")
        self.assertEqual(user.votes[0].poll_id, 1)
    
    def test_poll_relationships(self):
        poll = Poll.query.get(1)
        self.assertEqual(poll.poll_votes[0].user_id, 1)
        self.assertEqual(poll.poll_options[0].poll_id, 1)


    
if __name__ == "main":
    unittest.main()


