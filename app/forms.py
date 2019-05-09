from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, StringField, IntegerField
from wtforms.validators import DataRequired, ValidationError, DataRequired, Email, EqualTo
from app.models import User

class LoginForm(FlaskForm):
    username = StringField("Username", validators = [DataRequired()])
    password =  PasswordField("Password", validators = [DataRequired()])
    submit = SubmitField("Sign In")

class RegistrationForm(FlaskForm):
    username = StringField("Username", validators = [DataRequired()])
    email = StringField("Email", validators = [DataRequired(), Email()])
    password = PasswordField("Password", validators = [DataRequired()])
    password2 = PasswordField(
        "Repeat Password", validators = [DataRequired(), EqualTo("password")]
    )
    admin = BooleanField("I have an admin pin")
    submit = SubmitField("Register")

    def validate_username(self, username):
        user = User.query.filter_by(username = username.data).first()
        if(user is not None):
            raise ValidationError("Username taken, please user another")

    def validation_email(self, email):
        email = User.query.filter_by(email = email.data).first()
        if(email is not None):
            raise ValidationError("Email already registered.")

class AdminForm(FlaskForm):
    username = StringField("Username:", validators = [DataRequired()])
    pin = PasswordField("PIN:", validators = [DataRequired()])
    submit = SubmitField("Submit")

    def validate_username(self, username):
        user = User.query.filter_by(username = username.data).first()
        if(not user):
            raise ValidationError("User not registered")
    
