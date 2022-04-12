from flask import Flask, request, render_template, redirect, url_for, session
from src.auth import Login, CreateAccount, auth_passwordreset_request_base, auth_passwordreset_reset_base
# from json import dumps
from src.receive import receiveAndStore
from src.check_num_render_or_store import checkQuota
import requests
import functools
import json


app = Flask(__name__)
app.secret_key = "hello"


def loginRequired(func):
    @functools.wraps(func)
    def secureLog():
        if "Username" not in session:
            return redirect(url_for("UserLogin"))
        return func()

    return secureLog


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
        companyCode = request.form["CompanyCode"]
        email = request.form["Email"]
        try:
            CreateAccount(Username, Password, companyCode, email)
            session["Username"] = Username
            return redirect(url_for("Home"))
        except Exception as e:
            return render_template("Error.html", Error=e)
    else:
        return render_template("RegisterHome.html")


@app.route("/Home", methods=["GET", "POST"])
@loginRequired
def Home():
    if request.method == "POST":
        return "hello"
    else:
        return render_template("HomePage.html", Name=session["Username"])


@app.route("/Extract", methods=["GET", "POST"])
@loginRequired
def Extract():
    if request.method == "POST":
        FileName = request.form["FileName"]
        Password = request.form["Password"]
        url = "https://teamfudgeh17a.herokuapp.com/extract"
        data = {"FileName": FileName, "Password": Password}
        try:
            r = requests.post(url, data)
            return render_template("ExtractOutput.html", XML=r.text)
        except Exception as e:
            return render_template("Error.html", Error=e)
    else:
        return render_template("extractMain.html")


@app.route("/Store", methods=["GET", "POST"])
@loginRequired
def store():
    if request.method == "POST":
        FileName = request.form["FileName"]
        Password = request.form["Password"]
        Xml = request.form["XML"]

        if checkQuota("None", Password, "store") == "Fail":
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
@loginRequired
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
@loginRequired
def search():
    if request.method == "POST":
        senderName = request.form["sender_name"]
        issueDate = request.form["issue_date"]
        Password = request.form["Password"]
        url = "https://teamfudgeh17a.herokuapp.com/search"
        data = {
            "issue_date": issueDate,
            "senderName": senderName,
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
@loginRequired
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
@loginRequired
def rendering():
    if request.method == 'POST':
        FileName = request.form["FileName"]
        Password = request.form["Password"]

        # File type can only be pdf/html/json
        FileType = request.form["FileType"]

        extractURL = "https://teamfudgeh17a.herokuapp.com/extract"
        extractData = {"FileName": FileName, "Password": Password}

        # API: https://app.swaggerhub.com/apis/r-kaisar/e-invoice-rendering/1.0.0#/rendering
        renderUploadURL = "https://e-invoice-rendering-brownie.herokuapp.com/invoice/rendering/upload"
        renderDownloadURL = "https://e-invoice-rendering-brownie.herokuapp.com/invoice/rendering/download"

        try:
            # get the invoice as a string in the storage db
            fileStr = requests.post(extractURL, extractData)
            # print(fileStr.text)
            # convert string to a binary xml file
            with open("str_to_xml.xml", "w") as f:
                f.write(str(fileStr.text))
            # payload for rendering upload request
            # rendering upload ret type: {"file_ids": [int_file_id]}
            pload = {'file': open('str_to_xml.xml', 'r')}
            renderUploadRequest = requests.post(
                renderUploadURL, files=pload)
            renderUpload = json.loads(renderUploadRequest.text)
            # call rendering download endpoint
            # rendered file in rendering_download
            rendering_download = requests.get(
                renderDownloadURL, params={"file_id": renderUpload["file_ids"][0], "file_type": FileType})
            assert rendering_download.status_code == 200
            if checkQuota("None", Password, "render") == "Fail":
                return render_template("Error.html", Error="Rendered Invoice Quota is FULL")

            return render_template("renderOutput.html", file_path=rendering_download.url)
        except Exception as e:
            return render_template("Error.html", Error=e)
    else:
        return render_template("renderMain.html")

@APP.route("passwordreset/request", methods=["POST"])
def auth_passwordreset_request_v1():

    email = request.get_json("email")

    results = auth_passwordreset_request_base(email)

    return dumps({"reset_code_status": results})


@APP.route("passwordreset/reset", methods=["POST"])
def auth_passwordreset_reset_v1():

    inputs = request.get_json()
    reset_code = inputs["reset_code"]
    new_password = inputs["new_password"]

    results = auth_passwordreset_reset_base(reset_code, new_password)

    return dumps({"reset_status": results})


if __name__ == '__main__':
    app.debug = True
    app.run()