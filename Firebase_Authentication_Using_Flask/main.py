#Importing Flask and other important functions
from flask import Flask, render_template, request, redirect, abort, flash, session ,url_for
#Importing firebase auth from db.py
from db import auth

app = Flask(__name__)
app.secret_key = "MBSAIADITYA"

exempted_endpoints = ['signup','login','static']

'''
Signup Route
''' 
@app.route("/signup", methods = ['GET','POST'])
def signup():
    if request.method=='POST':
        name = request.form.get("name")
        username = request.form.get("email")
        password = request.form.get("password")
        repassword = request.form.get("repassword")
        if password == repassword:
            if len(password)>=6:
                try:
                    #Creating User in firebase using create_user_with_email_and_password method of firebase/auth
                    _user_ = auth.create_user_with_email_and_password(username ,password)
                    flash("User has been created successfully! Please Login")
                    return redirect("/")
                except Exception as e:
                    abort(500, {'message': str(e)})
            else:
                flash('Password is less than 6 characters!')
                return redirect("/signup")
        else:
            flash('Both Passwords do not match!')
            return redirect("/signup")
    return render_template("signup.html")

'''
Login Route
'''  
@app.route("/login",methods = ['GET','POST'] )
def login():
    if request.method == 'POST':
        data = dict(request.form)
        email = data.get("email")
        password = data.get("password")
        try:
            #Signing User in firebase using sign_in_with_email_and_password method of firebase/auth
            user = auth.sign_in_with_email_and_password(email ,password)
            print(user)
            session['user'] = user['localId']
            session['email'] = user['email']
            return redirect("/")     
        except Exception as e:
            abort(500, {'message': str(e)})

    if 'user' in session:
        return redirect("/")
    return render_template("login.html")

'''
Main dashboard route which has to be protected
'''   
@app.route("/",methods = ['GET','POST'])
def start():
    return render_template("index.html", user=session['email'])

'''
Logout Route
'''
@app.route("/logout",methods = ['GET','POST'])
def logout():
    session.pop('user')
    session.pop('email')
    flash("User logged out successfully!")
    return redirect("/")


'''This is an important middleware that run before any request made to flask application and checks
when user is authenticated or not!
'''

@app.before_request
def before_request_func():
    if request.endpoint in exempted_endpoints:
        return 
    if 'user' not in session:
        return redirect(url_for('login'))