import psycopg2
from src.config import DATABASE_URL


def check_okay(username: str, company_code: str, function_type: str):
    """given a company_code, and function_type return if the current function can be executed

    Args:
        username (str): the username of the user calling one of the functions
        company_code (str): the file name that the user wants to extract
        function_type (str): either 'store' or 'render'

    Returns:
        str: "Success" or "Fail"

    Exception:
        when connect to db failed
    """
    
    USAGE_LIMIT = 5

    try:
        # Connect to DB
        conn = psycopg2.connect(DATABASE_URL, sslmode='require')

        # Open a cursor for db operations
        cur = conn.cursor()

        if function_type == "store":
            # extract number of files stored with given company_code
            sql = "SELECT count(distinct file_name) FROM invoices WHERE password = %s"
            val = [company_code]
            cur.execute(sql, list(val))
            return_value = cur.fetchone()
            if return_value is not None:
                return_value = return_value[0]

        # Not sure how to do this becuase not sure how renders will be recorded
        else:
            sql = "SELECT sum(numrenders) OVER (partition by companycode) as totalrenders FROM userinfo WHERE companycode = %s"
            val = [company_code]
            cur.execute(sql, list(val))
            return_value = cur.fetchone()
            if return_value is not None:
                return_value = return_value[0]

        # final_return = None

        if return_value >= USAGE_LIMIT:
            # Close DB connection
            cur.close()
            conn.close()
            return "Fail"
            # final_return = 'Fail'
        elif (return_value < USAGE_LIMIT or return_value is None) and function_type == "render":
            sql = "UPDATE users SET numrenders = %s WHERE username = %s and companycode = %s"
            val = [return_value, username, company_code]
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
            return 'Success'
            # final_return = 'Success'

    except Exception as e:
        print(e)

    # finally:
    #     if final_return is not None:
    #         return final_return
    #     else:
    #         return 'success'