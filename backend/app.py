"""
Main Flask application with API routes and endpoints

Built by: Josh Topp, Josh Schmidt, Max Quirk
"""
from flask import Flask, request, jsonify, session, send_from_directory
from services.auth_service import AuthService
from repositories.user_repository import UserRepository
from repositories.group_repository import GroupRepository
from repositories.friend_repository import FriendRepository
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
from services.friend_service import FriendService
from models.group import Group
import os
import secrets


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
friend_repo = FriendRepository(os.path.join(DATA_DIR, 'friends.json'))
notification_repo = NotificationRepository(os.path.join(DATA_DIR, 'notifications.json'))
study_scheduler_repo = StudySchedulerRepository(os.path.join(DATA_DIR, 'schedule.json'))
chat_repo = ChatRepository(os.path.join(DATA_DIR, 'chat.json'))
auth_service = AuthService(user_repo, token_repo)
friend_service = FriendService(friend_repo,user_repo)
profile_service = ProfileService(profile_repo)
notification_service = NotificationService(notification_repo)
study_scheduler_service = SchedulerService(study_scheduler_repo)
chat_service = ChatService(chat_repo)

group_repo = GroupRepository(os.path.join(DATA_DIR, 'groups.json'))
group_service = GroupService(group_repo)


# HELPER FUNCTIONS

