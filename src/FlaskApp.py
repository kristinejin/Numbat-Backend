from flask import Flask, request, render_template, redirect, url_for, session
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

@app.route("/Home", methods=["POST", "GET"])
@login_required
def Home():
    if request.method == 'POST':
        pass
    else:
        return render_template("HomePage.html")

@app.route("/Extract", methods=["GET","POST"])
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

# @app.route("/Delete", methods=["GET","POST"])
# def delete():
#     if request.method == 'POST':
#         FileName = request.form["FileName"]
#         Password = request.form["Password"]
#         url = "https://teamfudgeh17a.herokuapp.com/store"
#         data = {"FileName":FileName, "Password": Password}
#         try:
#             r = requests.post(url,data)
#             if r.status_code == 200:
#                 return render_template("StoreOutput.html")
#             else:
#                 return render_template("Error.html", Error = 'Not able to save File')        
#         except Exception as e:
#             return render_template("Error.html", Error = e)         
#     else:
#         return render_template("storeMain.html")   

if __name__ == '__main__':
    app.debug = True
    app.run()