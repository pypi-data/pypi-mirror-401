import os
import json
import webbrowser
from flask import Flask, request, render_template_string
import threading
import time

AUTH_FILE = os.path.expanduser("~/.clipsync/auth.json")

# Firebase Config (provided by user)
FIREBASE_CONFIG = {
    "apiKey": "AIzaSyCCxDr_YYWPtx2TMAe-Ba5rZNzm_dqL_98",
    "authDomain": "do-so-fffm46.firebaseapp.com",
    "projectId": "do-so-fffm46",
    "storageBucket": "do-so-fffm46.firebasestorage.app",
    "messagingSenderId": "799239330915",
    "appId": "1:799239330915:web:a0d7c0ada1c7eadea5ac56"
}

LOGIN_HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>clipSync Login</title>
    <script src="https://www.gstatic.com/firebasejs/9.22.0/firebase-app-compat.js"></script>
    <script src="https://www.gstatic.com/firebasejs/9.22.0/firebase-auth-compat.js"></script>
    <script src="https://www.gstatic.com/firebasejs/9.22.0/firebase-firestore-compat.js"></script>
    <style>
        body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; display: flex; justify-content: center; align-items: center; height: 100vh; background: #121212; color: white; }
        .container { background: #1e1e1e; padding: 2rem; border-radius: 8px; box-shadow: 0 4px 6px rgba(0,0,0,0.3); width: 400px; text-align: center; border: 1px solid #fbc02d; }
        h1 { color: #fbc02d; margin-bottom: 1.5rem; }
        input, select, textarea { width: 100%; padding: 10px; margin: 10px 0; border-radius: 4px; border: 1px solid #333; background: #2c2c2c; color: white; box-sizing: border-box; }
        button { background: #fbc02d; color: black; border: none; padding: 12px 20px; border-radius: 4px; cursor: pointer; font-weight: bold; width: 100%; margin-top: 10px; }
        button:hover { background: #f9a825; }
        .hidden { display: none; }
    </style>
</head>
<body>
    <div class="container">
        <h1>XDT Labs clipSync</h1>
        <div id="auth-section">
            <input type="email" id="email" placeholder="Email">
            <input type="password" id="password" placeholder="Password">
            <button onclick="login()">Login / Sign Up</button>
        </div>
        <div id="profile-section" class="hidden">
            <h3>Complete Profile</h3>
            <input type="text" id="name" placeholder="Full Name">
            <input type="text" id="mobile" placeholder="Mobile Number">
            <input type="text" id="profession" placeholder="Profession">
            <textarea id="reason" placeholder="Why are you using this?"></textarea>
            <button onclick="saveProfile()">Start Syncing</button>
        </div>
        <p id="status"></p>
    </div>

    <script>
        const firebaseConfig = """ + json.dumps(FIREBASE_CONFIG) + """;
        firebase.initializeApp(firebaseConfig);
        const auth = firebase.auth();
        const db = firebase.firestore();

        async function login() {
            const email = document.getElementById('email').value;
            const password = document.getElementById('password').value;
            document.getElementById('status').innerText = "Authenticating...";
            
            try {
                // Try to create user, if fails try to login
                let userCredential;
                try {
                    userCredential = await auth.createUserWithEmailAndPassword(email, password);
                } catch (err) {
                    userCredential = await auth.signInWithEmailAndPassword(email, password);
                }
                
                const user = userCredential.user;
                // Check if profile exists
                const userDoc = await db.collection('users').doc(user.uid).get();
                if (userDoc.exists) {
                    finish(user.uid, user.email);
                } else {
                    document.getElementById('auth-section').classList.add('hidden');
                    document.getElementById('profile-section').classList.remove('hidden');
                }
            } catch (error) {
                document.getElementById('status').innerText = "Error: " + error.message;
            }
        }

        async function saveProfile() {
            const user = auth.currentUser;
            const profile = {
                name: document.getElementById('name').value,
                mobile: document.getElementById('mobile').value,
                profession: document.getElementById('profession').value,
                reason: document.getElementById('reason').value,
                email: user.email,
                uid: user.uid,
                createdAt: firebase.firestore.FieldValue.serverTimestamp()
            };
            
            try {
                await db.collection('users').doc(user.uid).set(profile);
                finish(user.uid, user.email);
            } catch (error) {
                document.getElementById('status').innerText = "Error: " + error.message;
            }
        }

        function finish(uid, email) {
            document.getElementById('status').innerText = "Success! You can close this window.";
            fetch('/callback?uid=' + uid + '&email=' + email);
        }
    </script>
</body>
</html>
"""

app = Flask(__name__)
auth_data = None

@app.route('/')
def index():
    return render_template_string(LOGIN_HTML)

@app.route('/callback')
def callback():
    global auth_data
    uid = request.args.get('uid')
    email = request.args.get('email')
    if uid and email:
        auth_data = {"uid": uid, "email": email}
        save_auth(auth_data)
        return "Login successful! You can return to your terminal."
    return "Login failed."

def save_auth(data):
    os.makedirs(os.path.dirname(AUTH_FILE), exist_ok=True)
    with open(AUTH_FILE, "w") as f:
        json.dump(data, f)

def get_auth():
    if os.path.exists(AUTH_FILE):
        with open(AUTH_FILE, "r") as f:
            return json.load(f)
    return None

def logout_user():
    if os.path.exists(AUTH_FILE):
        os.remove(AUTH_FILE)

def login_flow():
    global auth_data
    auth_data = None
    
    # Start Flask in a thread
    def run_app():
        app.run(port=5000, debug=False, use_reloader=False)
    
    thread = threading.Thread(target=run_app, daemon=True)
    thread.start()
    
    time.sleep(1)
    webbrowser.open("http://localhost:5000")
    
    print("Waiting for login...")
    while auth_data is None:
        time.sleep(1)
    
    print(f"Logged in as {auth_data['email']}")
    return auth_data
