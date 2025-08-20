from flask import Blueprint, render_template
from flask_jwt_extended import jwt_required

subscriptions_bp = Blueprint('subscriptions', __name__)


@subscriptions_bp.route('/subscription_plans', methods=['GET'])
def subscription_plans():
    return render_template('subscription_plans.html')

@subscriptions_bp.route('/primium_page', methods=['GET'])
def primium_page():
    return render_template('primium.html')