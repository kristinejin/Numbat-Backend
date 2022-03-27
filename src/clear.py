from src.config import DATABASE_URL
import psycopg2

def clear(ListOfUsernanames : list):
    if not isinstance(ListOfUsernanames,list):
        raise InputError("Clear function only accepts list")

    try:
        conn = psycopg2.connect(DATABASE_URL, sslmode='require')
        cur = conn.cursor()

        #Query
        sql = "Delete from userinfo where username = %s"

        #Delete all the files
        for Username in ListOfUsernanames:
            val = (Username)
            cur.execute(sql,[val])
        
        conn.commit()
        cur.close()
        conn.close()

    except Exception as e:
        raise e