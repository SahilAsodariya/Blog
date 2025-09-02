from flask import Blueprint, jsonify, render_template, request
from flask_jwt_extended import jwt_required, get_jwt_identity
import stripe
from ..models import User

stripe_bp = Blueprint('stripe', __name__)

@stripe_bp.route("/")
def index():
    return render_template("index.html")

@stripe_bp.route('/create-checkout', methods=['POST'])  
@jwt_required()  # Ensure the user is authenticated
def create_checkout_session():
    user_id = get_jwt_identity()
    user = User.query.filter_by(id=user_id).first()
    email = user.email
    
    try:
        checkout_session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=[{
            'price': 'price_1Ry9weDb35IcydsnWAh4Ul3m',  # subscription price ID from Stripe
            'quantity': 1,
        }],
        mode='subscription',
        success_url=f'{request.url_root}stripe/success?session_id={{CHECKOUT_SESSION_ID}}',
        cancel_url=f'{request.url_root}stripe/cancel',
        metadata={
        "user_id": user_id,  # 👈 store your app's user_id here
        "email" : email
    }
    )
        return jsonify({'id': checkout_session.id})
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@stripe_bp.route('/success', methods=['GET'])
def success():
    return render_template('primium.html')

@stripe_bp.route('/cancel', methods=['GET'])        
def cancel():
    return jsonify({'message': 'Payment cancelled.'}), 200






