import frappe
import json
import requests
from bs4 import BeautifulSoup

@frappe.whitelist()
def create_shipment(doc): 
    doc = json.loads(doc)
    pick_up_address_doc = frappe.get_doc("Address", doc.get("pickup_address_name"))
    delivery_address_doc = frappe.get_doc("Address", doc.get("delivery_address_name"))

    url = "https://ws.aramex.net/shippingapi.v2/shipping/service_1_0.svc"
    
    payload = f"""<?xml version="1.0" encoding="utf-8"?>
            <soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">
            <soap:Body>
                <ShipmentCreationRequest xmlns="http://ws.aramex.net/ShippingAPI/v1/">
                    <ClientInfo>
                        <UserName>{"armx.ruh.it@gmail.com"}</UserName>
                        <Password>{"YUre@9982"}</Password>
                        <Version>{"1.0"}</Version>
                        <AccountNumber>{"4004636"}</AccountNumber>
                        <AccountPin>{"442543"}</AccountPin>
                        <AccountEntity>{"RUH"}</AccountEntity>
                        <AccountCountryCode>{"SA"}</AccountCountryCode>
                        <Source>{"100"}</Source>
                    </ClientInfo>
                    <Transaction>
                        <Reference1>{"001"}</Reference1>
                        <Reference2>string</Reference2>
                        <Reference3>string</Reference3>
                        <Reference4>string</Reference4>
                        <Reference5>string</Reference5>
                    </Transaction>
                    <Shipments>
                        <Shipment>
                            <Reference1>string</Reference1>
                            <Shipper>
                                <Reference1>{"Ref 111111"}</Reference1>
                                <AccountNumber>{"4004636"}</AccountNumber>
                                <PartyAddress>
                                    <Line1>{pick_up_address_doc.address_line1}</Line1>
                                    <Line2>{pick_up_address_doc.address_line2}</Line2>
                                    <City>{pick_up_address_doc.city}</City>
                                    <StateOrProvinceCode>string</StateOrProvinceCode>
                                    <PostCode>{pick_up_address_doc.pincode}</PostCode>
                                    <CountryCode>{"SA"}</CountryCode>
                                </PartyAddress>
                                <Contact>
                                    <PersonName>{doc.get("pickup_contact_person")}</PersonName>
                                    <CompanyName>{doc.get("pickup_company")}</CompanyName>
                                    <PhoneNumber1>{"5555555"}</PhoneNumber1>
                                    <CellPhone>{pick_up_address_doc.phone}</CellPhone>
                                    <EmailAddress>{pick_up_address_doc.email_id}</EmailAddress>
                                </Contact>
                            </Shipper>
                            <Consignee>
                                <Reference1>string</Reference1>
                                <AccountNumber>{"4004636"}</AccountNumber>
                                <PartyAddress>
                                    <Line1>{delivery_address_doc.address_line1}</Line1>
                                    <Line2>{delivery_address_doc.address_line2}</Line2>
                                    <City>{delivery_address_doc.city}</City>
                                    <StateOrProvinceCode>string</StateOrProvinceCode>
                                    <PostCode>{delivery_address_doc.pincode}</PostCode>
                                    <CountryCode>{"SA"}</CountryCode>
                                </PartyAddress>
                                <Contact>
                                    <PersonName>{"Michael"}</PersonName>
                                    <CompanyName>{doc.get("delivery_company")}</CompanyName>
                                    <PhoneNumber1>{"5555555"}</PhoneNumber1>
                                    <CellPhone>{delivery_address_doc.phone}</CellPhone>
                                    <EmailAddress>{delivery_address_doc.email_id}</EmailAddress>
                                </Contact>
                            </Consignee>
                            <ShippingDateTime>{doc.get("pickup_date")}</ShippingDateTime>
                            <Details>
                                <ActualWeight>
                                    <Unit>{"KG"}</Unit>
                                    <Value>{"20"}</Value>
                                </ActualWeight>
                                <DescriptionOfGoods>string</DescriptionOfGoods>
                                <GoodsOriginCountry>{"SA"}</GoodsOriginCountry>
                                <NumberOfPieces>{"20"}</NumberOfPieces>
                                <ProductGroup>{"DOM"}</ProductGroup>
                                <ProductType>{"OND"}</ProductType>
                                <PaymentType>{"P"}</PaymentType>
                            </Details>
                            <ForeignHAWB>{"ABC 000111"}</ForeignHAWB>
                        </Shipment>
                    </Shipments>
                </ShipmentCreationRequest>
            </soap:Body>
            </soap:Envelope>"""
    headers = {
	'Content-Type': 'text/xml; charset=utf-8',
    'SOAPAction':'http://ws.aramex.net/ShippingAPI/v1/Service_1_0/CreateShipments'
    }
    response = requests.request("POST", url, headers=headers, data=payload)
    print(response)
    print ("***********************************Hy Suresh")

    frappe.msgprint((f'Its Done!! The SOAP API is called.'));

    # if response.status_code == 200:
    #     response_xml = BeautifulSoup(response.text, 'xml')
        
    #     if response_xml.find('Code').text != "ID":
    #         shipment_id = response_xml.find('ID').text 
    #         doc.shipment_id = shipment_id
    #         doc.save(ignore_permissions=True)
    #         frappe.db.commit()
    # else:
    #     pass