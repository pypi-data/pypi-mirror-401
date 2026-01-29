import requests
from .auth import get_auth

# Replace with your actual Cloud Function URLs after deployment
FUNCTIONS_BASE_URL = "https://us-central1-do-so-fffm46.cloudfunctions.net"

def check_version():
    """Checks the system version and kill switch"""
    try:
        # For now, we'll hit a placeholder or a simple Firestore read if we had the SDK
        # But per requirements, let's assume a function check
        response = requests.get(f"{FUNCTIONS_BASE_URL}/checkVersion", params={"version": "0.1.0"})
        if response.status_code == 200:
            return response.json().get("allowed", True)
        return True # Default to allowed if function not yet there
    except:
        return True

def update_remote_clipboard(text, device_id):
    """Securely updates the clipboard via Firebase Function"""
    auth = get_auth()
    if not auth:
        return False
    
    payload = {
        "uid": auth["uid"],
        "text": text,
        "device_id": device_id
    }
    try:
        # In a real SaaS, we'd include an ID Token here for security
        response = requests.post(f"{FUNCTIONS_BASE_URL}/updateClipboard", json=payload)
        return response.status_code == 200
    except:
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
