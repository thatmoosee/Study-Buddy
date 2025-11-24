from flask import Flask, request, jsonify, session, send_from_directory
from services.auth_service import AuthService
from services.email_service import EmailService
from repositories.user_repository import UserRepository
from repositories.group_repository import GroupRepository
from repositories.profile_repository import ProfileRepository
from repositories.password_reset_token_repository import PasswordResetTokenRepository
from services.group_service import GroupService
from services.profile_service import ProfileService
from models.group import Group
import os
import secrets

# Load environment variables from .env file if it exists
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass  # python-dotenv not installed, environment variables must be set manually

# Compute correct paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FRONTEND_DIR = os.path.join(BASE_DIR, '..', 'frontend')
DATA_DIR = os.path.join(BASE_DIR, 'data')  
# Ensure data directory exists
os.makedirs(DATA_DIR, exist_ok=True) 

# Flask setup
app = Flask(
    __name__,
    static_folder=FRONTEND_DIR,
    static_url_path=''
)
# Use environment variable for secret key, fallback to generated key
app.secret_key = os.environ.get('SECRET_KEY') or secrets.token_hex(32) 

# Initialize repositories and services with absolute paths
user_repo = UserRepository(os.path.join(DATA_DIR, 'users.json'))
group_repo = GroupRepository(os.path.join(DATA_DIR, 'groups.json'))
profile_repo = ProfileRepository(os.path.join(DATA_DIR, 'profiles.json'))
auth_service = AuthService(user_repo)
profile_service = ProfileService(profile_repo)

token_repo = PasswordResetTokenRepository(os.path.join(DATA_DIR, 'password_reset_tokens.json'))

# Initialize email service (will raise error if SENDGRID_API_KEY not set)
try:
    email_service = EmailService()
    auth_service = AuthService(user_repo, token_repo, email_service)
except ValueError as e:
    print(f"Warning: Email service not configured - {e}")
    print("Password reset functionality will not be available")
    auth_service = AuthService(user_repo)

group_repo = GroupRepository(os.path.join(DATA_DIR, 'groups.json'))
group_service = GroupService(group_repo)



# FRONTEND ROUTES


@app.route('/')
def serve_index():
    """Serve the main frontend page (index.html)"""
    return send_from_directory(app.static_folder, 'index.html')


@app.route('/<path:path>')
def serve_frontend(path):
    """Serve any file from the frontend directory"""
    full_path = os.path.join(app.static_folder, path)
    if os.path.exists(full_path):
        return send_from_directory(app.static_folder, path)
    else:
        return send_from_directory(app.static_folder, 'index.html')



# AUTHENTICATION ROUTES


@app.route('/api/auth/register', methods=['POST'])
def register():
    try:
        data = request.get_json()
        if not data:
            return jsonify({'success': False, 'error': 'Request body is required'}), 400
    except Exception:
        return jsonify({'success': False, 'error': 'Invalid JSON format'}), 400

    try:
        email = data.get('email')
        password = data.get('password')
        user = auth_service.register(email, password)
        return jsonify({
            'success': True,
            'message': 'Account created successfully',
            'data': {'user': user.to_dict()}
        }), 201
    except ValueError as e:
        return jsonify({'success': False, 'error': str(e)}), 400


@app.route('/api/auth/login', methods=['POST'])
def login():
    try:
        data = request.get_json()
        if not data:
            return jsonify({'success': False, 'error': 'Request body is required'}), 400
    except Exception:
        return jsonify({'success': False, 'error': 'Invalid JSON format'}), 400

    try:
        email = data.get('email')
        password = data.get('password')
        user = auth_service.login(email, password)
        session['user_id'] = user.id
        session['email'] = user.email
        return jsonify({'success': True, 'message': 'Login successful', 'data': {'user': user.to_dict()}})
    except ValueError as e:
        return jsonify({'success': False, 'error': str(e)}), 401


@app.route('/api/auth/logout', methods=['POST'])
def logout():
    auth_service.logout(session)
    return jsonify({'success': True, 'message': 'Logged out successfully'})


@app.route('/api/auth/status', methods=['GET'])
def auth_status():
    if 'user_id' in session:
        return jsonify({
            'logged_in': True,
            'user': {
                'user_id': session['user_id'],
                'email': session['email']
            }
        })
    return jsonify({'logged_in': False})


@app.route('/api/auth/forgot-password', methods=['POST'])
def forgot_password():
    try:
        data = request.get_json()
        if not data:
            return jsonify({'success': False, 'error': 'Request body is required'}), 400
    except Exception:
        return jsonify({'success': False, 'error': 'Invalid JSON format'}), 400

    try:
        email = data.get('email')
        if not email:
            return jsonify({'success': False, 'error': 'Email is required'}), 400

        # Request password reset (returns None if user doesn't exist for security)
        auth_service.request_password_reset(email)

        # Always return success to prevent user enumeration
        return jsonify({
            'success': True,
            'message': 'If an account exists with this email, password reset instructions have been sent.'
        }), 200
    except ValueError as e:
        error_message = str(e)
        # If it's a configuration error, return 503
        if 'not configured' in error_message.lower():
            return jsonify({'success': False, 'error': 'Password reset service is currently unavailable'}), 503
        # For validation errors or email sending failures, return 400
        return jsonify({'success': False, 'error': error_message}), 400
    except Exception as e:
        # Catch unexpected errors
        print(f"Unexpected error in forgot_password: {str(e)}")
        return jsonify({'success': False, 'error': 'An unexpected error occurred'}), 500


