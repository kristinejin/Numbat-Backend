import psycopg2
from src.config import DATABASE_URL


def checkQuota(username: str, companyCode: str, funcType: str):
    """given a companyCode, and funcType return if the current function can be executed

    Args:
        username (str): the username of the user calling one of the functions
        companyCode (str): the file name that the user wants to extract
        funcType (str): either 'store' or 'render'

    Returns:
        str: "Success" or "Fail"

    Exception:
        when connect to db failed
    """

    USAGE_LIMIT = 5

    try:
        # Connect to DB
        conn = psycopg2.connect(DATABASE_URL, sslmode="require")

        # Open a cursor for db operations
        cur = conn.cursor()

        if funcType == "store":
            # extract number of files stored with given companyCode
            sql = "SELECT count(distinct file_name) FROM invoices WHERE password = %s"
            val = [companyCode]
            cur.execute(sql, list(val))
            retVal = cur.fetchone()
            if retVal is not None:
                retVal = retVal[0]

        # Not sure how to do this becuase not sure how renders will be recorded
        else:
            sql = "SELECT sum(numrenders) OVER (partition by companycode) as totalrenders FROM userinfo WHERE companycode = %s"
            val = [companyCode]
            cur.execute(sql, list(val))
            retVal = cur.fetchone()
            if retVal is not None:
                retVal = retVal[0]

        # final_return = None

        if retVal >= USAGE_LIMIT:
            # Close DB connection
            cur.close()
            conn.close()
            return "Fail"
            # final_return = 'Fail'
        elif (retVal < USAGE_LIMIT) and funcType == "render":
            retVal += 1
            sql = "UPDATE userinfo SET numrenders = %s WHERE companycode = %s"
            val = [retVal, companyCode]
            cur.execute(sql, val)
            # Close DB connection
            conn.commit()
            cur.close()
            conn.close()
            return "Success"
            # final_return = 'Success'
        else:
            # Close DB connection
            cur.close()
            conn.close()
            return "Success"
            # final_return = 'Success'

    except Exception as e:
        # print(e)
        return e
