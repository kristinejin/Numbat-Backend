from src.other import BASE_CREATE_DATA, supplierCompanyInfo
import string
import random


def invoiceCreate(userInput, supplierCompanyCode):
    invoiceDict = BASE_CREATE_DATA
    for k, v in userInput.items():
        if k != 'fileName':
            if k[:-1] == "InvoiceName":
                invoiceDict["InvoiceTaxID" + k[-1]] = 10
                invoiceDict["InvoiceTaxPercent" + k[-1]] = 10
                invoiceDict["InvoiceTaxSchemeID" + k[-1]] = "GST"
                invoiceDict['InvoiceLineExtension' + k[-1]] = int(
                    invoiceDict['InvoiceQuantity'] + k[-1]) * int(invoiceDict['InvoicePriceAmount'] + k[-1])
            invoiceDict[k] = v
    invoiceDict['InvoiceLineExtension'] = int(
        invoiceDict['InvoiceQuantity']) * int(invoiceDict['InvoicePriceAmount'])
    # BuyerReference (caps) = AddDocReference (lowercase) = ID
    invoiceDict["ID"] = ''.join(random.choices(
        string.ascii_uppercase + string.digits, k=10))
    invoiceDict["BuyerReference"] = invoiceDict["ID"]
    invoiceDict["AddDocReference"] = invoiceDict["ID"].lower()
    invoiceDict['PaymentID'] = invoiceDict["ID"]

    # SupplierID (abn)
    # SupplierStreet
    # SupplierCity
    # SupplierPost
    # SupplierRegistration (trading name/company name)
    supplierInfo = supplierCompanyInfo(supplierCompanyCode)
    for k, v in supplierInfo.items():
        invoiceDict[k] = v

    # CustomerStreet
    # CustomerCity
    # CustomerPost
    # customerInfo = customerCompanyInfo(invoiceDict["CustomerRegistration"])
    # for k, v in customerInfo.items():
    #     invoiceDict[k] = v

    # TaxSubtotalAmount = TaxableAmount * 0.10
    # TaxInclusiveAmount = TaxableAmount + TaxSubtotalAmount
    # LegalLineExtension = TaxExclusiveAmount = TaxableAmount
    invoiceDict["TaxSubtotalAmount"] = int(
        invoiceDict["PayableAmount"]) - int(invoiceDict["TaxableAmount"])
    invoiceDict["TaxInclusiveAmount"] = invoiceDict["PayableAmount"]
    invoiceDict["LegalLineExtension"] = invoiceDict["TaxableAmount"]
    invoiceDict["TaxExclusiveAmount"] = invoiceDict["TaxableAmount"]
    invoiceDict["TaxAmount"] = invoiceDict["TaxSubtotalAmount"]
    return invoiceDict
