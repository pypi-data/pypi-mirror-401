from flask import Flask, request, jsonify, render_template_string, session
from flask_login import login_required, current_user
import logging
from datetime import datetime
import hashlib
import os
import sys

# Add QuickDev to path for qdflask import
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../../QuickDev'))

from qdflask import init_auth, create_admin_user
from qdflask.auth import auth_bp
from qdflask.models import db
from qdimages import init_image_manager

app = Flask(__name__)

# Configuration
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv(
    'DATABASE_URL',
    'sqlite:///' + os.path.join(os.path.dirname(__file__), 'commercenode.db')
)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize authentication with CommerceNode-specific roles
init_auth(app, roles=['admin', 'manager', 'staff'])

# Register authentication blueprint
app.register_blueprint(auth_bp)

# Initialize image manager (use the same db instance as qdflask)
init_image_manager(app, {
    'IMAGES_BASE_PATH': os.path.join(os.path.dirname(__file__), '../images'),
    'TEMP_IMAGES_PATH': os.path.join(os.path.dirname(__file__), '../temp_images'),
    'TEMP_DIRECTORY': '/tmp/commercenode_temp',
    'UPLOAD_FOLDER': os.path.join(os.path.dirname(__file__), 'uploads'),
    'MAX_CONTENT_LENGTH': 10 * 1024 * 1024  # 10MB
}, db_instance=db)

# Create admin user on first run
with app.app_context():
    admin_password = os.getenv('ADMIN_PASSWORD', 'admin')
    create_admin_user('admin', admin_password)
    if admin_password == 'admin':
        app.logger.warning("Using default admin password. Change it in production!")


@app.route("/")
def index():
    """Home page with navigation"""
    if current_user.is_authenticated:
        welcome_msg = f"Welcome, {current_user.username} ({current_user.role})"
        logout_link = '<a href="/auth/logout">Logout</a>'
        if current_user.is_admin():
            admin_link = ' | <a href="/auth/users">Manage Users</a>'
        else:
            admin_link = ''
    else:
        welcome_msg = "You are not logged in"
        logout_link = '<a href="/auth/login">Login</a>'
        admin_link = ''

    return f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>CommerceNode</title>
        <style>
            body {{
                font-family: Arial, sans-serif;
                max-width: 800px;
                margin: 50px auto;
                padding: 20px;
                background-color: #f5f5f5;
            }}
            .container {{
                background-color: white;
                padding: 40px;
                border-radius: 8px;
                box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            }}
            h1 {{
                color: #333;
            }}
            p {{
                color: #666;
                line-height: 1.6;
            }}
            .user-info {{
                background: #f0f0f0;
                padding: 15px;
                border-radius: 5px;
                margin: 20px 0;
            }}
            .nav {{
                margin-top: 20px;
                padding-top: 20px;
                border-top: 1px solid #ddd;
            }}
            a {{
                color: #667eea;
                text-decoration: none;
            }}
            a:hover {{
                text-decoration: underline;
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <h1>Welcome to CommerceNode</h1>
            <p>This is the CommerceNode application with user authentication.</p>

            <div class="user-info">
                <strong>User Status:</strong> {welcome_msg}
            </div>

            <div class="nav">
                {logout_link}{admin_link}
                {' | <a href="/image-editor">Image Editor</a>' if current_user.is_authenticated else ''}
            </div>
        </div>
    </body>
    </html>
    """


@app.route("/dashboard")
@login_required
def dashboard():
    """Protected dashboard - requires login"""
    return f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Dashboard - CommerceNode</title>
        <style>
            body {{
                font-family: Arial, sans-serif;
                max-width: 800px;
                margin: 50px auto;
                padding: 20px;
                background-color: #f5f5f5;
            }}
            .container {{
                background-color: white;
                padding: 40px;
                border-radius: 8px;
                box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            }}
            h1 {{
                color: #333;
            }}
            .info {{
                background: #f0f0f0;
                padding: 15px;
                border-radius: 5px;
                margin: 20px 0;
            }}
            a {{
                color: #667eea;
                text-decoration: none;
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <h1>Dashboard</h1>
            <div class="info">
                <p><strong>Username:</strong> {current_user.username}</p>
                <p><strong>Role:</strong> {current_user.role}</p>
                <p><strong>Account Status:</strong> {'Active' if current_user.is_active else 'Inactive'}</p>
                <p><strong>Last Login:</strong> {current_user.last_login.strftime('%Y-%m-%d %H:%M') if current_user.last_login else 'N/A'}</p>
            </div>
            <p><a href="/">← Back to Home</a></p>
        </div>
    </body>
    </html>
    """


@app.route("/ebay/marketplace-account-deletion", methods=["GET"])
def ebay_marketplace_account_deletion_challenge():
    """eBay marketplace account deletion challenge endpoint"""
    end_point = "https://www.commercenode.com/ebay/marketplace-account-deletion"
    challenge_code = request.args.get("challenge_code")
    verification_token = os.getenv("EBAY_VERIFICATION")
    app.logger.info(f"Challenge: {end_point} :: {challenge_code} :: {verification_token}")
    key = challenge_code + verification_token + end_point
    m = hashlib.sha256(key.encode('utf-8'))
    response = m.hexdigest()
    app.logger.info(f"Response: {response}")
    return jsonify({"challengeResponse": response}), 200


@app.route("/ebay/marketplace-account-deletion", methods=["POST"])
def ebay_marketplace_account_deletion_data():
    """
    eBay Marketplace Account Deletion/Closure Notification endpoint.

    This endpoint receives notifications from eBay when a user requests
    account deletion, as required for GDPR compliance.
    """
    try:
        # Get the notification data
        notification_data = request.get_json()

        # Log the notification
        app.logger.info(f"Received eBay marketplace account deletion notification")
        app.logger.info(f"Notification data: {notification_data}")

        # Extract relevant information if available
        if notification_data:
            metadata = notification_data.get("metadata", {})
            notification_id = metadata.get("notificationId", "N/A")
            topic = metadata.get("topic", "N/A")

            app.logger.info(f"Notification ID: {notification_id}")
            app.logger.info(f"Topic: {topic}")

            # Here you would typically:
            # 1. Store the notification in a database
            # 2. Queue a job to process the account deletion
            # 3. Remove user data according to your data retention policy

        # Return success response
        return (
            jsonify(
                {
                    "status": "success",
                    "message": "Notification received",
                    "timestamp": datetime.utcnow().isoformat(),
                }
            ),
            200,
        )

    except Exception as e:
        app.logger.error(f"Error processing eBay notification: {str(e)}", exc_info=True)
        # Still return 200 to acknowledge receipt even if processing fails
        return (
            jsonify(
                {
                    "status": "error",
                    "message": "Notification received but processing failed",
                    "timestamp": datetime.utcnow().isoformat(),
                }
            ),
            200,
        )


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5001)
