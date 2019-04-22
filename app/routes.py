from app import app
from flask import render_template, flash, redirect
from app.forms import LoginForm
from flask_login import current_user, login_user



@app.route("/")
@app.route("/index")
def index():
    return(render_template("index.html", title = "Home"))

@app.route("/login", methods = ["POST", "GET"])
def login():
    form = LoginForm()
    if(form.validate_on_submit()):
        flash("Login requested for {}".format(form.username.data))
        return(redirect("/index"))
    return(render_template("login.html", title =  "Sign In", form = form))