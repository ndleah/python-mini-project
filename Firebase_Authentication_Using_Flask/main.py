from flask import Flask, render_template, request, redirect, abort, flash, session, url_for
from db import auth

app = Flask(__name__)
app.secret_key = "somesecretkey"

exempted_endpoints = ['signup', 'login', 'static']

@app.route("/signup", methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        name = request.form.get("name")
        username = request.form.get("email")
        password = request.form.get("password")
        repassword = request.form.get("repassword")
        if password == repassword:
            if len(password) >= 6:
                try:
                    _user_ = auth.create_user_with_email_and_password(username, password)
                    flash("User has been created successfully! Please Login")
                    return redirect(url_for("login"))
                except Exception as e:
                    abort(500, {'message': str(e)})
            else:
                flash('Password must be at least 6 characters long!')
                return redirect(url_for("signup"))
        else:
            flash('Both Passwords do not match!')
            return redirect(url_for("signup"))
    return render_template("signup.html")

@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        data = dict(request.form)
        email = data.get("email")
        password = data.get("password")
        try:
            user = auth.sign_in_with_email_and_password(email, password)
            session['user'] = user['localId']
            session['email'] = user['email']
            return redirect(url_for("start"))
        except Exception as e:
            abort(500, {'message': str(e)})

    if 'user' in session:
        return redirect(url_for("start"))
    return render_template("login.html")

@app.route("/", methods=['GET', 'POST'])
def start():
    user_email = session.get('email', 'Guest')
    return render_template("index.html", user=user_email)

@app.route("/logout", methods=['GET', 'POST'])
def logout():
    session.pop('user', None)
    session.pop('email', None)
    flash("User logged out successfully!")
    return redirect(url_for("login"))

@app.before_request
def before_request_func():
    if request.endpoint in exempted_endpoints:
        return
    if 'user' not in session:
        return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)