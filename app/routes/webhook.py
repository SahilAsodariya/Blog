from flask import Flask, request, jsonify, Blueprint
from flask_jwt_extended import jwt_required, get_jwt_identity
from ..models import Subscription
from ..schema.schema import SubscriptionSchema
from ..extensions import db
import stripe
from datetime import datetime
from dotenv import load_dotenv
import os

load_dotenv()

weebhook_bp = Blueprint('webhook', __name__)
subscription_schema = SubscriptionSchema(many=True)

# ⚠️ This is your webhook secret from Stripe CLI/Dashboard
WEBHOOK_SECRET = os.getenv("WEBHOOK_SECRET")

@weebhook_bp.route("/webhook", methods=["POST"])

def stripe_webhook():
    payload = request.data
    sig_header = request.headers.get("Stripe-Signature")

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, WEBHOOK_SECRET
        )
    except stripe.error.SignatureVerificationError as e:
        return jsonify({"error": "Invalid signature"}), 400

    # ✅ Handle the event types you care about
    if event["type"] == "checkout.session.completed":
        session = event["data"]["object"]
        customer_email = session.get("customer_details", {}).get("email")
        subscription_id = session.get("subscription")
        if subscription_id:
            sub = stripe.Subscription.retrieve(subscription_id)
            
            # Stripe returns sub['items'] as a ListObject
            items_list = sub['items']['data']  # ✅ Correct access
            if items_list and len(items_list) > 0:
                end_timestamp = items_list[0].get("current_period_end")
                if end_timestamp:
                    from datetime import datetime
                    end_date = datetime.fromtimestamp(end_timestamp)
                    print("Subscription ends at:", end_date)
                else:
                    print("No current_period_end found in items")
            else:
                print("No items found in subscription")
        else:
            print("No subscription id in session")
        user_id = session.get("metadata", {}).get("user_id")  # 👈 recovered here
        eamil = session.get("metadata", {}).get("email")  # 👈 recovered here
        print(f"✅ Checkout completed for {customer_email} with subscription id {subscription_id}")
    
        user = Subscription(user_id=user_id,stripe_subscription_id=subscription_id, email=eamil, end_date=end_date)
        db.session.add(user)
        
    elif event["type"] == "invoice.paid":
        invoice = event["data"]["object"]
        print(f"💰 Invoice paid: {invoice['id']}")

    elif event["type"] == "customer.subscription.deleted":
        subscription = event["data"]["object"]
        subscription_id = subscription['id']
        
        print(f"❌ Subscription canceled: {subscription_id}")
    
        user = Subscription.query.filter_by(stripe_subscription_id=subscription_id).first()
        if user:
            db.session.delete(user)
        else:
            print(f"User with subscription id {subscription_id} not found.") 
            
            
    elif event["type"] == "invoice.payment_failed":
        invoice = event["data"]["object"]
        sub_id = invoice["subscription"]
        print(f"⚠️ Payment failed for subscription {sub_id}")
        # find subscription in DB
        sub = Subscription.query.filter_by(stripe_subscription_id=sub_id).first()
        if sub:
            sub.status = "past_due"  # or "pending" – your choice
            db.session.commit()

        
    elif event["type"] == "customer.subscription.updated":
        subscription = event["data"]["object"]
        status = subscription.get("status")  # active, canceled, past_due, unpaid
        print(f"🔄 Subscription {subscription['id']} updated. New status: {status}")

        sub = Subscription.query.filter_by(stripe_subscription_id=subscription['id']).first()
        if sub:
            sub.status = status
            db.session.commit()

    else:
        print(f"Unhandled event type: {event['type']}")
        
    db.session.commit()  # Commit all changes to the database

    return jsonify(success=True), 200   


