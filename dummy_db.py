from app import db 
from app.models import User, Poll, Responses, Votes

User.query.delete()

names = ["Joey Bloggs", "Jane Bloggs", "John Citizen", "Janet Citizen"]
email = ["joey@example.com", "jane@gmail.com", "john@hotmail.com", "janet@outlook.com"]

for i in range(len(names)):
    u = User(username = names[i], email = email[i], password_hash = names[i][:3], is_admin = False)
    db.session.add(u)
db.session.commit()

users = User.query.all()
for u in users:
    print(u)