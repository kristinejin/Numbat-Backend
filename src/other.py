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

        if username is None:
            return "Continue"
        else:
            return "Failed Check"

    except Exception as e:
        print(e)


def checkUniqueEmail(email: str):

    try:
        conn = psycopg2.connect(DATABASE_URL, sslmode='require')
        cur = conn.cursor()

        sql = "SELECT username FROM userinfo WHERE email = %s"
        val = [email]

        cur.execute(sql, val)

        email = cur.fetchone()

        cur.close()
        conn.close()

        if email is None:
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
        print(code)
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
        print(f"error is {e}")

# if __name__ == '__main__':
#     checkUniqueCompanyCode('randomcompanycode')
