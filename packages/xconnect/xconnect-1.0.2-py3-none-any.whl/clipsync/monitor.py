import time
import uuid
import threading
import pyperclip
from .api import update_remote_clipboard, check_version, FUNCTIONS_BASE_URL
from .auth import get_auth
import requests
import json

CHECK_INTERVAL = 1.0

stop_event = threading.Event()

def monitor_local_clipboard():
    """Monitor local clipboard and sync to remote"""
    auth = get_auth()
    if not auth:
        return
    
    device_id = auth.get("device_id") or str(uuid.uuid4())
    device_name = auth.get("device_name") or "Unknown Device"
    last_clipboard_text = pyperclip.paste()
    print(f"📋 Monitoring clipboard on '{device_name}'...")
    
    while not stop_event.is_set():
        try:
            current_text = pyperclip.paste()
            if current_text != last_clipboard_text:
                preview = current_text[:50] + "..." if len(current_text) > 50 else current_text
                preview = preview.replace('\n', ' ')
                print(f"\n📤 [{device_name}] Syncing: \"{preview}\"")
                if update_remote_clipboard(current_text, device_id, device_name):
                    print(f"✅ Synced successfully!")
                    last_clipboard_text = current_text
                else:
                    print("❌ Sync failed.")
        except Exception as e:
            print(f"❌ Error: {e}")
        time.sleep(CHECK_INTERVAL)

def listen_to_remote_changes():
    """Poll for remote changes"""
    auth = get_auth()
    if not auth:
        return

    device_id = auth.get("device_id") or str(uuid.uuid4())
    device_name = auth.get("device_name") or "Unknown"
    last_synced_text = ""
    
    print(f"👂 Listening for remote changes...")
    
    while not stop_event.is_set():
        try:
            headers = {"Authorization": f"Bearer {auth['token']}"}
            response = requests.get(f"{FUNCTIONS_BASE_URL}/getClipboard", headers=headers)
            if response.status_code == 200:
                data = response.json()
                text = data.get("text", "")
                remote_device_id = data.get("device_id", "")
                remote_device_name = data.get("device_name", "Unknown")
                
                # Only paste if from a different device and text is new
                if remote_device_id != device_id and text and text != last_synced_text:
                    pyperclip.copy(text)
                    last_synced_text = text
                    preview = text[:50] + "..." if len(text) > 50 else text
                    preview = preview.replace('\n', ' ')
                    print(f"\n📥 [{remote_device_name}] Received: \"{preview}\"")
                    print(f"✅ Pasted to clipboard!")
            elif response.status_code == 403 or response.status_code == 401:
                print("⚠️  Token expired. Refreshing...")
                from .api import refresh_id_token
                if refresh_id_token():
                    # Reload auth to get new token for next loop
                    auth = get_auth()
                    continue # Retry immediately
                else:
                    print("❌ Session expired. Please run 'csync logout' then 'csync login'.")
                    break
        except Exception as e:
            print(f"❌ Remote sync error: {e}")
        time.sleep(CHECK_INTERVAL)

def start_service():
    """Start both local monitor and remote listener"""
    auth = get_auth()
    if not auth:
        print("Error: Not logged in. Please run 'csync login' first.")
        return
    
    allowed, message = check_version()
    if not allowed:
        print(f"Error: {message}")
        return

    stop_event.clear()
    
    local_thread = threading.Thread(target=monitor_local_clipboard, daemon=True)
    remote_thread = threading.Thread(target=listen_to_remote_changes, daemon=True)
    
    local_thread.start()
    remote_thread.start()
    
    device_name = auth.get("device_name") or "Unknown Device"
    print(f"clipSync service is running on: {device_name}")
    print("Press Ctrl+C to stop.")
    try:
        while not stop_event.is_set():
            time.sleep(1)
    except KeyboardInterrupt:
        stop_service()

def stop_service():
    stop_event.set()
    print("clipSync service stopped.")
