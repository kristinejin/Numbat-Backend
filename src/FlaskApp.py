from flask import Flask, request, render_template, redirect, url_for, session
from flask import session
from src.config import DATABASE_URL
from src.auth import Login, CreateAccount
import requests


app = Flask(__name__)
app.secret_key = "hello"

def login_required(func):
    return func

#Account Creation, Login
@app.route("/")
def Start():
    return(redirect(url_for("UserLogin")))

#Store API
@app.route("/UserLogin", methods=["POST", "GET"])
def UserLogin():
    if request.method == 'POST':
        Username = request.form["UserName"]
        Password = request.form["Password"]
        try:
            Login(Username,Password)
            session[Username] = Password
            return redirect(url_for("Home"))
        except Exception as e:
            return render_template("Error.html", Error = e)
    else:
        return render_template("LoginHome.html")

@app.route("/Register", methods=["POST", "GET"])
def Register():
    if request.method == 'POST':
        Username = request.form["UserName"]
        Password = request.form["Password"]
        try:
            CreateAccount(Username,Password)
            return redirect(url_for("Home"))
        except Exception as e:
            return render_template("Error.html", Error = e)
    else:
        return render_template("RegisterHome.html")

@app.route("/Home", methods=["POST,GET"])
@login_required
def Home():
    if request.method == 'POST':
        pass
    else:
        return render_template("HomePage.html")

if __name__ == '__main__':
    app.debug = True
    app.run()