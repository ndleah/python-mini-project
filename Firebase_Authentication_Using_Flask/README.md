# Firebase Authentication for Flask Application

### Install all the requirements
- Run `pip install -r requirements.txt`

### Firebase Setup for Project

1. Create a [firebase](https://firebase.google.com/) project, set up a web project and get all the `Project Configurations` from `Project Settings`.

2. Navigate to the **Authentication** section in your firebase project and enable the `Email and Password`
 authentication.

3. The `Project Configurations` will look as follows :-
```bash
  "apiKey": YOUR_API_KEY ,
  "authDomain": YOUR_AUTH_DOMAIN,
  "databaseURL": YOUR_DATABASEURL,
  "projectId": YOUR_PROJECT_ID,
  "storageBucket": YOUR_STORAGE_BUCKET,
  "messagingSenderId": YOUR_MESSAGING_SENDER_ID,
  "appId": YOUR_APP_ID,
  "measurementId": YOUR_MEASUREMENT_ID 
```
4. Now create a `.env` file in your project dreictory and include the following parameters as it is :-
```bash
export FIREBASE_APIKEY=YOUR_API_KEY
export FIREBASE_AUTHDOMAIN=YOUR_AUTH_DOMAIN
export FIREBASE_DATABASEURL=YOUR_DATABASEURL
export FIREBASE_PROJECT_ID=YOUR_PROJECT_ID
export FIREBASE_STORAGE_BUCKET=YOUR_STORAGE_BUCKET
export FIREBASE_MESSAGING_SENDER_ID=YOUR_MESSAGING_SENDER_ID
export FIREBASE_APP_ID=YOUR_APP_ID
export FIREBASE_MEASUREMENT_ID=YOUR_MEASUREMENT_ID
``` 

# Now Just, Run the project
- To the run the project, just run the `python run.py` in the terminal.

## Author

[MBSA](https://github.com/MBSA-INFINITY)


