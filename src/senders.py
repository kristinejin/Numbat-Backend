from src.error import InputError
from src.config import DATABASE_URL
from src.other import companyCodeFromName
import psycopg2


def addSender(receiverCompanyCode, senderName):
    addSenderStatus = True
    senderCompanyCode = companyCodeFromName(senderName)['companyCode']
    if checkSenderAccess(receiverCompanyCode, senderCompanyCode)['isAuthorised']:
        raise InputError(
            description=f"Cannot add {senderName}: This sender have already been authorised")
    try:
        conn = psycopg2.connect(DATABASE_URL, sslmode="require")
        cur = conn.cursor()

        sql = (
            "INSERT INTO senders (owner, sender) VALUES (%s, %s)"
        )
        val = [receiverCompanyCode, senderCompanyCode]
        cur.execute(sql, val)
        conn.commit()
        cur.close()
        conn.close()
        return {
            'addSenderStatus': addSenderStatus
        }

    except Exception as e:
        raise e


def removeSender(receiverCompanyCode, senderName):
    removeSenderStatus = True
    senderCompanyCode = companyCodeFromName(senderName)['companyCode']
    if not checkSenderAccess(receiverCompanyCode, senderCompanyCode)['isAuthorised']:
        raise InputError(
            description=f"Cannot remove {senderName}: No sender with name {senderName} has been authorised")
    try:
        conn = psycopg2.connect(DATABASE_URL, sslmode="require")
        cur = conn.cursor()

        sql = (
            "DELETE FROM senders WHERE (owner = %s AND sender = %s)"
        )
        val = [receiverCompanyCode, senderCompanyCode]
        cur.execute(sql, val)
        conn.commit()
        cur.close()
        conn.close()
        return {
            'removeSenderStatus': removeSenderStatus
        }

    except Exception as e:
        raise e


def checkSenderAccess(receiverCompanyCode, senderCompanyCode):
    try:
        conn = psycopg2.connect(DATABASE_URL, sslmode="require")
        cur = conn.cursor()

        sql = (
            "SELECT owner, sender FROM senders WHERE (owner = %s AND sender = %s)"
        )
        val = [receiverCompanyCode, senderCompanyCode]
        cur.execute(sql, val)
        data = cur.fetchone()
        cur.close()
        conn.close()
        if data == None:
            return {
                'isAuthorised': False
            }
        if data[0] == receiverCompanyCode and data[1] == senderCompanyCode:
            return {
                'isAuthorised': True
            }
        else:
            return {
                'isAuthorised': False
            }
    except Exception as e:
        raise e


# if __name__ == '__main__':
    #print(addSender('math', 'unsw'))
    #print(checkSenderAccess('oflgxqqbfv', 'math'))
    #removeSender('math', 'unsw')
