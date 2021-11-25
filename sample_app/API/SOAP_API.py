import frappe
import requests

@frappe.whitelist()
def cancel_pickup(doc, method):
    print("*************************************SOAP API called****************************************")
    url = "https://ws.dev.aramex.net/ShippingAPI.V2/Shipping/Service_1_0.svc"
    
    payload = """<?xml version="1.0" encoding="utf-8"?>
            <soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">
            <soap:Body>
                <PickupCancelationRequest xmlns="http://ws.aramex.net/ShippingAPI/v1/">
                <ClientInfo>
                    <UserName>doc.name</UserName>
                    <Password>YUre@9982</Password>
                    <Version>1.0</Version>
                    <AccountNumber>4004636</AccountNumber>
                    <AccountPin>442543</AccountPin>
                    <AccountEntity>RUH</AccountEntity>
                    <AccountCountryCode>SA</AccountCountryCode>
                    <Source>100</Source>
                    <PreferredLanguageCode>EN</PreferredLanguageCode>
                </ClientInfo>
                <Transaction>
                    <Reference1>{}</Reference1>
                    <Reference2>string</Reference2>
                    <Reference3>string</Reference3>
                    <Reference4>string</Reference4>
                    <Reference5>string</Reference5>
                </Transaction>
                <PickupGUID>string</PickupGUID>
                <Comments>string</Comments>
                </PickupCancelationRequest>
            </soap:Body>
            </soap:Envelope>""".format(doc.name)
    headers = {
	'Content-Type': 'text/xml; charset=utf-8',
    'SOAPAction':'http://ws.aramex.net/ShippingAPI/v1/Service_1_0/CancelPickup'
    }
    response = requests.request("POST", url, headers=headers, data=payload)
    print(response.text)
    print(response)
    frappe.msgprint((f'Its Done!! The SOAP API is called.'));