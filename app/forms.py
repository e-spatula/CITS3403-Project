from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField,\
     StringField, IntegerField, FileField, TextAreaField, FormField, Form, \
     FieldList
from wtforms.validators import DataRequired, ValidationError, Email, EqualTo, Length
from wtforms.fields.html5 import DateField, TimeField
from app.models import User, Poll
from datetime import datetime
from dateparser import parse

class LoginForm(FlaskForm):
    username = StringField("Username", validators = [DataRequired()])
    password =  PasswordField("Password", validators = [DataRequired()])
    submit = SubmitField("Sign In")

class RegistrationForm(FlaskForm):
    username = StringField("Username", validators = [DataRequired()])
    email = StringField("Email", validators = [DataRequired(), Email()])
    password = PasswordField("Password", validators = [DataRequired()])
    password2 = PasswordField(
        "Repeat Password", validators = [DataRequired(), EqualTo("password", message = "Passwords must match")]
    )

    display_picture = FileField("Upload a display picture...or don't I'm not a cop")

    submit = SubmitField("Register")
    
    def validate_username(self, username):
        user = User.query.filter_by(username = username.data).first()
        if(user is not None):
            raise ValidationError("Username taken, please user another")

    def validate_email(self, email):
        email = User.query.filter_by(email = email.data).first()
        if(email is not None):
            raise ValidationError("Email already registered.")

class UploadForm(FlaskForm):
    
    display_picture = FileField("Select photo to upload")

    submit = SubmitField("Upload")
    
class AdminForm(FlaskForm):
    username = StringField("Username:", validators = [DataRequired()])
    pin = PasswordField("PIN:", validators = [DataRequired()])
    submit = SubmitField("Submit")

    def validate_username(self, username):
        user = User.query.filter_by(username = username.data).first()
        if(not user):
            raise ValidationError("User not registered")
    
class EditProfileForm(FlaskForm):
    description = TextAreaField('Personal Description:', validators=[Length(min=0, max=240)])
    submit = SubmitField("Submit")


"""
Function for dynamically creating the vote form. Creates a form and defers its construction until after the 
code below it has executed. The options for the poll are passed as a dictionary from the database
with the key being the response ID and the value being the value of the response.

The responses are taken from the from by getting the forms data and deleting the values for submit button
and CSRF token.
"""
def generate_poll_form(options, **kwargs):
    class PollForm(FlaskForm): 
        pass

        def get_responses(self):
            data = self.data
            del data["submit"]
            del data["csrf_token"]
            return(data) 

    for key in options.keys():
        label = key
        field = BooleanField(options[key])
        setattr(PollForm, label, field)

    setattr(PollForm, "submit", SubmitField("Submit"))
    return(PollForm(**kwargs))

class ResetPasswordRequestForm(FlaskForm):
    email = StringField("Email", validators = [DataRequired(), Email()])
    submit = SubmitField("Reset Password")

class ResetPasswordForm(FlaskForm):
    password = PasswordField("Password", validators = [DataRequired()])
    password2 = PasswordField("Repeat Password", validators = [DataRequired(), EqualTo("password")])
    
    submit = SubmitField("Reset")