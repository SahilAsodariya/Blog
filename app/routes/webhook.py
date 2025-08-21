from flask import Flask, request, jsonify, Blueprint
from flask_jwt_extended import jwt_required, get_jwt_identity
from ..models import Subscription
from ..schema.schema import SubscriptionSchema
from ..extensions import db
import stripe
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
        user_id = session.get("metadata", {}).get("user_id")  # 👈 recovered here
        print(f"✅ Checkout completed for {customer_email} with subscription id {subscription_id}")
    
        user = Subscription(user_id=user_id,stripe_subscription_id=subscription_id)
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
    else:
        print(f"Unhandled event type: {event['type']}")
        
    db.session.commit()  # Commit all changes to the database

    return jsonify(success=True), 200

@weebhook_bp.route("/webhook/user", methods=["GET"])
def get_user_subscription():    
    user = Subscription.query.all()
    result = subscription_schema.dump(user)
    return jsonify(result), 200


@weebhook_bp.route("/webhook/delete/user", methods=["POST"])
def delete_user_subscription():    
    user = Subscription.query.all()
    for u in user:
        db.session.delete(u)
    db.session.commit()
    return jsonify("Badha saff ho bhai."), 200