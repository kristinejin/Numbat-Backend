from flask import Flask, request, render_template, redirect, url_for, session
from src.auth import Login, CreateAccount
# from json import dumps
from src.receive import receiveAndStore
from src.check_num_render_or_store import check_okay
import requests
import functools
import json


app = Flask(__name__)
app.secret_key = "hello"


def login_required(func):
    @functools.wraps(func)
    def secure_log():
        if "Username" not in session:
            return redirect(url_for("UserLogin"))
        return func()

    return secure_log


# Account Creation, Login
@app.route("/")
def Start():
    return redirect(url_for("UserLogin"))


# Store API
@app.route("/UserLogin", methods=["POST", "GET"])
def UserLogin():
    if request.method == "POST":
        Username = request.form["UserName"]
        Password = request.form["Password"]
        try:
            Login(Username, Password)
            session["Username"] = Username
            return redirect(url_for("Home"))
        except Exception as e:
            return render_template("Error.html", Error=e)
    else:
        return render_template("LoginHome.html")


@app.route("/Register", methods=["POST", "GET"])
def Register():
    if request.method == "POST":
        Username = request.form["UserName"]
        Password = request.form["Password"]
        companycode = request.form["CompanyCode"]
        email = request.form["Email"]
        try:
            CreateAccount(Username, Password, companycode, email)
            session["Username"] = Username
            return redirect(url_for("Home"))
        except Exception as e:
            return render_template("Error.html", Error=e)
    else:
        return render_template("RegisterHome.html")


@app.route("/Home", methods=["GET", "POST"])
@login_required
def Home():
    if request.method == "POST":
        return "hello"
    else:
        return render_template("HomePage.html", Name=session["Username"])


@app.route("/Extract", methods=["GET", "POST"])
@login_required
def Extract():
    if request.method == "POST":
        FileName = request.form["FileName"]
        Password = request.form["Password"]
        url = "https://teamfudgeh17a.herokuapp.com/extract"
        data = {"FileName": FileName, "Password": Password}
        try:
            r = requests.post(url, data)
            print(type(r.text))
            return render_template("ExtractOutput.html", XML=r.text)
        except Exception as e:
            return render_template("Error.html", Error=e)
    else:
        return render_template("extractMain.html")


@app.route("/Store", methods=["GET", "POST"])
@login_required
def store():
    if request.method == "POST":
        FileName = request.form["FileName"]
        Password = request.form["Password"]
        Xml = request.form["XML"]

        if check_okay("None", Password, "store") == "Fail":
            return render_template("Error.html", Error="Stored Invoice Quota is FULL")

        url = "https://teamfudgeh17a.herokuapp.com/store"
        data = {"FileName": FileName, "XML": Xml, "Password": Password}
        try:
            r = requests.post(url, data)
            if r.status_code == 200:
                return render_template("StoreOutput.html")
            else:
                return render_template("Error.html", Error="Not able to save File")
        except Exception as e:
            return render_template("Error.html", Error=e)
    else:
        return render_template("storeMain.html")


@app.route("/Remove", methods=["GET", "POST"])
@login_required
def delete():
    if request.method == "POST":
        FileName = request.form["FileName"]
        Password = request.form["Password"]
        url = "https://teamfudgeh17a.herokuapp.com/remove"
        data = {"FileName": FileName, "Password": Password}
        try:
            r = requests.post(url, data)
            if r.status_code == 200:
                print(r.status_code)
                return render_template("RemoveOutput.html")
        except Exception as e:
            return render_template("Error.html", Error=e)
    else:
        return render_template("RemoveMain.html")


@app.route("/Search", methods=["GET", "POST"])
@login_required
def search():
    if request.method == "POST":
        sender_name = request.form["sender_name"]
        issue_date = request.form["issue_date"]
        Password = request.form["Password"]
        url = "https://teamfudgeh17a.herokuapp.com/search"
        data = {
            "issue_date": issue_date,
            "sender_name": sender_name,
            "Password": Password,
        }
        try:
            r = requests.post(url, data)
            if r.status_code == 200:
                return render_template("SearchOutput.html", Files=r.text)
            else:
                return render_template("Error.html", Error="Not able to save File")
        except Exception as e:
            return render_template("Error.html", Error=e)
    else:
        return render_template("SearchMain.html")


@app.route("/Logout", methods=["GET", "POST"])
@login_required
def logout():
    if request.method == "POST":
        if request.form["Logout"] == "Logout":
            session.clear()
            return redirect(url_for("UserLogin"))
    else:
        return render_template("Logout.html")


@app.route("/receive", methods=["POST"])
def receive_data():
   
    if request.method == "POST":
        xml = request.json['xml_attachments']
        email = request.json['sender_address']
        
        companyCode = receiveAndStore(email)

        url = "https://teamfudgeh17a.herokuapp.com/store"
        data = {"FileName": request.json['received_at_timestamp'], "XML":xml, "Password": companyCode}
        try:
            r = requests.post(url,data)
            if r.status_code == 200:
                return '200'
            else:
                return "Failed to receive"
        except Exception as e:
            return render_template("Error.html", Error = e)
    else:
        return render_template("Error.html")      

@app.route("/Render", methods=["GET", "POST"])
@login_required
def rendering():
    if request.method == 'POST':
        FileName = request.form["FileName"]
        Password = request.form["Password"]

        # File type can only be pdf/html/json
        FileType = request.form["FileType"]

        extract_url = "https://teamfudgeh17a.herokuapp.com/extract"
        extract_data = {"FileName": FileName, "Password": Password}

        # API: https://app.swaggerhub.com/apis/r-kaisar/e-invoice-rendering/1.0.0#/rendering
        rendering_upload_url = "https://e-invoice-rendering-brownie.herokuapp.com/invoice/rendering/upload"
        rendering_download_url = "https://e-invoice-rendering-brownie.herokuapp.com/invoice/rendering/download"

        try:
            # get the invoice as a string in the storage db
            file_str = requests.post(extract_url, extract_data)
            # print(file_str.text)
            # convert string to a binary xml file
            with open("str_to_xml.xml", "w") as f:
                f.write(str(file_str.text))
            # payload for rendering upload request
            # rendering upload ret type: {"file_ids": [int_file_id]}
            pload = {'file': open('str_to_xml.xml', 'r')}
            rendering_upload_request = requests.post(
                rendering_upload_url, files=pload)
            rendering_upload = json.loads(rendering_upload_request.text)
            # call rendering download endpoint
            # rendered file in rendering_download
            rendering_download = requests.get(
                rendering_download_url, params={"file_id": rendering_upload["file_ids"][0], "file_type": FileType})
            assert rendering_download.status_code == 200
            if check_okay("None", Password, "render") == "Fail":
                return render_template("Error.html", Error="Rendered Invoice Quota is FULL")

            return render_template("renderOutput.html", file_path=rendering_download.url)
        except Exception as e:
            return render_template("Error.html", Error=e)
    else:
        return render_template("renderMain.html")


if __name__ == '__main__':
    app.debug = True
    app.run()