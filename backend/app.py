from flask import Flask, request, jsonify, session, send_from_directory
from services.auth_service import AuthService
from repositories.user_repository import UserRepository
from repositories.group_repository import GroupRepository
from repositories.notification_repository import NotificationRepository
from repositories.study_scheduler_repository import StudySchedulerRepository
from repositories.chat_repository import ChatRepository
from repositories.profile_repository import ProfileRepository
from repositories.password_reset_token_repository import PasswordResetTokenRepository
from services.group_service import GroupService
from services.profile_service import ProfileService
from services.notification_service import NotificationService
from services.scheduler_services import SchedulerService
from services.chat_service import ChatService
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
token_repo = PasswordResetTokenRepository(os.path.join(DATA_DIR, 'password_reset_tokens.json'))
group_repo = GroupRepository(os.path.join(DATA_DIR, 'groups.json'))
profile_repo = ProfileRepository(os.path.join(DATA_DIR, 'profiles.json'))
notification_repo = NotificationRepository(os.path.join(DATA_DIR, 'notifications.json'))
study_scheduler_repo = StudySchedulerRepository(os.path.join(DATA_DIR, 'study_scheduler.json'))
chat_repo = ChatRepository(os.path.join(DATA_DIR, 'chat.json'))
auth_service = AuthService(user_repo, token_repo)
profile_service = ProfileService(profile_repo)
notification_service = NotificationService(notification_repo)
study_scheduler_service = SchedulerService(study_scheduler_repo)
chat_service = ChatService(chat_repo)

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


from services.password_service import EmailService


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


@app.route('/api/group/listall', methods=['GET'])
def list_all_groups():
    all_groups = group_service.list_all_groups()
    group_list = [group.to_dict() for group in all_groups]
    return jsonify({
        'success': True,
        'groups': group_list
    })


@app.route("/api/notifications", methods=['GET'])
def get_notifications():
    if 'user_id' not in session:
        return jsonify({'success': False, 'error': 'Not logged in'}), 401

    user_id = session['user_id']
    notifications = notification_service.get_notifications(user_id)

    return jsonify({
        'success': True,
        'notifications': notifications
    })


@app.route("/api/notifications/read", methods=['POST'])
def mark_notification_as_read():
    if 'user_id' not in session:
        return jsonify({'success': False, 'error': 'Not logged in'}), 401

    data = request.get_json() or {}
    notification_id = data.get('id')

    if not notification_id:
        return jsonify({'success': False, 'error': 'Notification ID is required'}), 400

    try:
        notification = notification_service.mark_notifications_as_read(notification_id)
        return jsonify({"success": True, "notification": notification.to_dict()})
    except ValueError as e:
        return jsonify({'success': False, 'error': str(e)}), 400

@app.route("/api/study_schedule/create", methods=['POST'])
def create_study_schedule():
    if 'user_id' not in session:
        return jsonify({'success': False, 'error': 'Not logged in'}), 401

    data = request.get_json() or {}
    title = data.get('title')
    start_time = data.get('start_time')
    end_time = data.get('end_time')

    if not title or not start_time or not end_time:
        return jsonify({'success': False, 'error': 'Invalid JSON format'}), 400

    user_id = session['user_id']
    try:
        schedule = study_scheduler_service.create_study_scheduler(user_id, title, start_time, end_time)
        return jsonify({
            'success': True,
            'message': f'Study schedule created successfully!',
            'study': schedule.to_dict()
        })
    except ValueError as e:
        return jsonify({'success': False, 'error': str(e)}), 400

@app.route('/api/chat/create', methods=['POST'])
def create_chat():
    data =request.get_json() or {}
    name = data.get('name')
    owner_id = data.get('owner_id')
    members = data.get('members', [])

    if not name or not owner_id:
        return jsonify({'success': False, 'error': 'Invalid JSON format'}), 400
    chat = chat_service.create_chat(name, owner_id , members)
    return jsonify({
        'success': True,
        'message': f'Chat created successfully!',
        'study': chat.to_dict()
    })

@app.route('/api/chat/join', methods=['POST'])
def send_message(chat_id):
    data = request.get_json() or {}
    message = data.get('message')
    if not chat_id:
        return jsonify({'success': False, 'error': 'Invalid JSON format'}), 400

    chat = chat_service.send_message(chat_id, message)
    return jsonify({
        'success': True,
        'message': f'Chat sent successfully!',
        'study': chat.to_dict()
    })

@app.route('/api/chat/receive', methods=['POST'])
def get_chat(chat_id):
    chat = chat_repo.get(chat_id)
    if not chat:
        return jsonify({'success': False, 'error': 'Chat not found'}), 404

    return jsonify({
        'success': True,
        'message': f'Chat received successfully!',
        'study': chat.to_dict()
    })

@app.route('/api/chat/leave', methods=['POST'])
def leave_chat(chat_id):
    data = request.get_json() or {}
    user_id = data.get('user_id')

    if not chat_id:
        return jsonify({'success': False, 'error': 'Invalid JSON format'}), 400

    chat = chat_service.leave_chat(user_id, chat_id)
    return jsonify({
        'success': True,
        'message': f'Chat leaved successfully!',
        'study': chat.to_dict()
    })

@app.route('/api/group/filter', methods=['POST'])
def filter_groups():
    data = request.get_json()
    filter_type = data.get('type')
    value = data.get('value')
    print(filter_type, value)
    if filter_type == "class":
        groups = group_service.filter_by_specified_class(value)
    elif filter_type == "study":
        groups = group_service.filter_by_study_times(value)
    else:
        return jsonify({'success': False, 'error': 'Invalid JSON format'}), 400

    for group in groups:
        print(group)

    return jsonify({
        'success': True,
        'message': f'Groups filtered successfully!',
        "groups": [group.to_dict() for group in groups]
    })



# main entry point

if __name__ == '__main__':
    print("Study Buddy running at http://localhost:5000")
    # Only enable debug mode in development, and don't expose to all interfaces
    is_dev = os.environ.get('FLASK_ENV') == 'development'
    app.run(debug=is_dev, host='127.0.0.1', port=5000)
