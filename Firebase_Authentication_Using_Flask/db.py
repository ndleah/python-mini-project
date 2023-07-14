#Importing Firebase
from firebase import Firebase
import os

#Intializing Firebase Configuration from the Environment Variables
config = {
  "apiKey": os.environ.get("FIREBASE_APIKEY"),
  "authDomain": os.environ.get("FIREBASE_AUTHDOMAIN"),
  "databaseURL": os.environ.get("FIREBASE_DATABASEURL"),
  "projectId": os.environ.get("FIREBASE_PROJECT_ID"),
  "storageBucket": os.environ.get("FIREBASE_STORAGE_BUCKET"),
  "messagingSenderId": os.environ.get("FIREBASE_MESSAGING_SENDER_ID"),
  "appId": os.environ.get("FIREBASE_APP_ID"),
  "measurementId": os.environ.get("FIREBASE_MEASUREMENT_ID")
  }

#Intializing Firebase Object
firebase = Firebase(config)

#Intializing Firebase Databse
db = firebase.database()

#Intializing Firebase Auth
auth = firebase.auth()