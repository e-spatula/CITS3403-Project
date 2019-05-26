from flask_mail import Message
from flask import render_template
from app import mail, app


"""
Function for sending
"""
def send_email(subject, sender, recipients, text_body, html_body):
    msg = Message(subject, sender = sender, recipients = recipients)
    msg.body = text_body
    msg.html = html_body
    mail.send(msg)


def send_password_reset_email(user):
    token = user.get_reset_password_token()
    send_email("Password reset token", sender = app.config["MAIL_DEFAULT_SENDER"],
     recipients = [user.email], text_body = render_template("email/reset_password.txt", user = user,
     token = token), html_body = render_template("email/reset_password.html", user = user, token = token))
    
def send_confirmation_email(user):
     token = user.generate_confirmation_token()
     send_email("Email address confirmation email", sender = app.config["MAIL_DEFAULT_SENDER"],
     recipients = [user.email], text_body = render_template("email/email_confirmation.txt", user = user, token = token), 
     html_body  = render_template("email/email_confirmation.html", user = user, token = token))

