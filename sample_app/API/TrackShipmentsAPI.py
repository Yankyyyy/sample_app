import frappe
import json
import requests
from bs4 import BeautifulSoup

@frappe.whitelist()
def track_shipments(doc, method):
    pick_up_address_doc = frappe.get_doc("Address", doc.pickup_address_name)
    delivery_address_doc = frappe.get_doc("Address", doc.delivery_address_name)
    
    url = "https://ws.aramex.net/shippingapi.v2/tracking/service_1_0.svc"
    
    track_shipments_dictionary = {

        "ClientInfo": {
            "UserName": "armx.ruh.it@gmail.com",
            "Password": "YUre@9982",
            "Version": "1.0",
            "AccountNumber": "4004636",
            "AccountPin": "442543",
            "AccountEntity": "RUH",
            "AccountCountryCode": "SA",
            "Source": "100",
            "PreferredLanguageCode": "EN"
        },

        "Transaction": {
            "Reference1": "001",
            "Reference2": "string",
            "Reference3": "string",
            "Reference4": "string",
            "Reference5": "string"
        },

        "Shipments": {
            "Shipment" : {
                "Reference1": "string",
                "Shipper": {
                    "Reference1": "Ref 111111",
                    "Reference2": "Ref 222222",
                    "AccountNumber": "4004636",
                    "PartyAddress": {
                        "Line1": pick_up_address_doc.address_line1,
                        "Line2": pick_up_address_doc.address_line2,
                        "City": pick_up_address_doc.city,
                        "StateOrProvinceCode": "string",
                        "PostCode": pick_up_address_doc.pincode,
                        "CountryCode": "SA"
                    },
                    "Contact": {
                        "PersonName": doc.pickup_contact_person,
                        "Title": "string",
                        "CompanyName": doc.pickup_company,
                        "PhoneNumber1": "5555555",
                        "PhoneNumber1Ext": "125",
                        "CellPhone": pick_up_address_doc.phone,
                        "EmailAddress": pick_up_address_doc.email_id
                    }
                },
                "Consignee" : {
                    "Reference1" : "string",
                    "Reference2" : "string",
                    "AccountNumber" : "",
                    "PartyAddress": {
                        "Line1": delivery_address_doc.address_line1,
                        "Line2": delivery_address_doc.address_line2,
                        "City": delivery_address_doc.city,
                        "StateOrProvinceCode": "string",
                        "PostCode": delivery_address_doc.pincode,
                        "CountryCode": "SA"
                    },
                    "Contact": {
                        "PersonName": "Michael",
                        "Title": "string",
                        "CompanyName": doc.delivery_company,
                        "PhoneNumber1": "5555555",
                        "PhoneNumber1Ext": "125",
                        "CellPhone": delivery_address_doc.phone,
                        "EmailAddress": delivery_address_doc.email_id
                    }
                },
                "ShippingDateTime" : doc.pickup_date,
                "Details" : {
                    "ActualWeight" : {
                        "Unit" : "KG",
                        "Value" : "93"
                    },
                    "DescriptionOfGoods" : "string",
                    "GoodsOriginCountry" : "SA",
                    "NumberOfPieces" : "100",
                    "ProductGroup" : "DOM",
                    "ProductType" : "OND",
                    "PaymentType" : "P",
                },
                "ForeignHAWB" : "ABC 000111",
            }          
        },
        
        "GetLastTrackingUpdateOnly" : "1",
        
        "LabelInfo" : {
            "ReportID" : "9201",
            "ReportType" : "URL"
        }
    }
    
    payload = f"""<?xml version="1.0" encoding="utf-8"?>
            <soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">
            <soap:Body>
                <ShipmentTrackingRequest xmlns="http://ws.aramex.net/ShippingAPI/v1/">
                    <ClientInfo>
                        <UserName>{track_shipments_dictionary["ClientInfo"]["UserName"]}</UserName>
                        <Password>{track_shipments_dictionary["ClientInfo"]["Password"]}</Password>
                        <Version>{track_shipments_dictionary["ClientInfo"]["Version"]}</Version>
                        <AccountNumber>{track_shipments_dictionary["ClientInfo"]["AccountNumber"]}</AccountNumber>
                        <AccountPin>{track_shipments_dictionary["ClientInfo"]["AccountPin"]}</AccountPin>
                        <AccountEntity>{track_shipments_dictionary["ClientInfo"]["AccountEntity"]}</AccountEntity>
                        <AccountCountryCode>{track_shipments_dictionary["ClientInfo"]["AccountCountryCode"]}</AccountCountryCode>
                        <Source>{track_shipments_dictionary["ClientInfo"]["Source"]}</Source>
                        <PreferredLanguageCode>{track_shipments_dictionary["ClientInfo"]["PreferredLanguageCode"]}</PreferredLanguageCode>
                    </ClientInfo>
                    <Transaction>
                        <Reference1>{track_shipments_dictionary["Transaction"]["Reference1"]}</Reference1>
                        <Reference2>{track_shipments_dictionary["Transaction"]["Reference2"]}</Reference2>
                        <Reference3>{track_shipments_dictionary["Transaction"]["Reference3"]}</Reference3>
                        <Reference4>{track_shipments_dictionary["Transaction"]["Reference4"]}</Reference4>
                        <Reference5>{track_shipments_dictionary["Transaction"]["Reference5"]}</Reference5>
                    </Transaction>
                    <Shipments>
                        <Shipment>
                            <Reference1>{track_shipments_dictionary["Shipments"]["Shipment"]["Reference1"]}</Reference1>
                            <Shipper>
                                <Reference1>{track_shipments_dictionary["Shipments"]["Shipment"]["Shipper"]["Reference1"]}</Reference1>
                                <Reference2>{track_shipments_dictionary["Shipments"]["Shipment"]["Shipper"]["Reference2"]}</Reference2>
                                <AccountNumber>{track_shipments_dictionary["Shipments"]["Shipment"]["Shipper"]["AccountNumber"]}</AccountNumber>
                                <PartyAddress>
                                    <Line1>{track_shipments_dictionary["Shipments"]["Shipment"]["Shipper"]["PartyAddress"]["Line1"]}</Line1>
                                    <Line2>{track_shipments_dictionary["Shipments"]["Shipment"]["Shipper"]["PartyAddress"]["Line2"]}</Line2>
                                    <City>{track_shipments_dictionary["Shipments"]["Shipment"]["Shipper"]["PartyAddress"]["City"]}</City>
                                    <StateOrProvinceCode>{track_shipments_dictionary["Shipments"]["Shipment"]["Shipper"]["PartyAddress"]["StateOrProvinceCode"]}</StateOrProvinceCode>
                                    <PostCode>{track_shipments_dictionary["Shipments"]["Shipment"]["Shipper"]["PartyAddress"]["PostCode"]}</PostCode>
                                    <CountryCode>{track_shipments_dictionary["Shipments"]["Shipment"]["Shipper"]["PartyAddress"]["CountryCode"]}</CountryCode>
                                </PartyAddress>
                                <Contact>
                                    <PersonName>{track_shipments_dictionary["Shipments"]["Shipment"]["Shipper"]["Contact"]["PersonName"]}</PersonName>
                                    <Title>{track_shipments_dictionary["Shipments"]["Shipment"]["Shipper"]["Contact"]["Title"]}</Title>
                                    <CompanyName>{track_shipments_dictionary["Shipments"]["Shipment"]["Shipper"]["Contact"]["CompanyName"]}</CompanyName>
                                    <PhoneNumber1>{track_shipments_dictionary["Shipments"]["Shipment"]["Shipper"]["Contact"]["PhoneNumber1"]}</PhoneNumber1>
                                    <PhoneNumber1Ext>{track_shipments_dictionary["Shipments"]["Shipment"]["Shipper"]["Contact"]["PhoneNumber1Ext"]}</PhoneNumber1Ext>
                                    <CellPhone>{track_shipments_dictionary["Shipments"]["Shipment"]["Shipper"]["Contact"]["CellPhone"]}</CellPhone>
                                    <EmailAddress>{track_shipments_dictionary["Shipments"]["Shipment"]["Shipper"]["Contact"]["EmailAddress"]}</EmailAddress>
                                </Contact>
                            </Shipper>
                            <Consignee>
                                <Reference1>{track_shipments_dictionary["Shipments"]["Shipment"]["Consignee"]["Reference1"]}</Reference1>
                                <Reference2>{track_shipments_dictionary["Shipments"]["Shipment"]["Consignee"]["Reference2"]}</Reference2>
                                <AccountNumber>{track_shipments_dictionary["Shipments"]["Shipment"]["Consignee"]["AccountNumber"]}</AccountNumber>
                                <PartyAddress>
                                    <Line1>{track_shipments_dictionary["Shipments"]["Shipment"]["Consignee"]["PartyAddress"]["Line1"]}</Line1>
                                    <Line2>{track_shipments_dictionary["Shipments"]["Shipment"]["Consignee"]["PartyAddress"]["Line2"]}</Line2>
                                    <City>{track_shipments_dictionary["Shipments"]["Shipment"]["Consignee"]["PartyAddress"]["City"]}</City>
                                    <StateOrProvinceCode>{track_shipments_dictionary["Shipments"]["Shipment"]["Consignee"]["PartyAddress"]["StateOrProvinceCode"]}</StateOrProvinceCode>
                                    <PostCode>{track_shipments_dictionary["Shipments"]["Shipment"]["Consignee"]["PartyAddress"]["PostCode"]}</PostCode>
                                    <CountryCode>{track_shipments_dictionary["Shipments"]["Shipment"]["Consignee"]["PartyAddress"]["CountryCode"]}</CountryCode>
                                </PartyAddress>
                                <Contact>
                                    <PersonName>{track_shipments_dictionary["Shipments"]["Shipment"]["Consignee"]["Contact"]["PersonName"]}</PersonName>
                                    <Title>{track_shipments_dictionary["Shipments"]["Shipment"]["Consignee"]["Contact"]["Title"]}</Title>
                                    <CompanyName>{track_shipments_dictionary["Shipments"]["Shipment"]["Consignee"]["Contact"]["CompanyName"]}</CompanyName>
                                    <PhoneNumber1>{track_shipments_dictionary["Shipments"]["Shipment"]["Consignee"]["Contact"]["PhoneNumber1"]}</PhoneNumber1>
                                    <PhoneNumber1Ext>{track_shipments_dictionary["Shipments"]["Shipment"]["Consignee"]["Contact"]["PhoneNumber1Ext"]}</PhoneNumber1Ext>
                                    <CellPhone>{track_shipments_dictionary["Shipments"]["Shipment"]["Consignee"]["Contact"]["CellPhone"]}</CellPhone>
                                    <EmailAddress>{track_shipments_dictionary["Shipments"]["Shipment"]["Consignee"]["Contact"]["EmailAddress"]}</EmailAddress>
                                </Contact>
                            </Consignee>
                            <ShippingDateTime>{track_shipments_dictionary["Shipments"]["Shipment"]["ShippingDateTime"]}</ShippingDateTime>
                            <Details>
                                <ActualWeight>
                                    <Unit>{track_shipments_dictionary["Shipments"]["Shipment"]["Details"]["ActualWeight"]["Unit"]}</Unit>
                                    <Value>{track_shipments_dictionary["Shipments"]["Shipment"]["Details"]["ActualWeight"]["Value"]}</Value>
                                </ActualWeight>
                                <DescriptionOfGoods>{track_shipments_dictionary["Shipments"]["Shipment"]["Details"]["DescriptionOfGoods"]}</DescriptionOfGoods>
                                <GoodsOriginCountry>{track_shipments_dictionary["Shipments"]["Shipment"]["Details"]["GoodsOriginCountry"]}</GoodsOriginCountry>
                                <NumberOfPieces>{track_shipments_dictionary["Shipments"]["Shipment"]["Details"]["NumberOfPieces"]}</NumberOfPieces>
                                <ProductGroup>{track_shipments_dictionary["Shipments"]["Shipment"]["Details"]["ProductGroup"]}</ProductGroup>
                                <ProductType>{track_shipments_dictionary["Shipments"]["Shipment"]["Details"]["ProductType"]}</ProductType>
                                <PaymentType>{track_shipments_dictionary["Shipments"]["Shipment"]["Details"]["PaymentType"]}</PaymentType>
                            </Details>
                            <ForeignHAWB>{track_shipments_dictionary["Shipments"]["Shipment"]["ForeignHAWB"]}</ForeignHAWB>
                        </Shipment>
                    </Shipments>
                    <GetLastTrackingUpdateOnly>{track_shipments_dictionary["GetLastTrackingUpdateOnly"]}</GetLastTrackingUpdateOnly>
                    <LabelInfo>
                        <ReportID>{track_shipments_dictionary["LabelInfo"]["ReportID"]}</ReportID>
                        <ReportType>{track_shipments_dictionary["LabelInfo"]["ReportType"]}</ReportType>
                    </LabelInfo>
                </ShipmentTrackingRequest>
            </soap:Body>
            </soap:Envelope>"""
    headers = {
	'Content-Type': 'text/xml; charset=utf-8',
    'SOAPAction':'http://ws.aramex.net/ShippingAPI/v1/Service_1_0/TrackShipments'
    }
    response = requests.request("POST", url, headers=headers, data=payload)
    print(response.text)
    print(response)
    frappe.msgprint((f'Its Done!! The SOAP API is called.'));