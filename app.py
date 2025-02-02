from flask import Flask
from flask import render_template, redirect, request, url_for, session
import sqlite3
import os
from datetime import timedelta

#creates a connection to the database
con = sqlite3.connect("oblock.db", check_same_thread=False)
cur = con.cursor()

app = Flask(__name__)
app.permanent_session_lifetime = timedelta(weeks=2)
app.secret_key = "whyisthisathing"

@app.route('/')
def homepage():
    return render_template('homepage.html', session=session)

@app.route('/login/<error>')
@app.route('/login', methods=['GET', 'POST'])
def login(error = None):
    error_translate = {
        "PasswordError" : "Incorrect password!",
        "InvalidUserError" : "Invalid username!",
        "BlankError" : "Please enter a username or password",
    }

    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        if not username or not password:
            return redirect("login/BlankError")
    
        users = list(cur.execute("SELECT * FROM Users WHERE username =?", (username,)))

        if len(users) != 1:
            return(redirect("login/InvalidUserError"))
        
        if hash(password) != hash(users[0][2]):
            return redirect(f"login/PasswordError")
        
        session["username"] = username
        return redirect(url_for('homepage'))
    
    if request.method == "GET":
        if error:
            return render_template("login.html", error=error_translate[error])
        return render_template("login.html")

@app.route('/register/<error>', methods=["GET"])
@app.route('/register', methods = ["GET", "POST"])
def register(error = None):
    error_translate = {
        "PasswordError" : "Passwords must match!",
        "DuplicateUsernameError" : "Sorry, username already in use!",
        "BlankError" : "Please enter a username or password",
    }

    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")
        account_type = request.form.get("account_type")
        
        if not username or not password:
            return redirect("register/BlankError")
        
        users = list(cur.execute("SELECT * FROM Users WHERE username = ?", (username,)))

        if len(users) > 1:
            return redirect("register/DuplicateUsernameError")
        
        if password != confirmation:
            return redirect("register/PasswordError")
        
        #cur.execute("INSERT INTO Users (username, password, account_type) VALUES (?,?,?)", (username, hash(password), account_type))
        cur.execute("INSERT INTO Users (username, password, account_type) VALUES (?,?,?)", (username, password, account_type))

        con.commit()
        session["username"] = username

        return redirect(url_for('homepage'))

    if request.method == "GET":
        if error:
            return render_template('register.html', error=error_translate[error])
        return render_template('register.html')

@app.route('/search')
def search():
    # TODO
    pass

@app.route('/logout')
def logout():
    session.pop('username')
    return redirect(url_for('homepage'))

@app.route('/retrieve/<id>')
def retrieve(id):
    info = cur.execute("SELECT * FROM Users WHERE id = %d" % id)
    print(info, type(info))
    return render_template('extract_from_db.html', info=list(info)[0])

if __name__ == '__main__':
   app.run()