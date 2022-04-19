# from tkinter.tix import InputOnly
# from this import d
from flask import Flask, request, redirect, url_for, session, send_file
import flask
from src.auth import Login, CreateAccount, createCompany, auth_passwordreset_request_base, auth_passwordreset_reset_base
from src.other import receiveAndStore, companyCodeFromUsername, companyCodeFromName
from src.invoices import invoiceCreate
from src.check_num_render_or_store import checkQuota
from src.select_all import selectAll
import requests
import functools
from io import BytesIO
from json import dumps
import json
from flask_cors import CORS
from src.error import InputError, AccessError
import psycopg2
from src.config import DATABASE_URL
from src.senders import addSender, removeSender, checkSenderAccess


app = Flask(__name__)
app.secret_key = "hello"
CORS(app, expose_headers=["Content-Disposition", "Content-Type"])


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
@app.route("/UserLogin", methods=["POST"])
def UserLogin():
    Username = request.form["UserName"]
    Password = request.form["Password"]
    loginStatus = Login(Username, Password)
    if loginStatus:
        session["Username"] = Username
        return dumps(
            {
                'loginStatus': loginStatus
            }
        )


@app.route("/Register", methods=["POST"])
def Register():
    """
    params:
    - UserName
    - Password
    - CompanyCode
    - Email
    """
    Username = request.form["UserName"]
    Password = request.form["Password"]
    companyCode = request.form["CompanyCode"]
    email = request.form["Email"]
    createStatus = CreateAccount(Username, Password, companyCode, email)
    if createStatus:
        session["Username"] = Username
        return dumps({
            'createStatus': createStatus
        })


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


@app.route("/Home", methods=["POST"])
# removed for testing purposes
# @loginRequired
def Home():
    # Username = session["Username"]
    Username = request.form["UserName"]
    companyCode = companyCodeFromUsername(Username)
    retVal = selectAll(companyCode)
    return dumps({"invoices": retVal})


@app.route("/Extract", methods=["POST"])
# removed for testing purposes
# @loginRequired
def Extract():
    """
    params:
    FileName
    """
    # Username = session["Username"]
    Username = "alpha"
    Password = companyCodeFromUsername(Username)
    FileName = request.form["FileName"]
    url = "https://teamfudgeh17a.herokuapp.com/extract"
    data = {"FileName": FileName, "Password": Password}
    try:
        r = requests.post(url, data)
        return send_file(BytesIO(
            r.text.encode('utf-8')), mimetype='text/xml', download_name=f"{FileName}.xml", as_attachment=True)
    except Exception as e:
        raise e


@app.route("/Store", methods=["POST"])
# removed for testing purposes
# @loginRequired
def store():

    FileName = request.form["FileName"]
    binaryFile = request.files['xml']
    Xml = binaryFile.read().decode('UTF-8')

    # Password = request.form["Password"]
    # Username = session["Username"]
    Username = "alpha"
    Password = companyCodeFromUsername(Username)

    if checkQuota("None", Password, "store") == "Fail":
        raise InputError(description="Stored Invoice Quota is FULL")

    url = "https://teamfudgeh17a.herokuapp.com/store"
    data = {"FileName": FileName, "XML": Xml, "Password": Password}
    try:
        r = requests.post(url, data)
        if r.status_code == 200:
            return dumps({
                "storeStatus": True
            })
        else:
            raise InputError(description="File cannot be stored")
    except Exception as e:
        raise e


@app.route("/Remove", methods=["POST"])
# removed for testing purposes
# @loginRequired
def remove():

    FileName = request.form["FileName"]
    """
    params:
    FileName
    """
    # Username = session["Username"]
    Username = "alpha"
    Password = companyCodeFromUsername(Username)

    url = "https://teamfudgeh17a.herokuapp.com/remove"
    data = {"FileName": FileName, "Password": Password}
    r = requests.post(url, data)
    if r.status_code == 200:
        return {
            'removeStatus': True
        }
    else:
        raise InputError(
            description="File cannot be removed: Incorrect file nme")


@app.route("/Search", methods=["POST"])
# removed for testing purposes
# @loginRequired
def search():
    """
    params:
    either/both: sender_name / issue_date
    return: {
        'file_names':[name1, name2, ... namen]
    }
    """
    issueDate = str()
    senderName = str()
    try:
        senderName = request.form["sender_name"]
        issueDate = request.form["issue_date"]
    except Exception:
        try:
            issueDate = request.form["issue_date"]
        except Exception:
            pass
    if issueDate == '' and senderName == '':
        raise InputError(description="Please input at least one keyword")
    # Username = session["Username"]
    Username = "alpha"
    Password = companyCodeFromUsername(Username)
    url = "https://teamfudgeh17a.herokuapp.com/search"
    data = {
        "issue_date": issueDate,
        "sender_name": senderName,
        "Password": Password
    }
    r = requests.post(url, data)
    if r.status_code == 200:
        return dumps(
            json.loads(r.text))
    else:
        return dumps({
            'searchOutput': "No file contains input keywords"
        })


