from src.config import DATABASE_URL
import psycopg2

def receiveAndStore(email):

    try:
        conn = psycopg2.connect(DATABASE_URL, sslmode='require')
        cur = conn.cursor()

        sql = "SELECT companycode FROM userinfo WHERE email = %s"
        val = email

        cur.execute(sql, val)

        companyCode = cur.fetchone()

        cur.close()
        conn.close()

        return companyCode[0]

    except Exception as e:
        print(e)


