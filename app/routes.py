from app import app, db, ALLOWED_FILES, UPLOAD_FOLDER, ADMIN_PIN
from flask import render_template, flash, redirect, url_for, request
from app.forms import LoginForm, RegistrationForm, AdminForm, EditProfileForm, generate_poll_form, UploadForm
from flask_login import current_user, login_user, logout_user, login_required
from app.models import User, Poll, Responses, Votes
from werkzeug.urls import url_parse
from werkzeug.utils import secure_filename
from datetime import datetime
import os


@app.before_request
def before_request():
    if(current_user.is_authenticated):
        current_user.last_seen = datetime.utcnow()
        db.session.commit()

@app.route("/")
@app.route("/index")
def index():
    return(render_template("index.html", title = "Home"))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if (current_user.is_authenticated):
        return(redirect(url_for('index')))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if(user is None or not user.check_password(form.password.data)):
            flash('Invalid username or password', category = "error")
            return(redirect(url_for('login')))
        login_user(user)
        next_page = request.args.get("next")
        if(not next_page or url_parse(next_page).netloc != ""):
            next_page = url_for("index")
        return(redirect(next_page))
    return(render_template('login.html', title='Sign In', form=form))


@app.route("/logout")
def logout():
    logout_user()
    return(redirect(url_for("index")))

@app.route("/admin", methods = ["POST", "GET"])
@login_required
def admin():
    if(current_user.get_admin()):
        return(redirect(url_for("index")))
    form = AdminForm()
    if(form.validate_on_submit()):
        admin_pin = ADMIN_PIN
        if(admin_pin == form.pin.data):
            current_user.set_admin(True)
            return(redirect(url_for("index")))
        form.pin.errors.append("Admin pin incorrect")
    return(render_template("admin.html", form = form))
    

@app.route("/register", methods = ["POST", "GET"])
def register():
    if(current_user.is_authenticated):
        return(redirect(url_for("index")))
    form = RegistrationForm()
    if(form.validate_on_submit()):
        user = User(username = form.username.data, email = form.email.data)
        user.set_password(form.password.data)
        if(form.display_picture.data):
            if(not file_uploader(form.username.data, form.display_picture.data)):
                db.session.rollback()
                return(redirect(url_for("register")))
        db.session.add(user)
        db.session.commit()
        flash("Congratulations you have now joined", category = "info")
        if(form.admin.data):
            next_page = "admin"
        else:
            next_page = "login"
        return(redirect(url_for(next_page)))
    return(render_template("register.html", title = "Register", form = form))

@app.route('/upload')
@login_required
def upload():
    form = UploadForm()
    return (render_template("upload.html", title = "Upload", form = form))

def allowed_file(file):
    return(file.filename.split(".")[1].lower() in ALLOWED_FILES)

def previous_file_checker():
    for file in os.listdir(UPLOAD_FOLDER):
        file_id = file.split(".")[0] 
        if(file_id == current_user.username):
            return(UPLOAD_FOLDER + file)

def file_uploader(username, file):
    if(request.method == "POST"):
        if(not file.filename):
            flash("No file uploaded!", category = "error")
            return(False)
        if(not allowed_file(file)):
            flash("Unsupported image type", category = "error")
            return(False)
        if(file):
            previous_file = ""
            extension = file.filename.split(".")[1]  
            if(current_user.is_authenticated):  
                previous_file = previous_file_checker()
            filename = secure_filename(username + "." + extension)
            if(previous_file):
                print(previous_file)
                os.remove(previous_file)
            file.save(os.path.join(UPLOAD_FOLDER, filename))
            flash("Files successfully uploaded", category = "info")
            return(True)


@app.route("/upload", methods = ["POST"])
@login_required
def upload_file():
    file = request.files["file"]
    if(file_uploader(current_user.username, file)):
        return(redirect(url_for("index")))
    else:
        return(redirect(url_for("upload")))

@app.route('/user/<username>')
@login_required
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    polls = Poll.query.filter_by(user_id = user.id)
    
    return render_template('user.html', user=user, polls = polls)

@app.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm()
    if(form.validate_on_submit()):
        current_user.description = form.description.data
        db.session.commit()
        flash('Your changes have been saved.', category = "info")
        return redirect(url_for('edit_profile'))
    elif(request.method == 'GET'):
        form.description.data = current_user.description
    return( render_template('edit_profile.html', title='Edit Profile', form=form))


def valid_vote(options, vote_limit):
    checked_options = 0
    for option in options.keys():
        if(options[option]):
            checked_options += 1
    if(checked_options == 0):
        flash("You haven't selected any options", category = "error")
        return(False)
    if(vote_limit == -1):
        return(True)
    elif(vote_limit > 0 and checked_options > vote_limit):
        flash("You have selected too many options, you are only allowed {} options and you have selected {}".format(vote_limit, checked_options), category = "error")
        return(False)
    else:
        return(True)




@app.route("/poll/<id>", methods = ["GET", "POST"])
def poll(id):
    poll = Poll.query.filter_by(id = id).first_or_404()
    options = poll.poll_options
    options_list = []
    options_values = []
    for option in options:
        options_list.append(str(option.id))
        options_values.append(option.value)
    
    option_limit = poll.option_limit
    form = generate_poll_form(options_list)

    if(form.validate_on_submit()):
        voted_options = form.get_responses()
        if(not can_vote(current_user, poll)):
            flash("You have already voted you sneaky devil", category = "error")
            return(render_template("poll-page.html", poll = poll, form = form, options_values = options_values))
        if(valid_vote(voted_options, option_limit)):
            for key in voted_options.keys():
                if(voted_options[key]):
                    vote = Votes(response_id = key, user_id = current_user.id, poll_id = id)
                    db.session.add(vote)
            db.session.commit()
            flash("Vote counted!", category = "info")
            return(redirect(url_for("index")))
    return(render_template("poll-page.html", poll = poll, form = form, options_values = options_values))

def can_vote(user, poll):
    responses = poll.poll_votes
    for response in responses:
        if(response.user_id == user.id):
            return(False)
    return(True)