@app.route("/Logout", methods=["POST"])
# removed for testing purposes
# @loginRequired
def logout():
    if request.form["Logout"] == "Logout":
        session.clear()
        return dumps({
            'logoutStatus': True
        })


@app.route("/receive", methods=["POST"])
def receive_data():

    xml = request.json['xml_attachments']
    email = request.json['sender_address']

    companyCode = receiveAndStore(email)

    url = "https://teamfudgeh17a.herokuapp.com/store"
    data = {
        "FileName": request.json['received_at_timestamp'], "XML": xml, "Password": companyCode}
    r = requests.post(url, data)
    if r.status_code == 200:
        return dumps({
            'receiveStatus': True
        })
    else:
        return dumps({
            'receiveStatus': "Invoice cannot be stored"
        })


@app.route("/Render", methods=["POST"])
# removed for testing purposes
# @loginRequired
def rendering():
    """
    Params:
    - Filenmae

    Returns:
    send_file function - BytesIO PDF file
    (can be change to a download attatchment pop up screen)
    """
    FileName = request.form["FileName"]
    # Username = session["Username"]
    Username = "alpha"
    Password = companyCodeFromUsername(Username)

    extractURL = "https://teamfudgeh17a.herokuapp.com/extract"
    extractData = {"FileName": FileName, "Password": Password}

    # API: https://app.swaggerhub.com/apis/r-kaisar/e-invoice-rendering/1.0.0#/rendering
    # renderUrl = "https://e-invoice-rendering-brownie.herokuapp.com/invoice/rendering/upload"
    # renderDownloadURL = "https://e-invoice-rendering-brownie.herokuapp.com/invoice/rendering/download"
    renderUrl = "https://www.invoicerendering.com/einvoices?renderType=pdf&lang=en"

    try:
        # get the invoice as a string in the storage db
        fileStr = requests.post(extractURL, data=extractData)

        # convert string to a binary xml file
        with open("str_to_xml.xml", "w") as f:
            f.write(str(fileStr.text))

        # payload for rendering upload request
        pload = {'xml': open('str_to_xml.xml', 'rb')}
        renderRequest = requests.post(
            renderUrl, files=pload)
        if renderRequest.status_code == 200:
            if checkQuota("None", Password, "render") == "Fail":
                raise Exception(
                    "Invoice cannot be rendered: Account Limit Reached")
            Response = flask.Response()
            Response.headers["Content-Type"] = 'application/pdf'
            Response.headers["Content-Disposition"] = f"attachment; filename='{FileName}.pdf'"
            print(Response.headers)
            with open("src/text.pdf", "wb") as f:
                f.write(renderRequest.content)
            # old code
            """
            # return send_file(BytesIO(renderRequest.content), mimetype='application/pdf')
            # as_attachment=True, download_name=f"{FileName}
            """
            return send_file('text.pdf',
                             mimetype='application/pdf',
                             download_name=f"{FileName}.pdf")
        else:
            raise Exception(f"Render API Error: {renderRequest.content}")
    except Exception as e:
        raise e


@app.route("/Create", methods=["POST"])
# removed for testing purposes
# @loginRequired
def invoice_create_route():
    """
    Params(NOTE: Create takes in json input)
    * General Info:
        - fileName: name of the file to be stored
        - IssueDate (input format: yyyy-mm-dd)
    * Customer Info: 
        - CustomerRegistration (trading name of the customer / buyer)
        - CustomerStreet
        - CustomerCity
        - CustomerPost
    * For invoice total: 
        - TaxableAmount (int) (total price of all purchases without the gst)
        - PayableAmount (int) (total price includes gst)
    * For a single product on invoice: 
        - InvoiceName (name of product) -> InvoiceName2..n
        - InvoiceQuantity (int) (quantity of a single product) -> InvoiceQuantity2..n
        - InvoicePriceAmount (int) (price/unit of a single product) -> InvoicePriceAmount2..n

    Input Example:
    {
        "fileName":"helloWorld",
        "IssueDate": "2022-03-01",
        "CustomerRegistration": "UNSW",
        "CustomerStreet": "700 UNSW Street",
        "CustomerCity": "Kensington",
        "CustomerPost": 2030,
        "TaxableAmount": 500,
        "PayableAmount": 550,
        "InvoiceName": "Office Chair",
        "InvoiceQuantity": 2,
        "InvoicePriceAmount": 250
    }

    Returns:
    send_file function - BytesIO XML file
    (can be change to a download attatchment pop up screen)
    """
    # https://app.swaggerhub.com/apis/SENG2021-DONUT/e-invoice_creation/1.0.0#/XML%20Conversion/jsonconvert
    pload = request.get_json()
    fileName = pload['fileName']
    # Username = session["Username"]
    Username = "alpha"
    supplierCompanyCode = companyCodeFromUsername(Username)
    invoiceDict = invoiceCreate(pload, supplierCompanyCode)

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


