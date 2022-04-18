from src.config import DATABASE_URL
from src.error import InputError
import psycopg2

def receiveAndStore(email: str):

    try:
        conn = psycopg2.connect(DATABASE_URL, sslmode='require')
        cur = conn.cursor()

        sql = "SELECT companycode FROM userinfo WHERE email = %s"
        val = [email]

        cur.execute(sql, val)

        companyCode = cur.fetchone()

        cur.close()
        conn.close()

        return companyCode[0]

    except Exception as e:
        print(e)

def companyCodeFromUsername(username: str):

    try:
        conn = psycopg2.connect(DATABASE_URL, sslmode='require')
        cur = conn.cursor()

        sql = "SELECT companycode FROM userinfo WHERE username = %s"
        val = [username]

        cur.execute(sql, val)

        companyCode = cur.fetchone()

        cur.close()
        conn.close()
        return companyCode[0]

    except Exception as e:
        print(e)

def checkUnusedUsername(username: str):

    try:
        conn = psycopg2.connect(DATABASE_URL, sslmode='require')
        cur = conn.cursor()

        sql = "SELECT username FROM userinfo WHERE username = %s"
        val = [username]

        cur.execute(sql, val)

        username = cur.fetchone()

        cur.close()
        conn.close()

        if username is None:
            return "Continue"
        else:
            return "Failed Check"

    except Exception as e:
        print(e)

def checkUniqueEmail(email):

    try:
        conn = psycopg2.connect(DATABASE_URL, sslmode='require')
        cur = conn.cursor()

        sql = "SELECT count(username) FROM userinfo WHERE email = %s"
        val = [email]

        cur.execute(sql, val)

        count = cur.fetchall()
        cur.close()
        conn.close()
        if count[0][0] == 0:
            return "Continue"
        else:
            return "Failed Check"

    except Exception as e:
        print(e)

def checkEmailExists(email):

    try:
        conn = psycopg2.connect(DATABASE_URL, sslmode='require')
        cur = conn.cursor()

        sql = "SELECT count(username) FROM userinfo WHERE email = %s"
        val = [email]

        cur.execute(sql, val)

        count = cur.fetchall()
        cur.close()
        conn.close()
        if count[0][0] == 1:
            return "Continue"
        else:
            return "Failed Check"

    except Exception as e:
        print(e)


def checkUniqueCompanyName(name: str):
    try:
        conn = psycopg2.connect(DATABASE_URL, sslmode='require')
        cur = conn.cursor()

        sql = "SELECT name FROM companyinfo WHERE name = %s"
        val = [name]

        cur.execute(sql, val)

        name = cur.fetchone()

        cur.close()
        conn.close()

        if name is None:
            return True
        else:
            return False
    except Exception as e:
        print(e)


def checkUniqueCompanyCode(code: str):

    try:
        conn = psycopg2.connect(DATABASE_URL, sslmode='require')
        cur = conn.cursor()

        sql = "SELECT companycode FROM companyinfo WHERE companycode = %s"
        val = [code]

        cur.execute(sql, val)

        code = cur.fetchone()
        cur.close()
        conn.close()

        if code is None:
            return {
                "codeExist": False
            }
        else:
            return {
                "codeExist": True
            }
    except Exception as e:
        raise e


def supplierCompanyInfo(companyCode):
    # SupplierID (abn)
    # SupplierStreet
    # SupplierCity
    # SupplierPost
    # SupplierRegistration (trading name/company name)

    SupplierID = int()
    SupplierStreet = str()
    SupplierCity = str()
    SupplierPost = str()
    SupplierRegistration = str()

    try:
        conn = psycopg2.connect(DATABASE_URL, sslmode='require')
        cur = conn.cursor()

        sql = "SELECT name, abn, street, suburb, postcode FROM companyinfo WHERE companycode = %s"
        val = [companyCode]

        cur.execute(sql, val)

        data = cur.fetchone()
        cur.close()
        conn.close()
        SupplierRegistration = data[0]
        SupplierID = data[1]
        SupplierStreet = data[2]
        SupplierCity = data[3]
        SupplierPost = data[4]

        return {
            "SupplierID": SupplierID,
            "SupplierStreet": SupplierStreet,
            "SupplierCity": SupplierCity,
            "SupplierPost": SupplierPost,
            "SupplierRegistration": SupplierRegistration
        }
    except Exception as e:
        raise e


