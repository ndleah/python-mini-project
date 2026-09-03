import os

config = {
    "apiKey": os.environ.get("FIREBASE_APIKEY", "mock-api-key"),
    "authDomain": os.environ.get("FIREBASE_AUTHDOMAIN", "mock-auth-domain"),
    "databaseURL": os.environ.get("FIREBASE_DATABASEURL", "https://mock.firebaseio.com"),
    "projectId": os.environ.get("FIREBASE_PROJECT_ID", "mock-project-id"),
    "storageBucket": os.environ.get("FIREBASE_STORAGE_BUCKET", "mock-storage-bucket"),
    "messagingSenderId": os.environ.get("FIREBASE_MESSAGING_SENDER_ID", "123456789"),
    "appId": os.environ.get("FIREBASE_APP_ID", "mock-app-id")
}

class MockFirebaseAuth:
    """Mock Firebase authentication for environment-independent execution."""
    def __init__(self):
        self.users = {}

    def create_user_with_email_and_password(self, email, password):
        user_id = f"user_{len(self.users) + 1}"
        user_data = {"localId": user_id, "email": email}
        self.users[email] = (password, user_data)
        return user_data

    def sign_in_with_email_and_password(self, email, password):
        if email in self.users and self.users[email][0] == password:
            return self.users[email][1]
        raise Exception("Invalid login credentials")

class MockFirebaseDatabase:
    def child(self, *args): return self
    def get(self): return None
    def push(self, data): return True

try:
    from firebase import Firebase
    firebase = Firebase(config)
    db = firebase.database()
    auth = firebase.auth()
except Exception:
    print("Notice: Firebase / Pyrebase library not configured. Using Mock FirebaseAuth provider.")
    db = MockFirebaseDatabase()
    auth = MockFirebaseAuth()