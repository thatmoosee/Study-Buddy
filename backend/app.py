from flask import Flask, request, jsonify, render_template_string, session
from services.auth_service import AuthService
from repositories.user_repository import UserRepository
from repositories.group_repository import GroupRepository
from services.group_service import GroupService
from models.group import Group
from repositories.friend_repository import FriendRepository
from services.friend_service import FriendService
app = Flask(__name__)
app.secret_key = "super-secret-key"  # TODO: replace with env var later

# Initialize storage (in-memory for now)
user_storage = {}
user_repo = UserRepository(user_storage)
auth_service = AuthService(user_repo)


group_storage = {}
group_repo = GroupRepository(group_storage)
group_service = GroupService(group_repo)

friend_repo = FriendRepository()
friend_service = FriendService(friend_repo)

# HTML Template with session-aware UI
HOME_TEMPLATE = '''
<!DOCTYPE html>
<html>
<head>
    <title>Study Buddy</title>
</head>
<body>
    <h1>Study Buddy</h1>

    <!-- CREATE ACCOUNT -->
    <div id="registerSection">
        <h2>Create Account</h2>
        <form id="registerForm">
            <input type="email" id="regEmail" placeholder="Email" required><br>
            <input type="password" id="regPassword" placeholder="Password" required><br>
            <button type="submit">Create Account</button>
        </form>
    </div>

    <!-- SIGN IN -->
    <div id="loginSection">
        <h2>Sign In</h2>
        <form id="loginForm">
            <input type="email" id="loginEmail" placeholder="Email" required><br>
            <input type="password" id="loginPassword" placeholder="Password" required><br>
            <button type="submit">Sign In</button>
        </form>
    </div>

    <!-- SIGN OUT -->
    <div id="logoutSection" style="display:none;">
        <p id="welcomeMsg"></p>
        <button id="logoutBtn">Sign Out</button>
    </div>

    <div id="message"></div>

    <script>
        async function checkAuthStatus() {
            const res = await fetch('/api/auth/status');
            const data = await res.json();

            if (data.logged_in) {
                document.getElementById('registerSection').style.display = 'none';
                document.getElementById('loginSection').style.display = 'none';
                document.getElementById('logoutSection').style.display = 'block';
                document.getElementById('welcomeMsg').innerText = 'Welcome ' + data.user.email;
            } else {
                document.getElementById('registerSection').style.display = 'block';
                document.getElementById('loginSection').style.display = 'block';
                document.getElementById('logoutSection').style.display = 'none';
            }
        }

        // REGISTER
        document.getElementById('registerForm').addEventListener('submit', async (e) => {
            e.preventDefault();
            const email = document.getElementById('regEmail').value;
            const password = document.getElementById('regPassword').value;

            const res = await fetch('/api/auth/register', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({email, password})
            });
            const data = await res.json();
            document.getElementById('message').innerText = data.message || data.error;

            if (data.success) {
                // Auto login after register
                await fetch('/api/auth/login', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({email, password})
                });
                checkAuthStatus();
            }
        });

        // LOGIN
        document.getElementById('loginForm').addEventListener('submit', async (e) => {
            e.preventDefault();
            const email = document.getElementById('loginEmail').value;
            const password = document.getElementById('loginPassword').value;

            const res = await fetch('/api/auth/login', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({email, password})
            });
            const data = await res.json();
            if (data.success) {
                checkAuthStatus();
            } else {
                document.getElementById('message').innerText = data.error;
            }
        });

        // LOGOUT
        document.getElementById('logoutBtn').addEventListener('click', async () => {
            const res = await fetch('/api/auth/logout', {method: 'POST'});
            const data = await res.json();
            document.getElementById('message').innerText = data.message;
            checkAuthStatus();
        });

        // Run check on page load
        checkAuthStatus();
    </script>
</body>
</html>
'''

@app.route('/')
def home():
    return render_template_string(HOME_TEMPLATE)

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
    
@app.route('/api/group/create', methods=['POST'])
def create_group():
    if 'user_id' not in session:
        return jsonify({'success': False, 'error': 'Not logged in'}), 401
    
    data = request.get_json()
    name = data.get('name')
    members = data.get('members', [])

    if not name:
        return jsonify({'success': False, 'error': 'Group ID is required'}), 400
    try:
        owner_id = session['user_id']
        group = group_service.create_group(name, owner_id, members)
        return jsonify({
            'success': True, 'message': f'Group {group._name} created successfully!',
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
            'success': True, 'message': f'Group {updated_group._name} joined successfully!',
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
            'message': f'You have left {updated_group.name}.',
            'data': updated_group.to_dict()
        })
    except ValueError as e:
        return jsonify({'success': False, 'error': str(e)}), 400

@app.route('/api/friends/add', methods=['POST'])
def add_friend():
    data = request.get_json()
    user = data.get("user")
    friend = data.get("friend")

    success, message = friend_service.add_friend(user, friend)

    return jsonify({
        "success": success,
        "message": message
    }), (200 if success else 400)

@app.route("/remove_friend", methods=["POST"])
def remove_friend():
    data = request.get_json()
    user_id = data.get("user")
    friend_id = data.get("friend")

    try:
        success = friend_service.remove_friend(user_id, friend_id)
        return jsonify({"success": success})
    except ValueError as e:
        return jsonify({"success": False, "message": str(e)}), 400

if __name__ == '__main__':
    print("Study Buddy running on http://localhost:5000")
    app.run(debug=True, host='0.0.0.0', port=5000)
