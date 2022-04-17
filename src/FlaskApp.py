from flask import Flask, request, render_template, redirect, url_for, session, send_file
from src.auth import Login, CreateAccount, createCompany
from src.other import receiveAndStore, companyCodeFromUsername
from src.invoices import invoiceCreate
from src.check_num_render_or_store import checkQuota
import requests
import functools
from io import BytesIO
from json import dumps
from flask_cors import CORS
from src.error import InputError


app = Flask(__name__)
app.secret_key = "hello"
CORS(app)


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
            return dumps({'loginStatus': True})
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
            return render_template("/errors/registerError.html", Error=e)
    else:
        return render_template("RegisterHome.html")


@app.route("/register/company", methods=["POST"])
def createCompanyRoute():
    """
    required field includes:
    # name
    # abn
    # street
    # suburb
    # postcode
    # companyCode
    """
    name = request.form["name"]
    abn = request.form["abn"]
    street = request.form["street"]
    suburb = request.form["suburb"]
    postcode = request.form["postcode"]
    companyCode = request.form["companyCode"]
    return dumps(createCompany(
        name, abn, street, suburb, postcode, companyCode))


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
        Username = session["Username"]
        Password = companyCodeFromUsername(Username)
        FileName = request.form["FileName"]
        url = "https://teamfudgeh17a.herokuapp.com/extract"
        data = {"FileName": FileName, "Password": Password}
        try:
            r = requests.post(url, data)
            return render_template("ExtractOutput.html", XML=r.text)
        except Exception as e:
            return render_template("/errors/extractError.html", Error=e)
    else:
        return render_template("extractMain.html")


@app.route("/Store", methods=["GET", "POST"])
@loginRequired
def store():
    if request.method == "POST":

        FileName = request.form["FileName"]
        Xml = request.form["XML"]

        # Password = request.form["Password"]
        Username = session["Username"]
        Password = companyCodeFromUsername(Username)

        if checkQuota("None", Password, "store") == "Fail":
            return render_template("Error.html", Error="Stored Invoice Quota is FULL")

        url = "https://teamfudgeh17a.herokuapp.com/store"
        data = {"FileName": FileName, "XML": Xml, "Password": Password}
        try:
            r = requests.post(url, data)
            if r.status_code == 200:
                return render_template("StoreOutput.html")
            else:
                return render_template("/errors/storeError.html", Error="Not able to save File")
        except Exception as e:
            return render_template("/errors/storeError.html", Error=e)
    else:
        return render_template("storeMain.html")


@app.route("/Remove", methods=["GET", "POST"])
@loginRequired
def delete():
    if request.method == "POST":
        FileName = request.form["FileName"]
        # Password = request.form["Password"]
        Username = session["Username"]
        Password = companyCodeFromUsername(Username)

        url = "https://teamfudgeh17a.herokuapp.com/remove"
        data = {"FileName": FileName, "Password": Password}
        try:
            r = requests.post(url, data)
            if r.status_code == 200:
                print(r.status_code)
                return render_template("RemoveOutput.html")
        except Exception as e:
            return render_template("/errors/removeError.html", Error=e)
    else:
        return render_template("RemoveMain.html")


@app.route("/Search", methods=["GET", "POST"])
@loginRequired
def search():
    if request.method == "POST":
        senderName = request.form["sender_name"]
        issueDate = request.form["issue_date"]
        Username = session["Username"]
        Password = companyCodeFromUsername(Username)

        url = "https://teamfudgeh17a.herokuapp.com/search"
        data = {
            "issue_date": issueDate,
            "sender_name": senderName,
            "Password": Password,
        }
        try:
            r = requests.post(url, data)
            if r.status_code == 200:
                return render_template("SearchOutput.html", Files=r.text)
            else:
                return render_template("/errors/searchError.html", Error="There's no file matching the keywords.")
        except Exception as e:
            return render_template("/errors/searchError.html", Error=e)
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
        data = {
            "FileName": request.json['received_at_timestamp'], "XML": xml, "Password": companyCode}
        try:
            r = requests.post(url, data)
            if r.status_code == 200:
                return '200'
            else:
                return "Failed to receive"
        except Exception as e:
            return render_template("Error.html", Error=e)
    else:
        return render_template("Error.html")


