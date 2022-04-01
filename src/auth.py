from src.config import DATABASE_URL
import psycopg2
import re
from src.error import InputError

CODE_LENGTH = 5

# def CreateAccount(Username : str, Password: str, companycode: str, email: str):
def CreateAccount(Username : str, Password: str, companycode: str):
    if not isinstance(Username,str):
        raise InputError(description="Only Strings Allowed")

    if not isinstance(Password,str):
        raise InputError(description="Only Strings Allowed")

    #check if valid regex
    if not isinstance(companycode, str):
        raise InputError(description="Only Strings Allowed")
    
    # Email is valid
    # if not re.match(
    #     r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}$", email
    # ):  
    #     raise InputError(description="Invalid Email Provided")


    if not isinstance(companycode, str):
        raise InputError(description="Only Strings Allowed")
    
    if (len(companycode) > CODE_LENGTH):
        raise InputError(description="companycode can not exceed " + CODE_LENGTH + " characters in length")

    # check if company_code is alphanumeric?
    # if not companycode.isalnum():
    #     raise InputError(description="Can only contain alphanumeric characters")

    #Add username, password, companycode and email to database
    
    try:
        conn = psycopg2.connect(DATABASE_URL, sslmode='require')
        cur = conn.cursor()

        # sql = "INSERT INTO userinfo (username, password, companycode, numrenders, email) VALUES (%s, %s, %s, 0, %s)"
        # val = [Username, Password, companycode, email]
        sql = "INSERT INTO userinfo (username, password, companycode) VALUES (%s, %s, %s)"
        val = [Username, Password, companycode]
        cur.execute(sql, val)
        conn.commit()
        cur.close()
        conn.close()
        return True

    except Exception as e:
        raise e

def Login(Username : str, Password: str):
    if not isinstance(Username,str):
        raise InputError(description="Only Strings Allowed")

    if not isinstance(Password,str):
        raise InputError(description="Only Strings Allowed")

    try:
        conn = psycopg2.connect(DATABASE_URL, sslmode='require')
        cur = conn.cursor()

        sql = "select * from userinfo where username = (%s) and password = (%s)"
        val = (Username,Password)
        cur.execute(sql,val)
        returnvalues = cur.fetchone()
        
        if(returnvalues == None):
            raise Exception(description="Incorrect Details")

        cur.close()
        conn.close()

        return True

    except Exception as e:
        raise e
    pass

if __name__ == '__main__':
    CreateAccount("TestU2", "TestP2", "Code2", "TestE2")