import pyrebase

# Config
config = {
  "apiKey": "AIzaSyB33WNvEv9-SBciuOZK2A8ZUbRO14fwc5k",
  "authDomain": "nubes-e8905.firebaseapp.com",
  "databaseURL": "https://nubes-e8905-default-rtdb.firebaseio.com",
  "storageBucket": "nubes-e8905.appspot.com"
}
firebase = pyrebase.initialize_app(config)

# Auth
auth = firebase.auth()
user = auth.sign_in_with_email_and_password('test@mail.com', 'Nubes1234')

# Data base reference
db = firebase.database()


# data to save
data = [
    [1, 2, 3, 4],
    [4, 5, 6, 7],
    [5, 3, 2, 8],
    [8, 3, 6, 9]
]
# Pass the user's idToken to the set method
results = db.child("input").set(data, user['idToken'])


# Data stream
# def stream_handler(message):
#     print(message["event"])
#     print(message["path"])
#     print(message["data"])

# my_stream = db.child("users").stream(stream_handler)

# my_stream.close()