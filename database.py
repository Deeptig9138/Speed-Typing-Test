import firebase_admin
from firebase_admin import credentials, db
import os
import json
from datetime import datetime

# Read Firebase credentials from an environment variable
firebase_credentials = os.getenv("FIREBASE_CREDENTIALS")

if firebase_credentials:
    firebase_credentials = json.loads(firebase_credentials)
    cred = credentials.Certificate(firebase_credentials)
    firebase_admin.initialize_app(cred, {
        'databaseURL': "https://speed-typing-test-shashi-singh-default-rtdb.firebaseio.com/"
    })
else:
    raise ValueError("Firebase credentials not found. Set the FIREBASE_CREDENTIALS environment variable.")

# Get reference to the Firebase Realtime Database
ref = db.reference("test")

def checkUniqueUser(username):
    """Check if a user exists in the database."""
    data = ref.get()  # Fetch fresh data every time
    if data:
        for key, value in data.items():
            if isinstance(value, dict):  # Ensure it's a dictionary before iterating
                for names, entry in value.items():
                    if entry == username:
                        return True
    return False

def initialiseNewUser(username, password):
    """Add a new user to the database."""
    new_value = {
        "name": username,
        "password": password
    }
    ref.child(username).set(new_value)  # Use `set()` instead of `update()` to avoid partial overwrites

def uploadCurrentData(username, wpm, accuracy):
    """Upload user WPM and accuracy data with a timestamp."""
    current_datetime = datetime.now()
    formatted_datetime = current_datetime.strftime("%Y-%m-%d %H:%M:%S")

    new_value = {
        "wpm": wpm,
        "accuracy": accuracy,
    }
    
    try:
        if username and username != "Login":
            ref.child(username).child("history").child(formatted_datetime).set(new_value)
    except firebase_admin.exceptions.FirebaseError as e:
        print(f"Failed to upload data: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")

def getHistory(username):
    """Retrieve the user's typing history."""
    new_data = ref.child(username).child("history").get()
    if not new_data:
        return []

    output_list = []
    
    for timestamp, values in new_data.items():
        try:
            datetime_obj = datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S")
            real_date = datetime_obj.date()
            real_time = datetime_obj.time()

            entry = {
                "date": real_date,
                "time": real_time,
                "wpm": values.get("wpm", 0),
                "accuracy": values.get("accuracy", 0),
            }
            output_list.append(entry)
        except ValueError:
            print(f"Skipping invalid timestamp: {timestamp}")

    return output_list



# def checking(username):
#     newData = ref.child(username).child("history").get()
#     count = len(newData)
#     print(count)

# getHistory("shashi")