from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField,\
     StringField, IntegerField, FileField, TextAreaField, FormField, Form, \
     FieldList, DateTimeField
from wtforms.validators import DataRequired, ValidationError, Email, EqualTo, Length
from app.models import User
from datetime import datetime

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
    admin = BooleanField("I have an admin pin")

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



def generate_poll_form(options, **kwargs):
    class PollForm(FlaskForm): 
        pass

        def get_responses(self):
            data = self.data
            del data["submit"]
            del data["csrf_token"]
            return(data)

    for i in range(len(options)):
        label = options[i]
        field = BooleanField(label)
        setattr(PollForm, label, field)
    setattr(PollForm, "submit", SubmitField("Submit"))
    return(PollForm(**kwargs))

class CreatePollField(FlaskForm):
    option =  DateTimeField("Date and Time:")

    def validate_option(self, option):
        if(option <= datetime.utcnow()):
            raise ValidationError("Can't put in option in the past")
        
class CreatePollForm(FlaskForm):
    title = StringField("Title:", validators = [DataRequired()])
    expiry_date = DateTimeField("Select when you want this poll to end:", validators = [DataRequired()])
    description = TextAreaField('Poll description', validators=[Length(min=0, max=240)])
    options = FieldList(
        FormField(CreatePollField),
        min_entries = 1,
        max_entries = 20
    )