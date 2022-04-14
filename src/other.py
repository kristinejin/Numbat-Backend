from src.config import DATABASE_URL
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

        if username[0] is NULL:
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
        print(count)
        cur.close()
        conn.close()
        if count[0][0] == 1:
            return "Continue"
        else:
            return "Failed Check"

    except Exception as e:
        print(e)
