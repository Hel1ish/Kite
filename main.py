# <main.py> <Kite Source Code, Developer: Govany Hanna>
# <Imports>
from flask import Flask, render_template, url_for, request, session, redirect, flash
from pymongo import MongoClient
from flaskwebgui import FlaskUI
import ctypes
from functions import retrieve
import os.path
import json
import random
import bcrypt
import secrets
from datetime import datetime
get = retrieve.GET()
time = datetime.now()
# <Definding app and variables>
app = Flask(__name__)
app.secret_key = "0c28fccd52814500a44013dd0e6a47b3"
client = MongoClient('mongodb+srv://Xynx_Dev:rabMue6xhQJH7gNR@kite-cluster.ie2xvdk.mongodb.net/?retryWrites=true&w=majority')
mong = client.get_database('Data')
database = mong.UserData
debug = False
# Main function ---> Panel Handler

@app.route("/panel", methods=["POST", "GET"])
def panel():
  if "token" in session:
    token = database.find_one({"token": session["token"]})
    if token:
      if request.method == "POST":
            user = token["_id"]
            amount = request.form.get("amount")
            data = get.data(user)
            message = get.addbal(amount, user)
            return redirect(request.path,code=302)
      else:
        data = get.data(token["_id"])
        return render_template('panel.html', 
        username=data[0], 
        email=data[1], 
        phone=data[2], 
        cbal=data[3], 
        wbal=data[4], 
        sch=data[5], 
        schoolid=data[6])
    else:
        message = 'Session expired please login again.'
        return render_template('login.html', message=message)
  else:
        message = 'Session expired please login again.'
        return render_template('login.html', message=message)

@app.route("/send", methods=["POST", "GET"])
def send():
    receiver = request.args.get('email')
    user = request.args.get('_id')
    receiverid = database.find_one({"email": receiver})
    x = database.find_one({"_id": user})
    token = x["token"]
    if request.method == "POST":
       if receiverid["_id"] == user:
        message="You can't send your self money."
        if "token" in session:
            if session["token"] == token:
                data = get.data(user)
                return render_template('panel.html',
                message=message, 
                username=data[0], 
                email=data[1], 
                phone=data[2], 
                cbal=data[3], 
                wbal=data[4], 
                sch=data[5], 
                schoolid=data[6])
            else:
                message = 'Session expired please login again.'
                return render_template('login.html', message=message)
        else:
            message = 'Session expired please login again.'
            return render_template('login.html', message=message)   
       else:
        amount = request.form.get("amount")
        message = get.transaction(amount, user, receiverid["_id"])
        if "token" in session:
            if session["token"] == token:
                data = get.data(user)
                return render_template('panel.html',
                message=message, 
                username=data[0], 
                email=data[1], 
                phone=data[2], 
                cbal=data[3], 
                wbal=data[4], 
                sch=data[5], 
                schoolid=data[6])
            else:
                message = 'Session expired please login again.'
                return render_template('login.html', message=message)
        else:
            message = 'Session expired please login again.'
            return render_template('login.html', message=message)   
    else:
            if receiverid:
                if "token" in session:
                    if session["token"] == token:
                        data = get.data(user)
                        message=''
                        return render_template('send.html',
                        message=message,
                        username=data[0], 
                        email=data[1], 
                        phone=data[2], 
                        cbal=data[3], 
                        wbal=data[4], 
                        sch=data[5], 
                        schoolid=data[6],
                        receiverEmail=receiver,
                        receiverName=receiverid["name"])
                    else:
                        message = 'Session expired please login again.'
                        return render_template('login.html', message=message)
                else:
                    message = 'Session expired please login again.'
                    return render_template('login.html', message=message)   
            else:
                message = 'User Not Found'
                user = request.args.get('_id')
                x = database.find_one({"_id": user})
                token = x["token"]
                if "token" in session:
                    if session["token"] == token:
                        data = get.data(user)
                        return render_template('send.html', 
                        message=message,
                        username=data[0], 
                        email=data[1], 
                        phone=data[2], 
                        cbal=data[3], 
                        wbal=data[4], 
                        sch=data[5], 
                        schoolid=data[6],
                        receiver=receiver)
                    else:
                        message = 'Session expired please login again.'
                        return render_template('login.html', message=message)
                else:
                    message = 'Session expired please login again.'
                    return render_template('login.html', message=message)
  
@app.route("/")
def home():
    return render_template('index.html')

# <Login Handler>
@app.route("/login", methods=["POST", "GET"])
def login():
    message = ''
    if "email" in session:
        check = database.find_one({"email": session["email"]})
        if check:
            userid = check["_id"]
            return redirect(url_for("panel", user=userid))
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        email_found = database.find_one({"email": email})
        if email_found:
            email_val = email_found['email']
            passwordcheck = email_found['password']
            
            if bcrypt.checkpw(password.encode('utf-8'), passwordcheck):
                session["token"] = email_found['token']
                session["email"] = email_val
                check = database.find_one({"email": session["email"]})
                userid = check["_id"]
                return redirect(url_for("panel", user=userid))
            else:
                if "email" in session:
                    check = database.find_one({"email": session["email"]})
                    userid = check["_id"]
                    return redirect("panel", user=userid)
                message = 'Password Incorrect'
                return render_template('login.html', message=message)
        else:
            message = 'No account found'
            return render_template('login.html', message=message)
    return render_template('login.html', message=message)

# <Signup Handler>
@app.route("/signup", methods=['post', 'get'])
def signup():
    message = ''
    if "token" in session:
        check = database.find_one({"email": session["email"]})
        if check:
            userid = check["_id"]
            return redirect(url_for("panel", user=userid))
    if request.method == "POST":
        user = request.form.get("fullname")
        email = request.form.get("email")
        password1 = request.form.get("password1")
        password2 = request.form.get("password2")
        school = request.form.get("school")
        user_found = database.find_one({"name": user})
        email_found = database.find_one({"email": email})
        if user_found:
            message = 'There already is a user by that name'
            return render_template('signup.html', message=message)
        if email_found:
            message = 'This email already exists in database'
            return render_template('signup.html', message=message)
        if password1 != password2:
            message = 'Passwords should match!'
            return render_template('signup.html', message=message)
        else:
            hashed = bcrypt.hashpw(password2.encode('utf-8'), bcrypt.gensalt())
            userid = secrets.token_hex(16)
            token = secrets.token_hex(32)
            user_input = {'_id': userid,'token': token,'name': user, 'email': email, 'password': hashed, 'school': school, 'wbalance': "0", 'tcrypto': "0", 'schoolID': None, 'phone#': None, 'time': time}
            database.insert_one(user_input)            
            user_data = database.find_one({"email": email})
            userid = user_data["_id"]
            session["token"] = token
            return redirect(url_for("panel", user=userid))
    return render_template('signup.html')

@app.route("/logout", methods=["POST", "GET"])
def logout():
    if "token" in session:
        session.pop("token", None)
        session.pop("email", None)
        return render_template("index.html")
    else:
        return render_template('index.html')

@app.errorhandler(404)
def not_found(e):
  return render_template('404.html'), 404

# <Starts application/run>
if __name__ == '__main__':
	app.run(
		host='0.0.0.0',
		port=random.randint(2000, 9000)
	)