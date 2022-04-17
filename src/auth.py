from src.config import DATABASE_URL
import psycopg2
import re
from src.error import InputError
from src.other import checkUnusedUsername, checkUniqueEmail, checkUniqueCompanyName, checkUniqueCompanyCode

COMPANY_CODE_LENGTH = 20
USERNAME_OR_PASSWORD_LENGTH = 12


def CreateAccount(Username: str, Password: str, companycode: str, email: str):
    if not isinstance(Username, str):
        raise InputError(description="Invalid Username: Only Strings Allowed")

    if len(Username) > USERNAME_OR_PASSWORD_LENGTH:
        raise InputError(description="Invalid Username: Must be " +
                         str(USERNAME_OR_PASSWORD_LENGTH) + " characters or less")

    if checkUnusedUsername(Username) == "Failed Check":
        raise InputError(description="Invalid Username: Already In Use")

    if not isinstance(Password, str):
        raise InputError(description="Invalid Password: Only Strings Allowed")

    if len(Password) > USERNAME_OR_PASSWORD_LENGTH:
        raise InputError(description="Invalid Password: Must be " +
                         str(USERNAME_OR_PASSWORD_LENGTH) + " characters or less")

    # # check if valid regex
    # if not isinstance(companycode, str):
    #     raise InputError(description="Invalid Company Code: Only Strings Allowed")

    if checkUniqueEmail(email) == "Failed Check":
        raise InputError(description="Invalid Email: Already In Use")

    # Email is valid
    if not re.match(
        r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}$", email
    ):
        raise InputError(
            description="Invalid Email: Does Not Match Standard Regex")

    # if not isinstance(companycode, str):
    #     raise InputError(description="Only Strings Allowed")

    if len(companycode) > COMPANY_CODE_LENGTH:
        raise InputError(description="Invalid Company Code: Company Code must be " +
                         str(COMPANY_CODE_LENGTH) + " characters or less")
    if not checkUniqueCompanyCode(companycode)['codeExist']:
        raise InputError(
            description="Invalid Company Code: Company does not exist")

    # check if company_code is alphanumeric?
    # if not companycode.isalnum():
    #     raise InputError(description="Can only contain alphanumeric characters")

    # Add username, password, companycode and email to database

    try:
        conn = psycopg2.connect(DATABASE_URL, sslmode="require")
        cur = conn.cursor()

        # sql = "INSERT INTO userinfo (username, password, companycode, numrenders, email) VALUES (%s, %s, %s, 0, %s)"
        # val = [Username, Password, companycode, email]
        sql = (
            "INSERT INTO userinfo (username, password, companycode, email) VALUES (%s, %s, %s, %s)"
        )
        val = [Username, Password, companycode, email]
        cur.execute(sql, val)
        conn.commit()
        cur.close()
        conn.close()
        return True

    except Exception as e:
        raise e


def Login(Username: str, Password: str):
    if not isinstance(Username, str):
        raise InputError(description="Only Strings Allowed")

    if not isinstance(Password, str):
        raise InputError(description="Only Strings Allowed")

    try:
        conn = psycopg2.connect(DATABASE_URL, sslmode="require")
        cur = conn.cursor()

        sql = "select * from userinfo where username = (%s) and password = (%s)"
        val = (Username, Password)
        cur.execute(sql, val)
        returnvalues = cur.fetchone()

        if returnvalues == None:
            raise InputError(description="Incorrect Username or Password")

        cur.close()
        conn.close()

        return True

    except Exception as e:
        raise e


def createCompany(name, abn, street, suburb, postcode, companyCode):
    """

    Args:
        name (str): trading name of the company
        abn (str): abn of the company
        street (int/str): street address of the company
        suburb (str): suburb of the company located
        postcode (int/str): postcode of the company located
        companyCode (str): company code of the company

    Raises:
        InputError: _description_
        InputError: _description_
        InputError: _description_
        InputError: _description_
        InputError: _description_
        e: _description_

    Returns:
        _type_: _description_
    """
    if not checkUniqueCompanyName(name):
        raise InputError(
            description="Invalid Company Name/Code: Company name and/or company code have been registered")
    if len(str(abn)) != 11:
        raise InputError(
            description="Invalid ABN: ABN must be an 11 digit integer"
        )
    if len(str(postcode)) != 4:
        raise InputError(
            description="Invalid Postcode: Postcode must be a 4 digit integer"
        )
    if checkUniqueCompanyCode(companyCode)['codeExist']:
        raise InputError(
            description="Invalid Company Name/Code: Company name and/or company code have been registered")
    if len(companyCode) > COMPANY_CODE_LENGTH:
        raise InputError(
            description="Invalid Company Code: Company Code must be " +
            COMPANY_CODE_LENGTH + " characters or less"
        )
    try:
        conn = psycopg2.connect(DATABASE_URL, sslmode="require")
        cur = conn.cursor()

        # sql = "INSERT INTO userinfo (username, password, companycode, numrenders, email) VALUES (%s, %s, %s, 0, %s)"
        # val = [Username, Password, companycode, email]
        sql = (
            "INSERT INTO companyinfo (name, abn, companycode, street, suburb, postcode) VALUES (%s, %s, %s, %s, %s, %s)"
        )
        val = [name, abn, companyCode, street, suburb, postcode]
        cur.execute(sql, val)
        conn.commit()
        cur.close()
        conn.close()
        return {"company_created": True}

    except Exception as e:
        raise e


if __name__ == "__main__":
    # CreateAccount("TestU2", "TestP2", "Code2", "TestE2"))
    pass
