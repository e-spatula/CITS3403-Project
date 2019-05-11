from app import app, db, ALLOWED_FILES, UPLOAD_FOLDER
from flask import render_template, flash, redirect, url_for, request
from app.forms import LoginForm, RegistrationForm, AdminForm
from flask_login import current_user, login_user, logout_user, login_required
from app.models import User
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
            flash('Invalid username or password')
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
        admin_pin = os.environ.get("ADMIN_PIN")
        if(admin_pin == form.pin.data):
            current_user.set_admin(True)
            return(redirect(url_for("index")))
        flash("Invalid username or pin")
    return(render_template("admin.html", form = form))
    

@app.route("/register", methods = ["POST", "GET"])
def register():
    if(current_user.is_authenticated):
        return(redirect(url_for("index")))
    form = RegistrationForm()
    if(form.validate_on_submit()):
        user = User(username = form.username.data, email = form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash("Congratulations you have now joined")
        if(form.admin.data):
            next_page = "admin"
        else:
            next_page = "login"
        return(redirect(url_for(next_page)))
    return(render_template("register.html", title = "Register", form = form))

@app.route('/user/<username>')
@login_required
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    polls = [
        {'author': user, 'body': 'Test post #1'},
        {'author': user, 'body': 'Test post #2'}
    ]
    
    return render_template('user.html', user=user, polls = polls)

@app.route('/upload')
@login_required
def upload():
    return (render_template("upload.html", title = "Upload"))

def allowed_file(file):
    return(file.filename.split(".")[1].lower() in ALLOWED_FILES)

def previous_file_checker():
    for file in os.listdir(UPLOAD_FOLDER):
        file_id = file.split(".")[0] 
        if(file_id == str(current_user.id)):
            return(UPLOAD_FOLDER + file)

@app.route("/upload", methods = ["POST"])
@login_required
def upload_file():
    if(request.method == "POST"):
        if("file" not in request.files):
            print(request.files)
            flash("No file part")
            return(redirect("upload"))
        file = request.files["file"]
        if(not file.filename):
            flash("No file uploaded!")
            return(redirect("upload"))
        if(not allowed_file(file)):
            flash("Unsupported image type")
            return(redirect(url_for("upload")))
        if(file):
            previous_file = previous_file_checker()
            extension = file.filename.split(".")[1]
            filename = secure_filename(str(current_user.id) + "." + extension)
            file.save(os.path.join(UPLOAD_FOLDER, filename))
            if(previous_file):
                os.remove(previous_file)
            flash("Files successfully uploaded")
            return(redirect(url_for("user", username = current_user.username)))
