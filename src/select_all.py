from src.config import DATABASE_URL
import psycopg2

def selectAll(companycode: str):

    try:
        conn = psycopg2.connect(DATABASE_URL, sslmode="require")
        cur = conn.cursor()

        sql = (
            "select id1, file_name, issue_date, sender_name, buyer_name, amount_payable, tax_payable, goods_payable from invoices where password = %s"
        )
        # sql = (
        #     "select id1, file_name, issue_date, sender_name from invoices where password = %s"
        # )
        val = [companycode]
        cur.execute(sql, val)
        retVal = cur.fetchall()

        invoices = []
        for invoice in retVal:
            invoices.append({"id": invoice[0], "file_name": invoice[1], "issue_date": str(invoice[2]), "sender_name": invoice[3], "buyer_name": invoice[4], "amount_payable": str(invoice[5]), "tax_payable": str(invoice[6]), "goods_payable": str(invoice[7])})
        cur.close()
        conn.close()

        return invoices

    except Exception as e:
        raise e
