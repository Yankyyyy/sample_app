#Basic soap request

import frappe
import json
import requests



@frappe.whitelist()
def cancel_pickup(doc, method):
    """CancelPickup api"""
    doc_json = json.dumps(doc.__dict__)
    url = "https://ws.dev.aramex.net/ShippingAPI.V2/Shipping/Service_1_0.svc"

    cancel_pickup_dictionary = {

        "ClientInfo": {
            "UserName": "string",
            "Password": "string",
            "Version": "string",
            "AccountNumber": "string",
            "AccountPin": "string",
            "AccountEntity": "string",
            "AccountCountryCode": "string",
            "Source": "100",
            "PreferredLanguageCode": "string"

        },

        "Transaction": {
            "Reference1": "string",
            "Reference2": "string",
            "Reference3": "string",
            "Reference4": "string",
            "Reference5": "string"
        },
        "PickupGUID" : "string",
        "Comments" : "string"
    }

    payload = f"""<?xml version="1.0" encoding="utf-8"?>
            <soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">
            <soap:Body>
                <PickupCancelationRequest xmlns="http://ws.aramex.net/ShippingAPI/v1/">
                <ClientInfo>
                    <UserName>string</UserName>
                    <Password>string</Password>
                    <Version>string</Version>
                    <AccountNumber>string</AccountNumber>
                    <AccountPin>string</AccountPin>
                    <AccountEntity>string</AccountEntity>
                    <AccountCountryCode>string</AccountCountryCode>
                    <Source>100</Source>
                    <PreferredLanguageCode>string</PreferredLanguageCode>
                </ClientInfo>
                <Transaction>
                    <Reference1>string</Reference1>
                    <Reference2>string</Reference2>
                    <Reference3>string</Reference3>
                    <Reference4>string</Reference4>
                    <Reference5>string</Reference5>
                </Transaction>
                <PickupGUID>string</PickupGUID>
                <Comments>string</Comments>
                </PickupCancelationRequest>
            </soap:Body>
            </soap:Envelope>"""
    headers = {
	'Content-Type': 'text/xml; charset=utf-8',
    'SOAPAction':'http://ws.aramex.net/ShippingAPI/v1/Service_1_0/CancelPickup'
    }
    response = requests.request("POST", url, headers=headers, data=payload)
    print(response.text)
    print(response)
    frappe.msgprint((f'Its Done!! The SOAP API is called.'));