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
        body { font-family: 'Inter', -apple-system, sans-serif; display: flex; justify-content: center; align-items: center; height: 100vh; background: #0a0a0a; color: #e0e0e0; margin: 0; }
        .container { background: #141414; padding: 2.5rem; border-radius: 12px; box-shadow: 0 10px 30px rgba(0,0,0,0.5); width: 420px; text-align: center; border: 1px solid #333; }
        h1 { color: #fbc02d; margin-bottom: 2rem; font-size: 1.8rem; font-weight: 700; letter-spacing: -0.5px; }
        .input-group { text-align: left; margin-bottom: 1rem; }
        label { display: block; margin-bottom: 5px; font-size: 0.9rem; color: #aaa; }
        input, select, textarea { width: 100%; padding: 12px; border-radius: 6px; border: 1px solid #333; background: #1a1a1a; color: white; box-sizing: border-box; font-size: 1rem; transition: border 0.3s; }
        input:focus { border-color: #fbc02d; outline: none; }
        
        .main-btn { background: #fbc02d; color: #000; border: none; padding: 14px; border-radius: 6px; cursor: pointer; font-weight: 600; width: 100%; margin-top: 10px; font-size: 1rem; transition: transform 0.1s, background 0.3s; }
        .main-btn:hover { background: #f9a825; }
        .main-btn:active { transform: scale(0.98); }
        
        .google-btn { background: white; color: rgba(0,0,0,0.54); border: 1px solid #ddd; padding: 10px; border-radius: 6px; cursor: pointer; font-weight: 500; width: 100%; margin-top: 1rem; display: flex; align-items: center; justify-content: center; gap: 10px; font-size: 0.95rem; }
        .google-btn:hover { background: #f5f5f5; }
        
        .divider { display: flex; align-items: center; color: #444; margin: 1.5rem 0; font-size: 0.8rem; }
        .divider::before, .divider::after { content: ""; flex: 1; height: 1px; background: #333; margin: 0 10px; }
        
        .secondary-links { margin-top: 1.5rem; font-size: 0.85rem; color: #888; }
        .secondary-links a { color: #fbc02d; text-decoration: none; cursor: pointer; }
        .secondary-links a:hover { text-decoration: underline; }
        
        #status { margin-top: 1.5rem; font-size: 0.9rem; padding: 10px; border-radius: 4px; }
        .error { color: #ff5252; background: rgba(255, 82, 82, 0.1); }
        .success { color: #4caf50; background: rgba(76, 175, 80, 0.1); }
        
        .hidden { display: none; }
    </style>
</head>
<body>
    <div class="container">
        <h1>XDT Labs clipSync</h1>
        
        <div id="auth-section">
            <div id="login-view">
                <div class="input-group">
                    <label>Email Address</label>
                    <input type="email" id="email" placeholder="name@example.com">
                </div>
                <div class="input-group">
                    <label>Password</label>
                    <input type="password" id="password" placeholder="••••••••">
                </div>
                <button class="main-btn" onclick="login()">Sign In</button>
                
                <div class="secondary-links">
                    <a onclick="forgotPassword()">Forgot Password?</a><br><br>
                    Don't have an account? <a onclick="toggleAuthView(false)">Create one</a>
                </div>
            </div>

            <div id="signup-view" class="hidden">
                <div class="input-group">
                    <label>Email Address</label>
                    <input type="email" id="signup-email" placeholder="name@example.com">
                </div>
                <div class="input-group">
                    <label>Password</label>
                    <input type="password" id="signup-password" placeholder="Min 6 characters">
                </div>
                <button class="main-btn" onclick="signup()">Create Account</button>
                <div class="secondary-links">
                    Already have an account? <a onclick="toggleAuthView(true)">Sign In</a>
                </div>
            </div>

            <div class="divider">OR</div>
            
            <button class="google-btn" onclick="googleSignIn()">
                <img src="https://www.gstatic.com/firebasejs/ui/2.0.0/images/auth/google.svg" width="18" height="18">
                Continue with Google
            </button>
        </div>

        <div id="profile-section" class="hidden">
            <h3>Complete Your Profile</h3>
            <div class="input-group">
                <label>Full Name</label>
                <input type="text" id="name" placeholder="John Doe">
            </div>
            <div class="input-group">
                <label>Mobile Number</label>
                <input type="text" id="mobile" placeholder="+1 ...">
            </div>
            <div class="input-group">
                <label>Profession</label>
                <input type="text" id="profession" placeholder="Developer / Designer">
            </div>
            <div class="input-group">
                <label>Why are you using clipSync?</label>
                <textarea id="reason" rows="3" placeholder="Sync code snippets between laptop and PC..."></textarea>
            </div>
            <button class="main-btn" onclick="saveProfile()">Start Syncing</button>
        </div>

        <div id="device-section" class="hidden">
            <h3>Name This Device</h3>
            <p style="font-size: 0.9rem; color: #888; margin-bottom: 1.5rem;">Give this device a unique name to identify it across your synced devices.</p>
            <div class="input-group">
                <label>Device Name</label>
                <input type="text" id="device-name" placeholder="MacBook Pro / Work PC / Home Laptop">
            </div>
            <button class="main-btn" onclick="saveDeviceName()">Complete Setup</button>
        </div>
        
        <div id="status" class="hidden"></div>
    </div>

    <script>
        const firebaseConfig = """ + json.dumps(FIREBASE_CONFIG) + """;
        firebase.initializeApp(firebaseConfig);
        const auth = firebase.auth();
        const db = firebase.firestore();

        function showStatus(msg, type) {
            const status = document.getElementById('status');
            status.innerText = msg;
            status.className = type;
            status.classList.remove('hidden');
        }

        function toggleAuthView(isLogin) {
            document.getElementById('login-view').classList.toggle('hidden', !isLogin);
            document.getElementById('signup-view').classList.toggle('hidden', isLogin);
        }

        async function login() {
            const email = document.getElementById('email').value;
            const password = document.getElementById('password').value;
            showStatus("Authenticating...", "success");
            
            try {
                const userCredential = await auth.signInWithEmailAndPassword(email, password);
                handleAuthSuccess(userCredential.user);
            } catch (error) {
                showStatus(error.message, "error");
            }
        }

        async function signup() {
            const email = document.getElementById('signup-email').value;
            const password = document.getElementById('signup-password').value;
            showStatus("Creating account...", "success");
            
            try {
                const userCredential = await auth.createUserWithEmailAndPassword(email, password);
                handleAuthSuccess(userCredential.user);
            } catch (error) {
                showStatus(error.message, "error");
            }
        }

        async function googleSignIn() {
            const provider = new firebase.auth.GoogleAuthProvider();
            try {
                const result = await auth.signInWithPopup(provider);
                handleAuthSuccess(result.user);
            } catch (error) {
                showStatus(error.message, "error");
            }
        }

        async function forgotPassword() {
            const email = document.getElementById('email').value;
            if (!email) {
                showStatus("Please enter your email above first.", "error");
                return;
            }
            try {
                await auth.sendPasswordResetEmail(email);
                showStatus("Reset link sent to your email.", "success");
            } catch (error) {
                showStatus(error.message, "error");
            }
        }

        async function handleAuthSuccess(user) {
            const token = await user.getIdToken();
            window.currentUser = user;
            window.currentToken = token;
            // Capture refresh token
            window.refreshToken = user.refreshToken;
            
            try {
                const userDoc = await db.collection('users').doc(user.uid).get();
                if (userDoc.exists) {
                    // Existing user - skip to device naming
                    document.getElementById('auth-section').classList.add('hidden');
                    document.getElementById('device-section').classList.remove('hidden');
                    document.getElementById('status').classList.add('hidden');
                } else {
                    // New user - show profile form first
                    document.getElementById('auth-section').classList.add('hidden');
                    document.getElementById('profile-section').classList.remove('hidden');
                    document.getElementById('status').classList.add('hidden');
                }
            } catch (error) {
                console.error("Firestore Access Error:", error);
                document.getElementById('auth-section').classList.add('hidden');
                document.getElementById('profile-section').classList.remove('hidden');
                showStatus("Authentication successful. Please complete your profile.", "success");
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
                // After profile, ask for device name
                document.getElementById('profile-section').classList.add('hidden');
                document.getElementById('device-section').classList.remove('hidden');
                document.getElementById('status').classList.add('hidden');
            } catch (error) {
                showStatus("Error saving profile: " + error.message + ". Check Firestore rules.", "error");
            }
        }

        async function saveDeviceName() {
            const user = auth.currentUser;
            const deviceName = document.getElementById('device-name').value.trim();
            
            if (!deviceName) {
                showStatus("Please enter a device name.", "error");
                return;
            }

            try {
                // Check if device name already exists for this user
                const userDoc = await db.collection('users').doc(user.uid).get();
                const userData = userDoc.data();
                const devices = userData.devices || {};
                
                // Check for duplicate device names
                const existingNames = Object.values(devices).map(d => d.name.toLowerCase());
                if (existingNames.includes(deviceName.toLowerCase())) {
                    showStatus("This device name already exists. Please choose a different name.", "error");
                    return;
                }

                // Generate a unique device ID
                const deviceId = 'device_' + Date.now() + '_' + Math.random().toString(36).substr(2, 9);
                
                // Update user document with device info
                await db.collection('users').doc(user.uid).update({
                    [`devices.${deviceId}`]: {
                        name: deviceName,
                        addedAt: firebase.firestore.FieldValue.serverTimestamp(),
                        lastActive: firebase.firestore.FieldValue.serverTimestamp()
                    }
                });

                const token = await user.getIdToken();
                // Pass refresh token to finish
                finish(user.uid, user.email, token, deviceId, deviceName, user.refreshToken);
            } catch (error) {
                showStatus("Error saving device: " + error.message, "error");
            }
        }

        function finish(uid, email, token, deviceId, deviceName, refreshToken) {
            showStatus("Success! Authenticated as " + email + ". You can close this window.", "success");
            const params = new URLSearchParams({
                uid: uid,
                email: email,
                token: token,
                deviceId: deviceId || '',
                deviceName: deviceName || '',
                refreshToken: refreshToken || ''
            });
            fetch('/callback?' + params.toString());
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
    import uuid
    
    uid = request.args.get('uid')
    email = request.args.get('email')
    token = request.args.get('token')
    device_id = request.args.get('deviceId')
    device_name = request.args.get('deviceName')
    refresh_token = request.args.get('refreshToken')
    
    if uid and email and token:
        # Generate device_id if not provided
        if not device_id:
            device_id = f"device_{int(time.time())}_{uuid.uuid4().hex[:9]}"
        
        # Use email username as default device name
        if not device_name:
            device_name = email.split('@')[0]
        
        auth_data = {
            "uid": uid, 
            "email": email, 
            "token": token,
            "refresh_token": refresh_token or "",
            "device_id": device_id,
            "device_name": device_name
        }
        save_auth(auth_data)
        return "Login successful! You can return to your terminal."
    return "Login failed."

def save_auth(data):
    auth_dir = os.path.dirname(AUTH_FILE)
    os.makedirs(auth_dir, exist_ok=True)
    # Set directory permissions to 700 (owner only)
    os.chmod(auth_dir, 0o700)
    
    with open(AUTH_FILE, "w") as f:
        json.dump(data, f)
    
    # Set file permissions to 600 (owner read/write only)
    os.chmod(AUTH_FILE, 0o600)

def get_auth():
    if os.path.exists(AUTH_FILE):
        with open(AUTH_FILE, "r") as f:
            return json.load(f)
    return None

def logout_user():
    if os.path.exists(AUTH_FILE):
        os.remove(AUTH_FILE)

def rename_device(new_name):
    """Rename the current device (updates locally, takes effect on next sync)"""
    import uuid
    
    auth = get_auth()
    if not auth:
        return False
    
    # Generate device_id if missing
    if not auth.get("device_id"):
        auth["device_id"] = f"device_{int(time.time())}_{uuid.uuid4().hex[:9]}"
    
    auth["device_name"] = new_name
    save_auth(auth)
    return True

def login_flow():
    global auth_data
    auth_data = None
    
    # Suppress Flask request logs
    import logging
    log = logging.getLogger('werkzeug')
    log.setLevel(logging.ERROR)
    
    # Start Flask in a thread
    def run_app():
        app.run(port=5005, debug=False, use_reloader=False)
    
    thread = threading.Thread(target=run_app, daemon=True)
    thread.start()
    
    time.sleep(1)
    webbrowser.open("http://localhost:5005")
    
    print("Waiting for login... (a browser window will open)")
    while auth_data is None:
        time.sleep(1)
    
    # Friendly welcome message
    name = auth_data.get('device_name') or auth_data['email'].split('@')[0]
    print(f"\n✨ Welcome, {name}!")
    print(f"📧 Logged in as {auth_data['email']}")
    if auth_data.get('device_name'):
        print(f"💻 Device: {auth_data['device_name']}")
    print("\nRun 'csync serve' to start syncing your clipboard!\n")
    return auth_data
