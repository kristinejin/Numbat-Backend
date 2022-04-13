from src.config import DATABASE_URL
import psycopg2
import re
from src.error import InputError
from src.other import checkUnusedUsername, checkUniqueEmail

COMPANY_CODE_LENGTH = 5
USERNAME_OR_PASSWORD_LENGTH = 12


def CreateAccount(Username: str, Password: str, companycode: str, email: str):
    if not isinstance(Username, str):
        raise InputError(description="Invalid Username: Only Strings Allowed")

    if len(Username) > USERNAME_OR_PASSWORD_LENGTH:
        raise InputError(description="Invalid Username: Must be " + str(USERNAME_OR_PASSWORD_LENGTH) + " characters or less")

    if checkUnusedUsername(Username) == "Failed Check":
        raise InputError(description="Invalid Username: Already In Use")

    if not isinstance(Password, str):
        raise InputError(description="Invalid Password: Only Strings Allowed")

    if len(Password) > USERNAME_OR_PASSWORD_LENGTH:
        raise InputError(description="Invalid Password: Must be " + str(USERNAME_OR_PASSWORD_LENGTH) + " characters or less")

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
        raise InputError(description="Invalid Company Code: Company Code must be " + str(COMPANY_CODE_LENGTH) + " characters or less")

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
            raise Exception(description="Incorrect Details")

        cur.close()
        conn.close()

        return True

    except Exception as e:
        raise e
    pass


if __name__ == "__main__":
    CreateAccount("TestU2", "TestP2", "Code2", "TestE2")
