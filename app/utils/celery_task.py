from app.celery_app import celery
from datetime import datetime, timedelta
from ..models import Subscription
from ..utils.email_utils import send_email
from app import create_app

app = create_app()

@celery.task(name="app.utils.celery_task.check_subscriptions")
def check_subscriptions():
    with app.app_context():
        today = datetime.utcnow()
        upcoming = today + timedelta(days=7)

        subs = Subscription.query.filter(
            Subscription.end_date <= upcoming,
            Subscription.status == "active"
        ).all()

        for sub in subs:
            days_left = (sub.end_date - today).days
            subject = "Your Subscription is Expiring Soon"
            recipients = [sub.email]
            body = "Important: Your subscription will expire soon. Please renew to continue enjoying our services."
            html = f"<p>Hi, your subscription will expire in <strong>{days_left}</strong> days. Please renew.</p>"
            send_email(subject=subject, recipients=recipients, body=body, html=html)




# from app.celery_app import celery

# @celery.task(name="app.utils.celery_task.check_subscriptions")
# def check_subscriptions():
#     print("✅ Task executed")