@app.route("/Render", methods=["GET", "POST"])
@loginRequired
def rendering():
    if request.method == 'POST':
        FileName = request.form["FileName"]
        Username = session["Username"]
        Password = companyCodeFromUsername(Username)

        # File type can only be pdf/html/json
        # Make filetype lowercase
        # FileType = request.form["FileType"]
        # FileType.lower()

        extractURL = "https://teamfudgeh17a.herokuapp.com/extract"
        extractData = {"FileName": FileName, "Password": Password}

        # API: https://app.swaggerhub.com/apis/r-kaisar/e-invoice-rendering/1.0.0#/rendering
        # renderUploadURL = "https://e-invoice-rendering-brownie.herokuapp.com/invoice/rendering/upload"
        # renderDownloadURL = "https://e-invoice-rendering-brownie.herokuapp.com/invoice/rendering/download"
        renderUploadURL = "https://www.invoicerendering.com/einvoices?renderType=pdf&lang=en"

        try:
            # get the invoice as a string in the storage db
            fileStr = requests.post(extractURL, data=extractData)
            # return fileStr.text
            # convert string to a binary xml file
            with open("str_to_xml.xml", "w") as f:
                f.write(str(fileStr.text))
            # payload for rendering upload request
            # rendering upload ret type: {"file_ids": [int_file_id]}
            pload = {'xml': open('str_to_xml.xml', 'rb')}
            renderUploadRequest = requests.post(
                renderUploadURL, files=pload)
            if renderUploadRequest.status_code == 200:
                # do the render quota thing
                if checkQuota("None", Password, "render") == "Fail":
                    raise Exception(
                        "Invoice cannot be rendered: Account Limit Reached")
                return send_file(BytesIO(renderUploadRequest.content), mimetype='application/pdf')
                # as_attachment=True, download_name='static_fname'
            return dumps(renderUploadRequest)
        except Exception as e:
            raise e
    else:
        return render_template("renderMain.html")


@app.route("/Create", methods=["POST"])
@loginRequired
def invoice_create_route():
    # https://app.swaggerhub.com/apis/SENG2021-DONUT/e-invoice_creation/1.0.0#/XML%20Conversion/jsonconvert
    pload = request.get_json()
    fileName = pload['fileName']
    Username = session["Username"]
    supplierCompanyCode = companyCodeFromUsername(Username)
    invoiceDict = invoiceCreate(pload, supplierCompanyCode)
    # TODO: required info:
    """
    * General Info:
    fileName: name of the file to be stored
    IssueDate (input format: yyyy-mm-dd)
    CustomerRegistration (trading name of the customer / buyer)
    CustomerStreet
    CustomerCity
    CustomerPost
    * For invoice total: 
    int: TaxableAmount (total price of all purchases without the gst)
    int: PayableAmount (total price includes gst)
    * For a single product on invoice: 
    InvoiceName (name of product)
    int: InvoiceQuantity (quantity of a single product) -> InvoiceQuantity2..n
    int: InvoicePriceAmount (price/unit of a single product)
    """

    createUrl = "https://seng-donut-deployment.herokuapp.com/json/convert"
    r = requests.post(
        createUrl, json=invoiceDict)

    if r.status_code == 200:
        if checkQuota("None", supplierCompanyCode, "store") == "Fail":
            raise InputError("Invoice cannot be stored: Account Limit Reached")

        storeUrl = "https://teamfudgeh17a.herokuapp.com/store"
        data = {"FileName": fileName, "XML": r.content.decode('ascii'),
                "Password": supplierCompanyCode}
        storeResp = requests.post(storeUrl, data=data)
        if storeResp.status_code != 200:
            raise InputError("Invoice cannot be stored")
        return send_file(BytesIO(r.content), mimetype='text/xml', as_attachment=True, download_name=f"{fileName}.xml")
    else:
        raise InputError(
            description="Invoice cannot be created: Duplicated Filename or Invalid XML format")


if __name__ == '__main__':
    app.debug = True
    app.run()
