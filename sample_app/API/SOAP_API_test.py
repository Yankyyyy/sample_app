import frappe
import requests
import xml, logging
from SOAPpy import WSDL
from suds.client import Client



@frappe.whitelist()
def print_label(doc, method):
    logging.basicConfig(level=logging.INFO)
    logging.getLogger('suds.client').setLevel(logging.DEBUG)
    WSDLFile = "https://ws.dev.aramex.net/ShippingAPI.V2/Shipping/Service_1_0.svc?singleWsdl"

    client = Client(WSDLFile)
    #proxy = WSDL.Proxy(WSDLFile)
    #uncomment thoses lines to see outgoing and incoming soap envelops
    #proxy.soapserver.config.dumpSOAPIn=1
    #proxy.soapserver.config.dumpSOAPOut=1

    #print(proxy.methods.keys())

    client.sd[0].service.setlocation('https://ws.dev.aramex.net/shippingapi/shipping/service_1_0.svc')

    clientobj = client.factory.create('ClientInfo')
    clientobj.UserName = 'testingapi@aramex.com'
    clientobj.Password = 'R123456789$r'
    clientobj.Version = 'v1.0'
    clientobj.AccountNumber = '20016'
    clientobj.AccountPin = '331421'
    clientobj.AccountEntity = 'AMM'
    clientobj.AccountCountryCode = 'JO'
    clientobj.PreferredLanguageCode = 'EN'

    transactionobj = client.factory.create('Transaction')
    transactionobj.Reference1 = doc.name
    transactionobj.Reference2 = ''
    transactionobj.Reference3 = ''
    transactionobj.Reference4 = ''
    transactionobj.Reference5 = ''

    labelinfoobj = client.factory.create('LabelInfo')
    labelinfoobj.ReportID = '9201'
    labelinfoobj.ReportType = 'WSDLFile'


    # headers = {
	# 'Content-Type': 'text/xml; charset=utf-8',
    # 'SOAPAction':'http://ws.aramex.net/ShippingAPI/v1/Service_1_0/CancelPickup'
    # }
    # response = requests.request("POST", url, headers=headers, data=payload)
    # print(response.text)
    # print(response)

    print(client.service.PrintLabel(clientobj,transactionobj,"001","EXP","",labelinfoobj))
    print("Great Job man. You just sent a massage using SOAP API!")
    frappe.msgprint((f'Its Done!! The SOAP API is called.'));