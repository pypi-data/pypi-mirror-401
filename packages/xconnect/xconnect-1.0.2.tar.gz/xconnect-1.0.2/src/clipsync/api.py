import requests
from .auth import get_auth

# Replace with your actual Cloud Function URLs after deployment
FUNCTIONS_BASE_URL = "https://us-central1-do-so-fffm46.cloudfunctions.net"

APP_VERSION = "1.0.2"

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

def update_remote_clipboard(text, device_id, device_name, retry=True):
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
        
        # If unauthorized, try to refresh token and retry ONE time
        if (response.status_code == 401 or response.status_code == 403) and retry:
            print("⚠️ Token expired. Refreshing...")
            if refresh_id_token():
                return update_remote_clipboard(text, device_id, device_name, retry=False)
        
        if response.status_code != 200:
            print(f"API Error: {response.status_code} - {response.text}")
        return response.status_code == 200
    except Exception as e:
        print(f"API Exception: {e}")
        return False

def refresh_id_token():
    """Refreshes the Firebase ID token using the refresh token"""
    from .auth import save_auth, get_auth
    
    auth = get_auth()
    if not auth or "refresh_token" not in auth:
        return False
        
    refresh_token = auth["refresh_token"]
    api_key = "AIzaSyCCxDr_YYWPtx2TMAe-Ba5rZNzm_dqL_98" # From auth.py
    
    url = f"https://securetoken.googleapis.com/v1/token?key={api_key}"
    payload = {
        "grant_type": "refresh_token",
        "refresh_token": refresh_token
    }
    
    try:
        response = requests.post(url, data=payload)
        if response.status_code == 200:
            data = response.json()
            new_token = data["id_token"]
            new_refresh_token = data["refresh_token"]
            
            # Update local auth
            auth["token"] = new_token
            auth["refresh_token"] = new_refresh_token
            save_auth(auth)
            print("🔄 Session refreshed successfully.")
            return True
        else:
            print(f"Failed to refresh token: {response.text}")
            return False
    except Exception as e:
        print(f"Error refreshing token: {e}")
        return False