def customerCompanyInfo(name):
    # CustomerStreet
    # CustomerCity
    # CustomerPost

    CustomerStreet = int()
    CustomerCity = str()
    CustomerPost = str()

    try:
        conn = psycopg2.connect(DATABASE_URL, sslmode='require')
        cur = conn.cursor()

        sql = "SELECT street, suburb, postcode FROM companyinfo WHERE name = %s"
        val = [name]

        cur.execute(sql, val)

        data = cur.fetchone()
        cur.close()
        conn.close()
        if data == None:
            raise Exception(
                description=f"Company Name Error: There is no company with name {name}")
        CustomerStreet = data[0]
        CustomerCity = data[1]
        CustomerPost = data[2]

        return {
            "CustomerStreet": CustomerStreet,
            "CustomerCity": CustomerCity,
            "CustomerPost": CustomerPost
        }
    except Exception as e:
        raise e


def companyCodeFromName(name):
    companyCode = str()
    try:
        conn = psycopg2.connect(DATABASE_URL, sslmode='require')
        cur = conn.cursor()

        sql = "SELECT companycode FROM companyinfo WHERE name = %s"
        val = [name]

        cur.execute(sql, val)

        data = cur.fetchone()
        cur.close()
        conn.close()
        if data == None:
            raise InputError(
                description=f"Company Name Error: There is no company with name {name}")

        companyCode = data[0]
        return {
            'companyCode': companyCode
        }
    except Exception as e:
        raise e


BASE_CREATE_DATA = {
    "UBLID": 2.1,
    "CustomizationID": "urn:cen.eu:en16931:2017#conformant#urn:fdc:peppol.eu:2017:poacc:billing:international:aunz:3.0",
    "ProfileID": "urn:fdc:peppol.eu:2017:poacc:billing:01:1.0",
    "ID": "EBWASP1002",
    "IssueDate": "2022-02-07",
    "InvoiceCode": 380,
    "Currency": "AUD",
    "BuyerReference": "EBWASP1002",
    "AddDocReference": "ebwasp1002",
    "SupplierID": 80647710156,
    "SupplierStreet": "100 Business Street",
    "SupplierCity": "Dulwich Hill",
    "SupplierPost": 2203,
    "SupplierCountry": "AU",
    "SupplierRegistration": "Ebusiness Software Services Pty Ltd",
    "CustomerStreet": "Suite 132 Level 45",
    "CustomerCity": "Homebush West",
    "CustomerPost": "2140",
    "CustomerCountry": "AU",
    "CustomerRegistration": "Awolako Enterprises Pty Ltd",
    "PaymentType": 1,
    "PaymentID": "EBWASP1002",
    "PaymentTerms": "As agreed",
    "TaxAmount": 10,
    "TaxableAmount": 100,
    "TaxSubtotalAmount": 10,
    "TaxID": "GST",
    "TaxPercent": 10,
    "TaxSchemeID": "GST",
    "LegalLineExtension": 100,
    "TaxExclusiveAmount": 100,
    "TaxInclusiveAmount": 110,
    "PayableRoundingAmount": 0,
    "PayableAmount": 110,
    "InvoiceID": 1,
    "InvoiceQuantity": 500,
    "InvoiceLineExtension": 100,
    "InvoiceName": "Pencils",
    "InvoiceTaxID": 5,
    "InvoiceTaxPercent": 10,
    "InvoiceTaxSchemeID": "GST",
    "InvoicePriceAmount": 0.2,
    "InvoiceBaseQuantity": 1
}

if __name__ == '__main__':
    # print(supplierCompanyInfo("oflgxqqbfv"))
    # print(customerCompanyInfo("unsw"))
    print(companyCodeFromName('math'))
