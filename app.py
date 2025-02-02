from flask import Flask
from flask import render_template, redirect, request, url_for, session
import sqlite3
import os
from datetime import timedelta
import datetime
import json

subjects = ["Algebra", "Calculus", "Geometry", "Physics", "Chemistry", "Engineering", "Biology", "Coding", "English", "History", "Geography", "French", "Spanish", "Chinese", "Latin", "Medicine"]

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
        
        id = cur.execute("SELECT seq FROM sqlite_sequence")

        session["username"] = username
        session["id"] = list(id)[0][0]
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

        id = cur.execute("SELECT seq FROM sqlite_sequence")

        session["username"] = username
        session["id"] = list(id)[0][0]

        return redirect(url_for('setup_user'))

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
    session.pop('id')
    return redirect(url_for('homepage'))

@app.route('/retrieve/<id>')
def retrieve(id):
    info = cur.execute("SELECT * FROM Users WHERE id = %d" % id)
    return render_template('extract_from_db.html', info=list(info)[0])

@app.route('/setup', methods = ['GET', 'POST'])
@app.route('/setup/<error>')
def setup_user(error = None):
    error_translate = {
        "DuplicateError" : "Interests must be unique",
    }

    if request.method == 'POST':
        first_interest = request.form.get('first_interest')
        second_interest = request.form.get('second_interest')
        third_interest = request.form.get('third_interest')
        aboutme = request.form.get('aboutme')

        if first_interest == second_interest or second_interest == third_interest or first_interest == third_interest:
            return redirect("setup/DuplicateError")

        weights = {}
        base_amt = 1 / (len(subjects) + 6)

        for s in subjects:
            weights[s] = base_amt

        weights[first_interest] += 3 * base_amt
        weights[second_interest] += 2 * base_amt
        weights[third_interest] += 1 * base_amt

        user = {"username" : session["username"], "weights" : weights}
        user_string = json.dumps(user)

        cur.execute("INSERT INTO user_info (id, interests, aboutme) VALUES (?, ?, ?)", (session["id"], user_string, aboutme))
        con.commit()

        return(redirect(url_for("homepage")))

    if request.method == 'GET':
        if error:
            return(render_template('user_setup.html', error=error_translate[error], subjects=subjects))
        return(render_template('user_setup.html', subjects=subjects))

@app.route('/profile')
def profile():
    info = list(cur.execute("SELECT interests FROM user_info WHERE id = ?", (session["id"], )))
    loaded_info = dict(json.loads(info[0][0]))
    loaded_info["keys"] = list(loaded_info["weights"].keys())

    aboutme = list(cur.execute("SELECT aboutme FROM user_info WHERE id = ?", (session["id"], )))[0][0]

    return(render_template("profile.html", info=loaded_info, aboutme=aboutme))

@app.route('/compose', methods = ["GET", "POST"])
def compose():
    if request.method == "POST" and request.form.get("title"):
        id = session.get("id")
        username = session.get("username")
        title = request.form.get("title")
        content = request.form.get("content")
        subject_areas = (request.form.get("first_interest"), request.form.get("second_interest"), request.form.get("third_interest"))
        tunings = (float(request.form.get("first_tuning")), float(request.form.get("second_tuning")), float(request.form.get("third_tuning")))

        weights = {subject_areas[0] : tunings[0], subject_areas[1] : tunings[1], subject_areas[2] : tunings[2]}

        weights_string = json.dumps(weights)

        cur.execute("INSERT INTO posts (poster_id, title, content, timestamp, weights) VALUES (?, ?, ?, ?, ?)", (id, title, content, str(datetime.datetime.now()), weights_string))
        con.commit()

        return redirect(url_for("view_all_posts"))

    else:
        return render_template("compose.html", subjects=subjects)
    
@app.route("/updatebio", methods = ["POST"])
def update_about_me():
    if request.method == "POST":
        cur.execute("UPDATE user_info SET aboutme = ? WHERE id = ?", (request.form.get("newbio"), session["id"]))
        con.commit()
        return(redirect(url_for('profile')))
    
@app.route("/posts")
def view_all_posts():
    posts = list(cur.execute("SELECT * FROM posts"))

    fixed_data = []

    for p in posts:
        p = list(p)
        p[5] = json.loads(p[5])

        temp = p
        temp.append(list(cur.execute("SELECT username FROM users WHERE id = ?", (p[1],)))[0][0])

        fixed_data.append(temp)

    print(fixed_data)

    return render_template("posts.html", posts=fixed_data)

@app.route("/post/<id>", methods = ["GET", "POST"])
def view_post(id):
    poster_id, title, content = list(cur.execute("SELECT poster_id, title, content FROM posts WHERE message_id = ?", (id,)))[0]
    return(render_template("viewpost.html", title=title, content=content, username=list(cur.execute("SELECT username FROM users WHERE id = ?", (poster_id,)))[0][0]))

if __name__ == '__main__':
   app.run()