@app.route('/api/auth/reset-password', methods=['POST'])
def reset_password():
    try:
        data = request.get_json()
        if not data:
            return jsonify({'success': False, 'error': 'Request body is required'}), 400
    except Exception:
        return jsonify({'success': False, 'error': 'Invalid JSON format'}), 400

    try:
        token = data.get('token')
        new_password = data.get('new_password')

        if not token or not new_password:
            return jsonify({'success': False, 'error': 'Token and new password are required'}), 400

        # Reset password using token
        user = auth_service.reset_password(token, new_password)

        return jsonify({
            'success': True,
            'message': 'Password has been reset successfully. You can now login with your new password.'
        }), 200
    except ValueError as e:
        error_message = str(e)
        # If it's a configuration error, return 503
        if 'not configured' in error_message.lower():
            return jsonify({'success': False, 'error': 'Password reset service is currently unavailable'}), 503
        # For invalid token or validation errors, return 400
        return jsonify({'success': False, 'error': error_message}), 400
    except Exception as e:
        # Catch unexpected errors
        print(f"Unexpected error in reset_password: {str(e)}")
        return jsonify({'success': False, 'error': 'An unexpected error occurred'}), 500



# GROUP ROUTES


@app.route('/api/group/create', methods=['POST'])
def create_group():
    if 'user_id' not in session:
        return jsonify({'success': False, 'error': 'Not logged in'}), 401

    try:
        data = request.get_json()
        if not data:
            return jsonify({'success': False, 'error': 'Request body is required'}), 400
    except Exception:
        return jsonify({'success': False, 'error': 'Invalid JSON format'}), 400

    name = data.get('name')
    members = data.get('members', [])

    if not name:
        return jsonify({'success': False, 'error': 'Group name is required'}), 400

    try:
        owner_id = session['user_id']
        group = group_service.create_group(name, owner_id, members)
        return jsonify({
            'success': True,
            'message': f'Group {group.name} created successfully!',
            'data': group.to_dict()
        })
    except ValueError as e:
        return jsonify({'success': False, 'error': str(e)}), 400


@app.route('/api/group/join', methods=['POST'])
def join_group():
    if 'user_id' not in session:
        return jsonify({'success': False, 'error': 'Not logged in'}), 401

    try:
        data = request.get_json()
        if not data:
            return jsonify({'success': False, 'error': 'Request body is required'}), 400
    except Exception:
        return jsonify({'success': False, 'error': 'Invalid JSON format'}), 400

    if 'group_id' not in data:
        return jsonify({'success': False, 'error': 'Group ID is required'}), 400

    try:
        user_id = session['user_id']
        group_id = data['group_id']
        updated_group = group_service.join_group(user_id, group_id)
        return jsonify({
            'success': True,
            'message': f'Group {updated_group.name} joined successfully!',
            'data': updated_group.to_dict()
        })
    except ValueError as e:
        return jsonify({'success': False, 'error': str(e)}), 400


@app.route('/api/group/leave', methods=['POST'])
def leave_group():
    if 'user_id' not in session:
        return jsonify({'success': False, 'error': 'Not logged in'}), 401

    try:
        data = request.get_json()
        if not data:
            return jsonify({'success': False, 'error': 'Request body is required'}), 400
    except Exception:
        return jsonify({'success': False, 'error': 'Invalid JSON format'}), 400

    if 'group_id' not in data:
        return jsonify({'success': False, 'error': 'Group ID is required'}), 400

    try:
        user_id = session['user_id']
        group_id = data['group_id']
        updated_group = group_service.leave_group(user_id, group_id)
        return jsonify({
            'success': True,
            'message': f'You have left {updated_group.name}.',
            'data': updated_group.to_dict()
        })
    except ValueError as e:
        return jsonify({'success': False, 'error': str(e)}), 400
    
@app.route('/api/group/list', methods=['GET'])
def list_groups():
    if 'user_id' not in session:
        return jsonify({'success': False, 'error': 'Not logged in'}), 401

    user_id = session['user_id']

    # Get groups user belongs to using service method
    user_groups = group_service.get_user_groups(user_id)
    groups = [g.to_dict() for g in user_groups]

    return jsonify({
        'success': True,
        'groups': groups
    })

@app.route('/api/profile/upload', methods=['POST'])
def upload_profile():
    if 'user_id' not in session:
        return jsonify({'success': False, 'error': 'Not logged in'}), 401
    data = request.get_json() or {}
    user_id = session['user_id']
    profile = profile_service.upload_profile(user_id, data)
    return jsonify({'success': True, 'message':'Profile updated successfully', 'profile': profile.to_dict()})






# main entry point

if __name__ == '__main__':
    print("Study Buddy running at http://localhost:5000")
    # Only enable debug mode in development, and don't expose to all interfaces
    is_dev = os.environ.get('FLASK_ENV') == 'development'
    app.run(debug=is_dev, host='127.0.0.1', port=5000)
