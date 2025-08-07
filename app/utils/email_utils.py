from flask_mail import Message
from ..extensions import mail

def send_email(subject, recipients, body, html):
    msg = Message(subject=subject, recipients=recipients, body=body, html=html)
    mail.send(msg)
    