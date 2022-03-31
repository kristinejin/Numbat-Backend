from src.config import DATABASE_URL
import psycopg2

def CreateAccount(Username : str, Password: str):
    if not isinstance(Username,str):
        raise InputError("Only Strings Allowed")

    if not isinstance(Password,str):
        raise InputError("Only Strings Allowed")

    #check if valid regex

    #Add username and password to database
    
    try:
        conn = psycopg2.connect(DATABASE_URL, sslmode='require')
        cur = conn.cursor()

        sql = "INSERT INTO userinfo VALUES (%s,%s)"
        val = [Username, Password]
        cur.execute(sql,val)
        conn.commit()
        cur.close()
        conn.close()
        return True

    except Exception as e:
        raise e

def Login(Username : str, Password: str):
    if not isinstance(Username,str):
        raise InputError("Only Strings Allowed")

    if not isinstance(Password,str):
        raise InputError("Only Strings Allowed")

    try:
        conn = psycopg2.connect(DATABASE_URL, sslmode='require')
        cur = conn.cursor()

        sql = "select * from userinfo where username = (%s) and password = (%s)"
        val = (Username,Password)
        cur.execute(sql,val)
        returnvalues = cur.fetchone()
        
        if(returnvalues == None):
            raise Exception("Incorrect Details")

        cur.close()
        conn.close()

        return True

    except Exception as e:
        raise e
    pass

if __name__ == '__main__':
    CreateAccount("TestU2","TestP2")