@app.route("/Test", methods=["POST"])
# removed for testing purposes
# @loginRequired
def userinfo_return():
    Username = request.form["UserName"]
    # Username = session["Username"]

    conn = psycopg2.connect(DATABASE_URL, sslmode='require')

    cur = conn.cursor()

    # Insert data into db
    sql = """
        select a.username, a.password, a.email, b.numrenders, c.numinvoices 
        from userinfo a, 
        (select sum(numrenders) as numrenders from userinfo where companycode = (select companycode from userinfo where username  = %s)) as b, 
        (select count(distinct file_name) as numinvoices from invoices where password = (select companycode from userinfo where username  = %s)) as c where a.username = %s
        """
    val = [Username, Username, Username]
    cur.execute(sql, val)

    retVal = cur.fetchall()

    account = []
    print(retVal)
    for tup in retVal[0]:
        account.append(tup)

    cur.close()
    conn.close()

    return dumps({"userinfo": {"username": account[0], "password": account[1], "email": account[2], "numrenders": account[3], "numinvoices": account[4]}})


@app.route("/passwordreset/request", methods=["POST"])
def auth_passwordreset_request_v1():
    email = request.get_json("email")

    results = auth_passwordreset_request_base(email)

    return dumps({"Request_Status": results})


@app.route("/passwordreset/reset", methods=["POST"])
def auth_passwordreset_reset_v1():

    inputs = request.get_json()
    reset_code = inputs["reset_code"]
    new_password = inputs["new_password"]

    results = auth_passwordreset_reset_base(reset_code, new_password)
    return dumps({"Reset_Status": results})


@app.route("/senders/add", methods=["POST"])
# removed for testing purposes
# @loginRequired
def add_sender_route():
    '''
    Description: 
    - Given a sender name, add the sender to the receiver company's sender list 

    Params:
    - senderName: trading name of the sender to be added

    Exception:
    - InputError when:
        1. No sender associate with given senderName (sender does not exist)
        2. Sender name have already been added

    Return:{ 'addSenderStatus': True } on success
    '''

    senderName = request.form['senderName']
    # Username = session["Username"]
    Username = "alpha"
    companyCode = companyCodeFromUsername(Username)
    return dumps(addSender(companyCode, senderName))


@app.route("/senders/remove", methods=["DELETE"])
# removed for testing purposes
# @loginRequired
def remove_sender_route():
    '''
    NOTE: This route is DELETE method, if it doesn't work well, please change to POST or PUT
    Description:
    - Given a sender name, delete the sender from the receiver company's sender list 

    Params:
    - senderName: trading name of the sender to be removed

    Exception:
    - InputError when:
        1. No sender associate with given senderName (sender does not exist)
        2. senderName does not exist on the receiver's sender list (i.e., the sender have not been added/already been deleted)

    Return:{ 'removeSenderStatus': True } on success
    '''
    senderName = request.form['senderName']
    # Username = session["Username"]
    Username = "alpha"
    companyCode = companyCodeFromUsername(Username)
    return dumps(removeSender(companyCode, senderName))


@app.route("/Send", methods=["POST"])
# removed for testing purposes
# @loginRequired
def internal_sending_route():
    '''
    Description:
    - Given a sender name, delete the sender from the receiver company's sender list 

    Params:
    - senderName: trading name of the sender to be removed

    Exception:
    - InputError when:
        1. No sender associate with given senderName (sender does not exist)
        2. senderName does not exist on the receiver's sender list (i.e., the sender have not been added/already been deleted)

    Return:{ 'removeSenderStatus': True } on success
    '''
    receiverName = request.form["receiverName"]
    FileName = request.form["FileName"]
    # Username = session["Username"]
    Username = "alpha"
    senderCompanyCode = companyCodeFromUsername(Username)
    receiverCompanyCode = companyCodeFromName(receiverName)['companyCode']

    # check if sender have access to send to receiver
    access = checkSenderAccess(receiverCompanyCode, senderCompanyCode)
    if not access['isAuthorised']:
        raise AccessError(
            description=f"Cannot send to {receiverName}: Please request permission from this company")

    # extract from sender companyCode - using storage api
    extractUrl = "https://teamfudgeh17a.herokuapp.com/extract"
    data = {"FileName": FileName, "Password": senderCompanyCode}
    extract = requests.post(extractUrl, data)
    if extract.status_code != 200:
        raise InputError(
            description=f"Cannot send {FileName}: File does not exist")

    # check receiver quota
    if checkQuota("None", receiverCompanyCode, "store") == "Fail":
        raise InputError(
            description=f"Cannot send file: Contact {receiverName}, receiver storage is full")

    # check if file name exist in the receiver storage:
    # TODO: not sure if this works, check please!!!!
    receiverData = {"FileName": FileName, "Password": receiverCompanyCode}

    try:
        receiverExtract = requests.post(extractUrl, receiverData)
        if receiverExtract.status_code == 200:
            FileName += '(1)'
    except Exception:
        pass

    # store to receiver companyCode - using storage api
    storeUrl = "https://teamfudgeh17a.herokuapp.com/store"
    data = {"FileName": FileName, "XML": extract.text,
            "Password": receiverCompanyCode}
    storeResp = requests.post(storeUrl, data=data)
    if storeResp.status_code != 200:
        raise Exception("Something went wrong: Invoice Cannot be Stored")

    # end - return status
    return {
        'sendStatus': True
    }


if __name__ == '__main__':
    app.debug = True
    app.run()
