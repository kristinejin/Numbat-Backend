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


def auth_passwordreset_request_base(email):
    """
    Given an email address, if the user is a registered user,
    sends them an email containing a specific secret code, that
    when entered in auth/passwordreset/reset, shows that the user
    trying to reset the password is the one who got sent this email.
    No error should be raised when passed an invalid email, as that
    would pose a security/privacy concern. When a user requests a
    password reset, they should be logged out of all current sessions.

    Args:
        email (str): the email of the user to be given a reset code

    Returns:
        dict: empty
    """

    # generate a random 5 digit code to send to the user
    reset_code = random.randint(10000, 99999)

    # only send the reset code if the email belongs to a user
    if (checkUniqueEmail(email) == "Continue"):

        user = [user for user in store["users"] if user["email"] == email["email"]]

        # send the code via email
        sender = "" ###############################################################################
        receivers = [email]
        body_of_email = "This is your password reset code: " + str(reset_code)

        msg = MIMEText(body_of_email, "html")
        msg["Subject"] = "Numbat E-invoice Solutions account reset code"
        msg["From"] = sender
        msg["To"] = ",".join(receivers)

        s = smtplib.SMTP_SSL(host="smtp.gmail.com", port=465)
        ########################################################################################
        s.login(user="streams.team22@gmail.com", password="Seaniscool")
        s.sendmail(sender, receivers, msg.as_string())
        s.quit()

        # store only the most recent reset code
        try:
            conn = psycopg2.connect(DATABASE_URL, sslmode='require')
            cur = conn.cursor()

            sql = "INSERT INTO reset_codes (email, code) VALUES (%s, %s)" 
            val = [email, reset_code]

            cur.execute(sql, val)
            cur.close()
            conn.close()

        except Exception as e:
            print(e)

        # # Remove all active sessions that belong to the user
        # store["active_sessions"] = [
        #     session
        #     for session in store["active_sessions"]
        #     if session["auth_user_id"] != user[0]["u_id"]
        # ]

    return "Reset Code has been sent"

# Create table reset_codes (
# email text,
# code int
# ):

def auth_passwordreset_reset_base(reset_code, new_password):
    """
    Given a reset code for a user, set that user's new password to the password provided.

    Args:
        reset_code (str): The code that was supplied to the user to reset their password
        new_password (str): The new password for the user

    Raises:
        InputError: reset_code is invalid
        InputError: the length of the new password is less than 6
    """

    # check for valid reset code
    try:
        reset_code = int(reset_code)
    except ValueError as e:
        raise InputError(description="Invalid password reset code") from e

    if reset_code not in store["reset_codes"].values():
        raise InputError(description="Invalid password reset code")
    # check for valid password length
    if len(new_password) > PASSWORD_LENGTH:
        raise InputError(description="Password cannot be more than " + PASSWORD_LENGTH + " characters")

    try:
        conn = psycopg2.connect(DATABASE_URL, sslmode='require')
        cur = conn.cursor()

        sql = "select email from reset_codes where code = %s)" 
        val = [reset_code]

        cur.execute(sql, val)
        email = cur.fetchall()
        cur.close()
        conn.close()

    except Exception as e:
        print(e)

    if email[0] is not None:
        try:
            conn = psycopg2.connect(DATABASE_URL, sslmode='require')
            cur = conn.cursor()

            sql = "Update userinfo set password = %s where email = %s" 
            val = [password, email]

            cur.execute(sql, val)
            
            sql = "Delete from reset_codes where code = %s"
            val = [email]

            cur.execute(sql, val)

            cur.close()
            conn.close()

        except Exception as e:
            print(e)

    return "Password Reset Successfully"


if __name__ == "__main__":
    # CreateAccount("TestU2", "TestP2", "Code2", "TestE2"))
    pass
