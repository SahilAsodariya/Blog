from threading import Thread
from flask import current_app

def send_email(subject, recipients, body, html=None):
    """Send email in background using threading."""
    from ..extensions import mail  # import your existing Mail instance

    def _send(subject, recipients, body, html):
        with current_app.app_context():
            from flask_mail import Message
            msg = Message(subject=subject,  
                          recipients=recipients,
                          body=body,
                          html=html)
            mail.send(msg)

    Thread(target=_send, args=(subject, recipients, body, html)).start()
