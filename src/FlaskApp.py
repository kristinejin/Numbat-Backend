from flask import Flask, request, render_template, redirect, url_for, session
from src.auth import Login, CreateAccount
import requests
import functools


app = Flask(__name__)
app.secret_key = "hello"

def login_required(func):
    @functools.wraps(func)
    def secure_log():
        if "Username" not in session:
            return redirect(url_for("UserLogin"))
        return func()
    return secure_log

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
            session["Username"] = Username
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
            session["Username"] = Username
            return redirect(url_for("Home"))
        except Exception as e:
            return render_template("Error.html", Error = e)
    else:
        return render_template("RegisterHome.html")

@app.route("/Home", methods=["GET", "POST"])
@login_required
def Home():
    if request.method == 'POST':
        return "hello"
    else:
        return render_template("HomePage.html", Name=session["Username"])

@app.route("/Extract", methods=["GET","POST"])
@login_required
def Extract():
    if request.method == 'POST':
        FileName = request.form["FileName"]
        Password = request.form["Password"]
        url = "https://teamfudgeh17a.herokuapp.com/extract"
        data = {"FileName":FileName, "Password": Password}
        try:
            r = requests.post(url,data)
            return render_template("ExtractOutput.html", XML = r.text)
        except Exception as e:
            return render_template("Error.html", Error = e)         
    else:
        return render_template("extractMain.html")

@app.route("/Store", methods=["GET","POST"])
@login_required
def store():
    if request.method == 'POST':
        FileName = request.form["FileName"]
        Password = request.form["Password"]
        Xml = request.form["XML"]
        url = "https://teamfudgeh17a.herokuapp.com/store"
        data = {"FileName":FileName, "XML":Xml, "Password": Password}
        try:
            r = requests.post(url,data)
            if r.status_code == 200:
                return render_template("StoreOutput.html")
            else:
                return render_template("Error.html", Error = 'Not able to save File')        
        except Exception as e:
            return render_template("Error.html", Error = e)         
    else:
        return render_template("storeMain.html")

@app.route("/Remove", methods=["GET","POST"])
@login_required
def delete():
    if request.method == 'POST':
        FileName = request.form["FileName"]
        Password = request.form["Password"]
        url = "https://teamfudgeh17a.herokuapp.com/remove"
        data = {"FileName":FileName, "Password": Password}
        try:
            r = requests.post(url,data)
            if r.status_code == 200:
                print(r.status_code)
                return render_template("RemoveOutput.html")        
        except Exception as e:
            return render_template("Error.html", Error = e)         
    else:
        return render_template("RemoveMain.html")   


@app.route("/Search", methods=["GET","POST"])
@login_required
def search():
    if request.method == 'POST':
        sender_name = request.form["sender_name"]
        issue_date = request.form["issue_date"]
        Password = request.form["Password"]
        url = "https://teamfudgeh17a.herokuapp.com/search"
        data = {"issue_date":issue_date, "sender_name": sender_name, "Password": Password}
        try:
            r = requests.post(url,data)
            if r.status_code == 200:
                return render_template("SearchOutput.html", Files = r.text)
            else:
                return render_template("Error.html", Error = 'Not able to save File')        
        except Exception as e:
            return render_template("Error.html", Error = e)         
    else:
        return render_template("SearchMain.html") 

if __name__ == '__main__':
    app.debug = True
    app.run()