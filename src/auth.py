from test.error import DuplicateFileError, WrongPassword
from src.config import DATABASE_URL

def CreateAccount(Username : str, Password: str):
    if not isinstance(Username,str):
        raise InputError("Only Strings Allowed")

    if not isinstance(Password,str):
        raise InputError("Only Strings Allowed")

    #check if valid regex

    #Check if UserName alrd exist
    try:
        conn = psycopg2.connect(DATABASE_URL, sslmode='require')
    except Exception as e:
        raise e

    #Add username and password to database

    pass