def convert_ids_to_emails(user_ids):
    """Convert a list of user IDs to emails"""
    emails = []
    for user_id in user_ids:
        user = user_repo.find_by_id(user_id)
        if user:
            emails.append(user.email)
        else:
            emails.append(str(user_id))  # Fallback to ID if user not found
    return emails

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
    """Request password reset - generates token for in-app use"""
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

        # Request password reset token
        reset_token = auth_service.request_password_reset(email)

        if reset_token:
            # Return token for in-app display (no email sending)
            return jsonify({
                'success': True,
                'message': 'Password reset link generated successfully.',
                'token': reset_token.token
            }), 200
        else:
            # User doesn't exist, but don't reveal this for security
            return jsonify({
                'success': True,
                'message': 'If an account exists with this email, a reset link has been generated.'
            }), 200

    except ValueError as e:
        error_message = str(e)
        # If it's a configuration error, return 503
        if 'not configured' in error_message.lower():
            return jsonify({'success': False, 'error': 'Password reset service is currently unavailable'}), 503
        # For validation errors, return 400
        return jsonify({'success': False, 'error': error_message}), 400
    except Exception as e:
        # Catch unexpected errors
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
    study_times = data.get('study_times',[])
    specified_class = data.get('specified_class',[])
    if not name:
        return jsonify({'success': False, 'error': 'Group name is required'}), 400

    try:
        owner_id = session['user_id']
        group = group_service.create_group(name, owner_id, members, study_times, specified_class)
        chat_service.create_chat(name, owner_id, members, group.to_dict().get('id', None))

        # Convert member IDs to emails
        group_dict = group.to_dict()
        group_dict['members'] = convert_ids_to_emails(group_dict['members'])

        return jsonify({
            'success': True,
            'message': f'Group {group.name} created successfully!',
            'data': group_dict
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
        return jsonify({'success': False, 'error': 'Group ID or name is required'}), 400

    try:
        user_id = session['user_id']
        group_id = data['group_id']
        updated_group = group_service.join_group(user_id, group_id)
        chat_service.join_chat(user_id, group_id)
        group = group_service.get_group(group_id)
        for member in group.to_dict()['members']:
            if user_id == member:
                notification_service.send_notification(member, f"You joined the group {group.to_dict()['name']}")
            else:
                notification_service.send_notification(member, f"{user_id} joined the group {group.to_dict()['name']}")
        # Convert member IDs to emails
        group_dict = updated_group.to_dict()
        group_dict['members'] = convert_ids_to_emails(group_dict['members'])

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
        return jsonify({'success': False, 'error': 'Group ID or name is required'}), 400

    try:
        user_id = session['user_id']
        group_id = data['group_id']

        # Get group info before leaving
        group_before = group_service.get_group(group_id)
        if not group_before:
            return jsonify({'success': False, 'error': 'Group not found'}), 400

        group_name = group_before.name

        # Leave the group (may delete if last member)
        updated_group = group_service.leave_group(user_id, group_id)
        chat_service.leave_chat(user_id, group_id)

        # Check if group still exists after leaving
        group_after = group_service.get_group(group_id)

        # Send notifications to remaining members
        if group_after:
            for member in group_after.members:
                if member != user_id:
                    notification_service.send_notification(member, f"{user_id} left the group {group_name}")

        # Send notification to user who left
        notification_service.send_notification(user_id, f"You left the group {group_name}")

        return jsonify({
            'success': True,
            'message': f'You have left {group_name}.',
            'group_deleted': group_after is None
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
    groups = []
    for g in user_groups:
        group_dict = g.to_dict()
        group_dict['members'] = convert_ids_to_emails(group_dict['members'])
        groups.append(group_dict)
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
    group_list = []
    for group in all_groups:
        group_dict = group.to_dict()
        group_dict['members'] = convert_ids_to_emails(group_dict['members'])
        group_list.append(group_dict)
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
        'notifications': [notification.to_dict() for notification in notifications]
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

@app.route("/api/notifications/delete", methods=['POST'])
def delete_notifications():
    if 'user_id' not in session:
        return jsonify({'success': False, 'error': 'Not logged in'}), 401

    data = request.get_json() or {}
    notification_id = data.get('id')
    if not notification_id:
        return jsonify({'success': False, 'error': 'Notification ID is required'}), 400

    try:
        notification_service.delete_notification(notification_id)
        return jsonify({"success": True})
    except ValueError as e:
        return jsonify({'success': False, 'error': str(e)}), 400



@app.route("/api/study_schedule/create", methods=['POST'])
def create_study_schedule():
    if 'user_id' not in session:
        return jsonify({'success': False, 'error': 'Not logged in'}), 401

    data = request.get_json() or {}
    title = data.get('session_name')
    start_time = data.get('start_date')
    end_time = data.get('end_date')
    group_id = data.get('group_id') or None

    if not title or not start_time or not end_time:
        return jsonify({'success': False, 'error': 'Invalid JSON format'}), 400

    user_id = session['user_id']
    try:
        if group_id:
            group = group_service.get_group(group_id)
            for member in group.to_dict()['members']:
                schedule = study_scheduler_service.create_study_scheduler(member, title, start_time, end_time, group_id)
                if user_id == member:
                    notification_service.send_notification(member,
                                                           f"You created a Study Schedule for Group {group.to_dict()['name']} from {start_time} to {end_time}")
                else:
                    notification_service.send_notification(member,
                                                           f"{user_id} rceated a Study Schedule for Group {group.to_dict()['name']} from {start_time} to {end_time}")

        return jsonify({
            'success': True,
            'message': f'Study schedule created successfully!',
            'study': schedule.to_dict()
        })
    except ValueError as e:
        return jsonify({'success': False, 'error': str(e)}), 400

@app.route("/api/study_schedule/get", methods=['GET'])
def get_study_schedule():
    if 'user_id' not in session:
        return jsonify({'success': False, 'error': 'Not logged in'}), 401

    user_id = session['user_id']
    try:
        schedules = study_scheduler_service.get_user_sessions(user_id)
        schedule = [sessions.to_dict() for sessions in schedules]
        return jsonify({
            'success': True,
            'message': f"Study schedule retrieved successfully!",
            'study': schedule
        })
    except ValueError as e:
        return jsonify({'success': False, 'error': str(e)}), 400

@app.route('/api/study_schedule/delete', methods=["POST"])
def delete_study_schedule():
    if 'user_id' not in session:
        return jsonify({'success': False, 'error': 'Not logged in'}), 401

    data = request.get_json() or {}
    session_id = data.get('id')
    if not session_id:
        return jsonify({'success': False, 'error': 'session id is required'}), 400

    try:
        study_scheduler_service.delete_session(session_id)
        return jsonify({"success": True})
    except ValueError as e:
        return jsonify({'success': False, 'error': str(e)}), 400

@app.route('/api/chat/join', methods=['POST'])
def join_chat():
    data = request.get_json() or {}
    chat_id = data.get('chat_id')
    user_id = session['user_id']
    if not chat_id or not user_id:
        return jsonify({'success': False, 'error': 'Invalid JSON format'}), 401

    chat = chat_service.join_chat(user_id, chat_id)
    group = chat_service.get_chat(chat_id)
    for member in group.to_dict()['members']:
        if user_id == member:
            notification_service.send_notification(member, f"You joined a Chat {group.to_dict()['name']}!")
        else:
            notification_service.send_notification(member, f"{user_id} joined a Chat {group.to_dict()['name']}!")
    # Convert member IDs to emails
    chat_dict = chat.to_dict()
    chat_dict['members'] = convert_ids_to_emails(chat_dict['members'])

    return jsonify({
        'success': True,
        'message': f'Chat joined successfully!',
        'chats': chat.to_dict()
    })

@app.route('/api/chat/create', methods=['POST'])
def create_chat():
    data = request.get_json() or {}
    name = data.get('name')
    owner_id = session['user_id']
    members = data.get('members', [])

    if not name or not owner_id:
        return jsonify({'success': False, 'error': 'Invalid JSON format'}), 400
    chat = chat_service.create_chat(name, owner_id, members)
    notification_service.send_notification(owner_id, f"You created a Chat {name}")

    # Convert member IDs to emails
    chat_dict = chat.to_dict()
    chat_dict['members'] = convert_ids_to_emails(chat_dict['members'])

    return jsonify({
        'success': True,
        'message': f'Chat created successfully!',
        'chats': chat.to_dict()
    })

@app.route('/api/chat/send', methods=['POST'])
def send_message():
    data = request.get_json() or {}
    chat_id = data.get('chat_id')
    message = data.get('message')
    user_id = session['user_id']
    if not chat_id:
        return jsonify({'success': False, 'error': 'Invalid JSON format'}), 400

    # Get user email to use in message
    user = user_repo.find_by_id(user_id)
    user_email = user.email if user else str(user_id)

    chat = chat_service.send_message(user_id, chat_id, message, user_email)
    group = chat_service.get_chat(chat_id)
    for member in chat.members:
        if user_id == member:
            pass
        else:
            notification_service.send_notification(member, f"{user_email} just sent a message in {group.to_dict()['name']}!")

    # Convert member IDs to emails
    chat_dict = chat.to_dict()
    chat_dict['members'] = convert_ids_to_emails(chat_dict['members'])

    return jsonify({
        'success': True,
        'message': f'Chat sent successfully!',
        'study': chat_dict
    })

@app.route('/api/chat/receive', methods=['POST'])
def get_chat():
    data = request.get_json() or {}
    chat = data.get('chat')
    if not chat:
        return jsonify({'success': False, 'error': 'Chat not found'}), 404

    return jsonify({
        'success': True,
        'message': f'Chat received successfully!',
        'chats': chat.to_dict()
    })

@app.route('/api/chat/leave', methods=['POST'])
def leave_chat():
    data = request.get_json() or {}
    chat_id = data.get('chat_id')
    user_id = session['user_id']

    if not chat_id:
        return jsonify({'success': False, 'error': 'Invalid JSON format'}), 400

    chat = chat_service.leave_chat(user_id, chat_id)
    group = chat_service.get_chat(chat_id)
    for member in group.to_dict()['members']:
        if user_id == member:
            notification_service.send_notification(member, f"You left a Chat {group.to_dict()['name']}!")
        else:
            notification_service.send_notification(member, f"{user_id} left a Chat {group.to_dict()['name']}!")

    # Convert member IDs to emails
    chat_dict = chat.to_dict()
    chat_dict['members'] = convert_ids_to_emails(chat_dict['members'])

    return jsonify({
        'success': True,
        'message': f'Chat leaved successfully!',
        'chats': chat_dict
    })

@app.route('/api/chat/listallchats', methods=['GET'])
def list_all_chats():
    user_id = session['user_id']
    if not user_id:
        return jsonify({'success': False, 'error': 'Not logged in'}), 401

    user_chats = chat_service.list_all_chats(user_id)

    # Convert member IDs to emails in each chat
    for chat_id, chat in user_chats.items():
        chat['members'] = convert_ids_to_emails(chat['members'])

    return jsonify({
        'success': True,
        'message': f'Chat listed successfully!',
        'chats': user_chats
    })

@app.route('/api/group/filter', methods=['POST'])
def filter_groups():
    data = request.get_json()
    filter_type = data.get('type')
    value = data.get('value')
    print(data)
    print(filter_type, value)
    if not filter_type or not value:
        return jsonify({
            "success": False,
            "error": "Missing a field"
        })

    if filter_type == "class":
        print(value)
        groups = group_service.filter_by_specified_class(value)
    elif filter_type == "time":
        groups = group_service.filter_by_study_times(value)
    else:
        return jsonify({'success': False, 'error': 'Invalid JSON format'}), 400
    # Convert member IDs to emails
    group_list = []
    for group in groups:
        group_dict = group.to_dict()
        group_dict['members'] = convert_ids_to_emails(group_dict['members'])
        group_list.append(group_dict)

    return jsonify({
        'success': True,
        'message': f'Groups filtered successfully!',
        "groups": group_list
    })

# FRIEND ROUTES


@app.route('/api/friend/remove', methods=['POST'])
def remove_friend():
    """Remove a friend"""
    if 'user_id' not in session:
        return jsonify({'success': False, 'error': 'Not logged in'}), 401

    try:
        data = request.get_json()
        if not data:
            return jsonify({'success': False, 'error': 'Request body is required'}), 400
    except Exception:
        return jsonify({'success': False, 'error': 'Invalid JSON format'}), 400

    if 'friend_id' not in data:
        return jsonify({'success': False, 'error': 'Friend ID is required'}), 400

    try:
        user_id = session['user_id']
        friend_id = int(data['friend_id'])
        friend_service.remove_friend(user_id, friend_id)
        return jsonify({
            'success': True,
            'message': 'Friend removed successfully'
        })
    except ValueError as e:
        return jsonify({'success': False, 'error': str(e)}), 400


@app.route('/api/friend/request', methods=['POST'])
def send_friend_request():
    """Send a friend request by email"""
    if 'user_id' not in session:
        return jsonify({'success': False, 'error': 'Not logged in'}), 401

    try:
        data = request.get_json()
        if not data:
            return jsonify({'success': False, 'error': 'Request body is required'}), 400
    except Exception:
        return jsonify({'success': False, 'error': 'Invalid JSON format'}), 400

    if 'email' not in data:
        return jsonify({'success': False, 'error': 'Email is required'}), 400

    try:
        user_id = session['user_id']
        friend_email = data['email']
        success, message, friend_id = friend_service.send_friend_request(user_id, friend_email)

        if success:
            # Send notification to the recipient
            notification_service.send_notification(friend_id, f"You have a new friend request!")
            return jsonify({
                'success': True,
                'message': message
            })
        else:
            return jsonify({'success': False, 'error': message}), 400
    except ValueError as e:
        return jsonify({'success': False, 'error': str(e)}), 400


@app.route('/api/friend/accept', methods=['POST'])
def accept_friend_request():
    """Accept a friend request"""
    if 'user_id' not in session:
        return jsonify({'success': False, 'error': 'Not logged in'}), 401

    try:
        data = request.get_json()
        if not data:
            return jsonify({'success': False, 'error': 'Request body is required'}), 400
    except Exception:
        return jsonify({'success': False, 'error': 'Invalid JSON format'}), 400

    if 'request_id' not in data:
        return jsonify({'success': False, 'error': 'Request ID is required'}), 400

    try:
        user_id = session['user_id']
        request_id = data['request_id']

        # Get the friendship to find the other user
        friendship = friend_service.friend_repo.find_by_id(request_id)
        if not friendship:
            return jsonify({'success': False, 'error': 'Friend request not found'}), 400

        requester_id = friendship.user_id

        success, message = friend_service.accept_friend_request(user_id, request_id)

        if success:
            # Create a DM chat between the two friends
            try:
                chat = chat_service.create_DM(user_id, requester_id)
                notification_service.send_notification(requester_id, f"Your friend request was accepted!")

                # Convert member IDs to emails
                chat_dict = chat.to_dict()
                chat_dict['members'] = convert_ids_to_emails(chat_dict['members'])

                return jsonify({
                    'success': True,
                    'message': f'{message} A chat has been created!',
                    'chat': chat_dict
                })
            except Exception as e:
                # Friend was accepted but chat creation failed
                return jsonify({
                    'success': True,
                    'message': message,
                    'warning': 'Chat creation failed'
                })
        else:
            return jsonify({'success': False, 'error': message}), 400
    except ValueError as e:
        return jsonify({'success': False, 'error': str(e)}), 400



@app.route('/api/friend/reject', methods=['POST'])
def reject_friend_request():
    """Reject a friend request"""
    if 'user_id' not in session:
        return jsonify({'success': False, 'error': 'Not logged in'}), 401

    try:
        data = request.get_json()
        if not data:
            return jsonify({'success': False, 'error': 'Request body is required'}), 400
    except Exception:
        return jsonify({'success': False, 'error': 'Invalid JSON format'}), 400

    if 'request_id' not in data:
        return jsonify({'success': False, 'error': 'Request ID is required'}), 400

    try:
        user_id = session['user_id']
        request_id = data['request_id']
        success, message = friend_service.reject_friend_request(user_id, request_id)

        if success:
            return jsonify({
                'success': True,
                'message': message
            })
        else:
            return jsonify({'success': False, 'error': message}), 400
    except ValueError as e:
        return jsonify({'success': False, 'error': str(e)}), 400


@app.route('/api/friend/requests', methods=['GET'])
def get_friend_requests():
    """Get pending friend requests for the logged-in user"""
    if 'user_id' not in session:
        return jsonify({'success': False, 'error': 'Not logged in'}), 401

    try:
        user_id = session['user_id']
        requests = friend_service.get_pending_requests(user_id)

        return jsonify({
            'success': True,
            'requests': requests
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400


@app.route('/api/friend/list', methods=['GET'])
def list_friends():
    """Get list of friends for the logged-in user"""
    if 'user_id' not in session:
        return jsonify({'success': False, 'error': 'Not logged in'}), 401

    try:
        user_id = session['user_id']
        friend_ids = friend_service.get_friends_list(user_id)

        # Fetch user details, profile, and chats for each friend
        friends_list = []
        for friend_id in friend_ids:
            try:
                friend_user = user_repo.find_by_id(friend_id)
                if friend_user:
                    friend_data = {
                        'id': friend_user.id,
                        'email': friend_user.email
                    }

                    # Get friend's profile
                    try:
                        friend_profile = profile_repo.find_by_user_id(friend_id)
                        if friend_profile:
                            friend_data['profile'] = {
                                'name': friend_profile.name,
                                'major': friend_profile.major,
                                'availability': friend_profile.availability
                            }
                        else:
                            friend_data['profile'] = None
                    except Exception as e:
                        friend_data['profile'] = None

                    # Get chats that the friend is in
                    friend_chats = []
                    try:
                        all_chats = chat_service.list_all_chats(friend_id)
                        for chat_id, chat in all_chats.items():
                            friend_chats.append({
                                'chat_id': chat_id,
                                'name': chat['name']
                            })
                    except Exception:
                        pass
                    friend_data['chats'] = friend_chats

                    friends_list.append(friend_data)
            except Exception as e:
                continue

        return jsonify({
            'success': True,
            'friends': friends_list
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400


@app.route("/students/search", methods=["GET"])
def search_student():
    email = request.args.get("email", "").strip().lower()
    if not email:
        return jsonify({"error": "Email parameter required"}), 400

    user = user_repo.find_by_email(email)
    if user:
        return jsonify({"found": True, "student": user}), 200
    else:
        return jsonify({"found": False, "message": "Student not found"}), 404

if __name__ == '__main__':
    print("Study Buddy running at http://localhost:5000")
    # Only enable debug mode in development, and don't expose to all interfaces
    is_dev = os.environ.get('FLASK_ENV') == 'development'
    app.run(debug=is_dev, host='127.0.0.1', port=5000)
