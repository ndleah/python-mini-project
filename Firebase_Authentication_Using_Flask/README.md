<!--Please do not remove this part-->
![Star Badge](https://img.shields.io/static/v1?label=%F0%9F%8C%9F&message=If%20Useful&style=style=flat&color=BC4E99)
![Open Source Love](https://badges.frapsoft.com/os/v1/open-source.svg?v=103)

# Firebase Authentication for Flask Application

## 🛠️ Description
This project enables developers to implement secure user authentication features in their Flask applications with ease using Firebase Authentication which offers various authentication methods, including email/password, social media login (such as Google, Facebook, Twitter), and more. It handles the entire authentication process, including user registration, login, and password reset, taking care of security best practices like password hashing and token-based authentication.

## ⚙️ Languages or Frameworks Used
 - Flask, Firebase
 - HTML, CSS, Bootstrap


## 🌟 How to run
 - ### Install all the requirements
    Run `pip install -r requirements.txt` to install all the requirements.
 - ### Firebase Setup for Project

   - Create a [firebase](https://firebase.google.com/) project, set up a web project and get all the `Project Configurations` from `Project Settings`.

   - Navigate to the **Authentication** section in your firebase project and enable the `Email and Password`
 authentication.

   - The `Project Configurations` will look as follows :-
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
- ### Setup Environment for the project
   - Now create a `.env` file in your project dreictory and include the following parameters as it is :-
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

- ###  Now Just, Run the project
  - To the run the project, go to the `bash` terminal of VSCode or any other code editor and run `./start_server.sh`.
  - You don't have to care about setting `.env` then yourself then.


## 📺 Demo
![image](https://github.com/MBSA-INFINITY/MBSA-Forms/assets/85332648/2200ef81-57de-4619-ba33-4bed2cf31780)
![image](https://github.com/MBSA-INFINITY/MBSA-Forms/assets/85332648/ad83c91d-e140-4f4b-9b30-81b4903f1011)

## 🤖 Author

Github - [MBSA-INFINITY](https://github.com/MBSA-INFINITY)
LinkedIn - [MBSAIADITYA](https://www.linkedin.com/in/mbsaiaditya/)
Portfolio - [MBSA](https://mbsaiaditya.in/)




