import time
import uuid
import threading
import pyperclip
from .api import update_remote_clipboard, check_version, FUNCTIONS_BASE_URL
from .auth import get_auth
import requests
import json

DEVICE_ID = str(uuid.uuid4())
CHECK_INTERVAL = 1.0

stop_event = threading.Event()

def monitor_local_clipboard():
    """Monitor local clipboard and sync to remote"""
    last_clipboard_text = pyperclip.paste()
    
    while not stop_event.is_set():
        try:
            current_text = pyperclip.paste()
            if current_text != last_clipboard_text:
                if update_remote_clipboard(current_text, DEVICE_ID):
                    last_clipboard_text = current_text
        except Exception as e:
            pass
        time.sleep(CHECK_INTERVAL)

def listen_to_remote_changes():
    """Poll for remote changes (SSE implementation simplified or polling)"""
    auth = get_auth()
    if not auth:
        return

    last_synced_text = ""
    uid = auth["uid"]
    
    # We poll a function that returns the current clipboard for the user
    while not stop_event.is_set():
        try:
            # We can use a special function for this or just the update one?
            # Let's assume a getClipboard function
            response = requests.get(f"{FUNCTIONS_BASE_URL}/getClipboard", params={"uid": uid})
            if response.status_code == 200:
                data = response.json()
                text = data.get("text", "")
                remote_device_id = data.get("device_id", "")
                
                if remote_device_id != DEVICE_ID and text != last_synced_text:
                    pyperclip.copy(text)
                    last_synced_text = text
        except:
            pass
        time.sleep(CHECK_INTERVAL)

def start_service():
    """Start both local monitor and remote listener"""
    if not check_version():
        print("Error: Version mismatch. Please update csync.")
        return

    stop_event.clear()
    
    local_thread = threading.Thread(target=monitor_local_clipboard, daemon=True)
    remote_thread = threading.Thread(target=listen_to_remote_changes, daemon=True)
    
    local_thread.start()
    remote_thread.start()
    
    print("clipSync service is running in background. Press Ctrl+C to stop in this window (if not detached).")
    try:
        while not stop_event.is_set():
            time.sleep(1)
    except KeyboardInterrupt:
        stop_service()

def stop_service():
    stop_event.set()
    print("clipSync service stopped.")
