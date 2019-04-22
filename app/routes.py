from app import app
from flask import render_template
from app.forms import LoginForm
from flask_login import current_user, login_user


@app.route("/")
@app.route("/index")
def index():
    return(render_template("index.html", title = "Home"))

@app.route("/login")
def login():
    form = LoginForm()
    return(render_template("login.html", title =  "Sign In", form = form))