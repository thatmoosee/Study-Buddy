from flask import Flask, request, jsonify, render_template_string
from services.auth_service import AuthService
from repositories.user_repository import UserRepository

app = Flask(__name__)

# Initialize storage
user_storage = {}
user_repo = UserRepository(user_storage)
auth_service = AuthService(user_repo)

# Simple HTML template
HOME_TEMPLATE = '''
<!DOCTYPE html>
<html>
<head>
    <title>Study Buddy</title>
</head>
<body>
    <h1>Study Buddy</h1>
    <h2>Create Account</h2>
    <form id="registerForm">
        <label>Email:</label><br>
        <input type="email" id="email" required><br><br>
        <label>Password:</label><br>
        <input type="password" id="password" required><br><br>
        <button type="submit">Create Account</button>
    </form>
    <div id="message"></div>

    <script>
        document.getElementById('registerForm').addEventListener('submit', async (e) => {
            e.preventDefault();
            const email = document.getElementById('email').value;
            const password = document.getElementById('password').value;
            
            try {
                const response = await fetch('/api/auth/register', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({email, password})
                });
                const data = await response.json();
                
                if (data.success) {
                    document.getElementById('message').innerHTML = '<p style="color:green;">' + data.message + '</p>';
                    document.getElementById('registerForm').reset();
                } else {
                    document.getElementById('message').innerHTML = '<p style="color:red;">' + data.error + '</p>';
                }
            } catch (error) {
                document.getElementById('message').innerHTML = '<p style="color:red;">Error: ' + error + '</p>';
            }
        });
    </script>
</body>
</html>
'''

@app.route('/')
def home():
    return render_template_string(HOME_TEMPLATE)

@app.route('/api/auth/register', methods=['POST'])
def register():
    try:
        data = request.get_json()
        if not data:
            return jsonify({'success': False, 'error': 'Request body is required'}), 400
        
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
    except Exception as e:
        return jsonify({'success': False, 'error': f'Server error: {str(e)}'}), 500

if __name__ == '__main__':
    print("Study Buddy running on http://localhost:5000")
    app.run(debug=True, host='0.0.0.0', port=5000)