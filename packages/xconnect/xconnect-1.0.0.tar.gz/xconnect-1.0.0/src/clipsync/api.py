import requests
from .auth import get_auth

# Replace with your actual Cloud Function URLs after deployment
FUNCTIONS_BASE_URL = "https://us-central1-do-so-fffm46.cloudfunctions.net"

APP_VERSION = "1.0.0"

def check_version():
    """Checks the system version and kill switch. Returns (allowed, message)"""
    try:
        response = requests.get(f"{FUNCTIONS_BASE_URL}/checkVersion", params={"version": APP_VERSION})
        if response.status_code == 200:
            data = response.json()
            allowed = data.get("allowed", True)
            message = data.get("message", "")
            return allowed, message
        return True, ""  # Default to allowed if function not responding
    except:
        return True, ""  # Default to allowed on error

def update_remote_clipboard(text, device_id, device_name):
    """Securely updates the clipboard via Firebase Function"""
    auth = get_auth()
    if not auth or "token" not in auth:
        return False
    
    headers = {"Authorization": f"Bearer {auth['token']}"}
    payload = {
        "text": text,
        "device_id": device_id,
        "device_name": device_name
    }
    try:
        response = requests.post(f"{FUNCTIONS_BASE_URL}/updateClipboard", json=payload, headers=headers)
        if response.status_code != 200:
            print(f"API Error: {response.status_code} - {response.text}")
        return response.status_code == 200
    except Exception as e:
        print(f"API Exception: {e}")
        return False

def listen_to_remote_clipboard(callback):
    """
    Since we are using Functions, real-time sync is best done via 
    Firestore snapshot listener or a polling mechanism if using only Functions.
    However, the user wants immediate sync. 
    Using the Firebase Admin SDK locally with user UID filtering is easiest.
    """
    # Placeholder for the listener logic
    pass
