from flask import Flask, request, jsonify, session, send_from_directory
from services.auth_service import AuthService
from repositories.user_repository import UserRepository
from repositories.group_repository import GroupRepository
from services.group_service import GroupService
from models.group import Group
import os

# Compute correct path to frontend directory (one level up)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FRONTEND_DIR = os.path.join(BASE_DIR, '..', 'frontend')

# Flask setup
app = Flask(
    __name__,
    static_folder=FRONTEND_DIR,       # Serve files from ../frontend
    static_url_path=''                # So /index.html works at /
)
app.secret_key = "super-secret-key" 

# Initialize repositories and services
user_storage = {}
user_repo = UserRepository(user_storage)
auth_service = AuthService(user_repo)

group_storage = {}
group_repo = GroupRepository(group_storage)
group_service = GroupService(group_repo)

# ======================
# FRONTEND ROUTES
# ======================

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


# ======================
# AUTHENTICATION ROUTES
# ======================

@app.route('/api/auth/register', methods=['POST'])
def register():
    data = request.get_json()
    if not data:
        return jsonify({'success': False, 'error': 'Request body is required'}), 400

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
    data = request.get_json()
    if not data:
        return jsonify({'success': False, 'error': 'Request body is required'}), 400

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


# ======================
# GROUP ROUTES
# ======================

@app.route('/api/group/create', methods=['POST'])
def create_group():
    if 'user_id' not in session:
        return jsonify({'success': False, 'error': 'Not logged in'}), 401
    
    data = request.get_json()
    name = data.get('name')
    members = data.get('members', [])

    if not name:
        return jsonify({'success': False, 'error': 'Group name is required'}), 400

    try:
        owner_id = session['user_id']
        group = group_service.create_group(name, owner_id, members)
        return jsonify({
            'success': True,
            'message': f'Group {group._name} created successfully!',
            'data': {'id': group.id, 'name': group._name, 'members': group._members}
        })
    except ValueError as e:
        return jsonify({'success': False, 'error': str(e)}), 400


@app.route('/api/group/join', methods=['POST'])
def join_group():
    if 'user_id' not in session:
        return jsonify({'success': False, 'error': 'Not logged in'}), 401

    data = request.get_json()
    if not data or 'group_id' not in data:
        return jsonify({'success': False, 'error': 'Group ID is required'}), 400

    try:
        user_id = session['user_id']
        group_id = data['group_id']
        updated_group = group_service.join_group(user_id, group_id)
        return jsonify({
            'success': True,
            'message': f'Group {updated_group._name} joined successfully!',
            'data': {'id': updated_group.id, 'name': updated_group._name, 'members': updated_group._members}
        })
    except ValueError as e:
        return jsonify({'success': False, 'error': str(e)}), 400


@app.route('/api/group/leave', methods=['POST'])
def leave_group():
    if 'user_id' not in session:
        return jsonify({'success': False, 'error': 'Not logged in'}), 401

    data = request.get_json()
    if not data or 'group_id' not in data:
        return jsonify({'success': False, 'error': 'Group ID is required'}), 400

    try:
        user_id = session['user_id']
        group_id = data['group_id']
        updated_group = group_service.leave_group(user_id, group_id)
        return jsonify({
            'success': True,
            'message': f'You have left {updated_group._name}.',
            'data': updated_group.to_dict()
        })
    except ValueError as e:
        return jsonify({'success': False, 'error': str(e)}), 400


# ======================
# ENTRY POINT
# ======================

if __name__ == '__main__':
    print("Study Buddy running at http://localhost:5000")
    app.run(debug=True, host='0.0.0.0', port=5000)
