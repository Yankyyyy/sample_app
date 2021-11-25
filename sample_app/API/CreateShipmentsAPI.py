import frappe
import json
import requests


@frappe.whitelist()
def create_shipments(doc, method):
    shipment_doc = frappe.get_doc("Shipment", "SHIPMENT-00001")
    pick_up_address_doc = frappe.get_doc("Address", shipment_doc.pickup_address_name)
    delivery_address_doc = frappe.get_doc("Address", shipment_doc.delivery_address_name)

    url = "https://ws.aramex.net/shippingapi.v2/shipping/service_1_0.svc"
    
    create_shipment_dictionary = {

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
                "Reference2": "string",
                "Reference3": "string",
                "Shipper": {
                    "Reference1": "Ref 111111",
                    "Reference2": "Ref 222222",
                    "AccountNumber": "4004636",
                    "PartyAddress": {
                        "Line1": pick_up_address_doc.address_line1,
                        "Line2": pick_up_address_doc.address_line2,
                        "Line3": "string",
                        "City": pick_up_address_doc.city,
                        "StateOrProvinceCode": "string",
                        "PostCode": pick_up_address_doc.pincode,
                        "CountryCode": "SA",
                        "Longitude": "66",
                        "Latitude": "54",
                        "BuildingNumber": "string",
                        "BuildingName": pick_up_address_doc.address_title,
                        "Floor": "string",
                        "Apartment": "string",
                        "POBox": "string",
                        "Description": "string"
                    },
                    "Contact": {
                        "Department": "string",
                        "PersonName": shipment_doc.pickup_contact_person,
                        "Title": "string",
                        "CompanyName": shipment_doc.pickup_company,
                        "PhoneNumber1": "5555555",
                        "PhoneNumber1Ext": "125",
                        "PhoneNumber2": "string",
                        "PhoneNumber2Ext": "string",
                        "FaxNumber": "string",
                        "CellPhone": pick_up_address_doc.phone,
                        "EmailAddress": pick_up_address_doc.email_id,
                        "Type": pick_up_address_doc.address_type
                    }
                },
                "Consignee" : {
                    "Reference1" : "string",
                    "Reference2" : "string",
                    "AccountNumber" : "string",
                    "PartyAddress": {
                        "Line1": delivery_address_doc.address_line1,
                        "Line2": delivery_address_doc.address_line2,
                        "Line3": "string",
                        "City": delivery_address_doc.city,
                        "StateOrProvinceCode": "string",
                        "PostCode": delivery_address_doc.pincode,
                        "CountryCode": "SA",
                        "Longitude": "66",
                        "Latitude": "54",
                        "BuildingNumber": "string",
                        "BuildingName": delivery_address_doc.address_title,
                        "Floor": "string",
                        "Apartment": "string",
                        "POBox": "string",
                        "Description": "string"
                    },
                    "Contact": {
                        "Department": "string",
                        "PersonName": "Michael",
                        "Title": "string",
                        "CompanyName": shipment_doc.delivery_company,
                        "PhoneNumber1": "5555555",
                        "PhoneNumber1Ext": "125",
                        "PhoneNumber2": "string",
                        "PhoneNumber2Ext": "string",
                        "FaxNumber": "string",
                        "CellPhone": delivery_address_doc.phone,
                        "EmailAddress": delivery_address_doc.email_id,
                        "Type": delivery_address_doc.address_type
                    }
                },
                "ThirdParty" : {
                    "Reference1" : "string",
                    "Reference2" : "string",
                    "AccountNumber" : "string",
                    "PartyAddress" : {
                        "Line1" : "Mecca St",
                        "Line2" : "string",
                        "Line3" : "string",
                        "City" : "Amman",
                        "StateOrProvinceCode" : "string",
                        "PostCode" : "string",
                        "CountryCode" : "JO",
                        "Longitude" : "66",
                        "Latitude" : "54",
                        "BuildingNumber" : "string",
                        "BuildingName" : "string",
                        "Floor" : "string",
                        "Apartment" : "string",
                        "POBox" : "string",
                        "Description" : "string"
                    },
                    "Contact" : {
                        "Department": "string",
                        "PersonName": "Michael",
                        "Title": "string",
                        "CompanyName": "Aramex",
                        "PhoneNumber1": "5555555",
                        "PhoneNumber1Ext": "125",
                        "PhoneNumber2": "string",
                        "PhoneNumber2Ext": "string",
                        "FaxNumber": "string",
                        "CellPhone": "07777777",
                        "EmailAddress": "michael@aramex.com",
                        "Type": "string"
                    }                
                },
                "ShippingDateTime" : shipment_doc.pickup_date,
                "DueDate" : "2021-11-16T08:16:08.058Z",
                "Comments" : shipment_doc.description_of_content,
                "PickupLocation" : shipment_doc.pickup_address_name,
                "OperationsInstructions" : "string",
                "AccountingInstructions" : "string",
                "Details" : {
                    "Dimensions" : {
                        "Length" : "81",
                        "Width" : "57",
                        "Height" : "40",
                        "Unit" : "CM"
                    },
                    "ActualWeight" : {
                        "Unit" : "KG",
                        "Value" : "93"
                    },
                    "ChargeableWeight" : {
                        "Unit" : "string",
                        "Value" : "26"
                    },
                    "DescriptionOfGoods" : "string",
                    "GoodsOriginCountry" : "SA",
                    "NumberOfPieces" : "100",
                    "ProductGroup" : "DOM",
                    "ProductType" : "string",
                    "PaymentType" : "P",
                    "PaymentOptions" : "string",
                    "CustomsValueAmount" : {
                        "CurrencyCode" : "USD",
                        "Value" : "11"
                    },
                    "CashOnDeliveryAmount" : {
                        "CurrencyCode" : "USD",
                        "Value" : "33"
                    },
                    "InsuranceAmount" : {
                        "CurrencyCode" : "USD",
                        "Value" : "41"
                    },
                    "CashAdditionalAmount" : {
                        "CurrencyCode" : "USD",
                        "Value" : "19"
                    },
                    "CashAdditionalAmountDescription" : "string",
                    "CollectAmount" : {
                        "CurrencyCode" : "USD",
                        "Value" : "18"
                    },
                    "Services" : "string",
                    "Items" : {
                        "ShipmentItem" : {
                            "PackageType" : "string",
                            "Quantity" : "100",
                            "Weight" : {
                                "Unit" : "KG",
                                "Value" : "47"
                            },
                            "Comments" : "string",
                            "Reference" : "string",
                            "PiecesDimensions" : {
                                "Dimensions" : {
                                    "Length" : "65",
                                    "Width" : "14",
                                    "Height" : "97",
                                    "Unit" : "M"
                                }
                            },
                            "CommodityCode" : "string",
                            "GoodsDescription" : "string",
                            "CountryOfOrigin" : "SA",
                            "CustomsValue" : {
                                "CurrencyCode" : "USD",
                                "Value" : "7" 
                            },
                            "ContainerNumber" : "string"                  

                        }
                    },
                    "DeliveryInstructions" : {
                        "Option" : "string",
                        "Reference" : "string"
                    },
                    "AdditionalProperties" : {
                        "AdditionalProperty" : {
                            "CategoryName" : "string",
                            "Name" : "string",
                            "Value" : "string"
                        }
                    },
                    "ContainsDangerousGoods" : "true"

                },
                "Attachments" : {
                    "Attachment" : {
                        "FileName" : "string",
                        "FileExtension" : "string",
                        "FileContents" : "Y29udGVudA=="
                    }
                },
                "ForeignHAWB" : "ABC 000111",
                "TransportType_x0020_" : "1",
                "PickupGUID" : "string",
                "Number" : "string", 
                "ScheduledDelivery" : {
                    "PreferredDeliveryDate" : "2021-11-16T08:16:08.058Z",
                    "PreferredDeliveryTimeFrame_x0020_" : "string",
                    "PreferredDeliveryTime" : "string"
                }
            }          
        },
        "LabelInfo" : {
            "ReportID" : "9201",
            "ReportType" : "URL"
        }
    }
    
    payload = f"""<?xml version="1.0" encoding="utf-8"?>
            <soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">
            <soap:Body>
                <ShipmentCreationRequest xmlns="http://ws.aramex.net/ShippingAPI/v1/">
                <ClientInfo>
                        <UserName>{create_shipment_dictionary["ClientInfo"]["UserName"]}</UserName>
                        <Password>{create_shipment_dictionary["ClientInfo"]["Password"]}</Password>
                        <Version>{create_shipment_dictionary["ClientInfo"]["Version"]}</Version>
                        <AccountNumber>{create_shipment_dictionary["ClientInfo"]["AccountNumber"]}</AccountNumber>
                        <AccountPin>{create_shipment_dictionary["ClientInfo"]["AccountPin"]}</AccountPin>
                        <AccountEntity>{create_shipment_dictionary["ClientInfo"]["AccountEntity"]}</AccountEntity>
                        <AccountCountryCode>{create_shipment_dictionary["ClientInfo"]["AccountCountryCode"]}</AccountCountryCode>
                        <Source>{create_shipment_dictionary["ClientInfo"]["Source"]}</Source>
                        <PreferredLanguageCode>{create_shipment_dictionary["ClientInfo"]["PreferredLanguageCode"]}</PreferredLanguageCode>
                    </ClientInfo>
                    <Transaction>
                        <Reference1>{create_shipment_dictionary["Transaction"]["Reference1"]}</Reference1>
                        <Reference2>{create_shipment_dictionary["Transaction"]["Reference2"]}</Reference2>
                        <Reference3>{create_shipment_dictionary["Transaction"]["Reference3"]}</Reference3>
                        <Reference4>{create_shipment_dictionary["Transaction"]["Reference4"]}</Reference4>
                        <Reference5>{create_shipment_dictionary["Transaction"]["Reference5"]}</Reference5>
                    </Transaction>
                    <Shipments>
                        <Shipment>
                            <Reference1>{create_shipment_dictionary["Shipments"]["Shipment"]["Reference1"]}</Reference1>
                            <Reference2>{create_shipment_dictionary["Shipments"]["Shipment"]["Reference2"]}</Reference2>
                            <Reference3>{create_shipment_dictionary["Shipments"]["Shipment"]["Reference3"]}</Reference3>
                            <Shipper>
                                <Reference1>{create_shipment_dictionary["Shipments"]["Shipment"]["Shipper"]["Reference1"]}</Reference1>
                                <Reference2>{create_shipment_dictionary["Shipments"]["Shipment"]["Shipper"]["Reference2"]}</Reference2>
                                <AccountNumber>{create_shipment_dictionary["Shipments"]["Shipment"]["Shipper"]["AccountNumber"]}</AccountNumber>
                                <PartyAddress>
                                    <Line1>{create_shipment_dictionary["Shipments"]["Shipment"]["Shipper"]["PartyAddress"]["Line1"]}</Line1>
                                    <Line2>{create_shipment_dictionary["Shipments"]["Shipment"]["Shipper"]["PartyAddress"]["Line2"]}</Line2>
                                    <Line3>{create_shipment_dictionary["Shipments"]["Shipment"]["Shipper"]["PartyAddress"]["Line3"]}</Line3>
                                    <City>{create_shipment_dictionary["Shipments"]["Shipment"]["Shipper"]["PartyAddress"]["City"]}</City>
                                    <StateOrProvinceCode>{create_shipment_dictionary["Shipments"]["Shipment"]["Shipper"]["PartyAddress"]["StateOrProvinceCode"]}</StateOrProvinceCode>
                                    <PostCode>{create_shipment_dictionary["Shipments"]["Shipment"]["Shipper"]["PartyAddress"]["PostCode"]}</PostCode>
                                    <CountryCode>{create_shipment_dictionary["Shipments"]["Shipment"]["Shipper"]["PartyAddress"]["CountryCode"]}</CountryCode>
                                    <Longitude>{create_shipment_dictionary["Shipments"]["Shipment"]["Shipper"]["PartyAddress"]["Longitude"]}</Longitude>
                                    <Latitude>{create_shipment_dictionary["Shipments"]["Shipment"]["Shipper"]["PartyAddress"]["Latitude"]}</Latitude>
                                    <BuildingNumber>{create_shipment_dictionary["Shipments"]["Shipment"]["Shipper"]["PartyAddress"]["BuildingNumber"]}</BuildingNumber>
                                    <BuildingName>{create_shipment_dictionary["Shipments"]["Shipment"]["Shipper"]["PartyAddress"]["BuildingName"]}</BuildingName>
                                    <Floor>{create_shipment_dictionary["Shipments"]["Shipment"]["Shipper"]["PartyAddress"]["Floor"]}</Floor>
                                    <Apartment>{create_shipment_dictionary["Shipments"]["Shipment"]["Shipper"]["PartyAddress"]["Apartment"]}</Apartment>
                                    <POBox>{create_shipment_dictionary["Shipments"]["Shipment"]["Shipper"]["PartyAddress"]["POBox"]}</POBox>
                                    <Description>{create_shipment_dictionary["Shipments"]["Shipment"]["Shipper"]["PartyAddress"]["Description"]}</Description>
                                </PartyAddress>
                                <Contact>
                                    <Department>{create_shipment_dictionary["Shipments"]["Shipment"]["Shipper"]["Contact"]["Department"]}</Department>
                                    <PersonName>{create_shipment_dictionary["Shipments"]["Shipment"]["Shipper"]["Contact"]["PersonName"]}</PersonName>
                                    <Title>{create_shipment_dictionary["Shipments"]["Shipment"]["Shipper"]["Contact"]["Title"]}</Title>
                                    <CompanyName>{create_shipment_dictionary["Shipments"]["Shipment"]["Shipper"]["Contact"]["CompanyName"]}</CompanyName>
                                    <PhoneNumber1>{create_shipment_dictionary["Shipments"]["Shipment"]["Shipper"]["Contact"]["PhoneNumber1"]}</PhoneNumber1>
                                    <PhoneNumber1Ext>{create_shipment_dictionary["Shipments"]["Shipment"]["Shipper"]["Contact"]["PhoneNumber1Ext"]}</PhoneNumber1Ext>
                                    <PhoneNumber2>{create_shipment_dictionary["Shipments"]["Shipment"]["Shipper"]["Contact"]["PhoneNumber2"]}</PhoneNumber2>
                                    <PhoneNumber2Ext>{create_shipment_dictionary["Shipments"]["Shipment"]["Shipper"]["Contact"]["PhoneNumber2Ext"]}</PhoneNumber2Ext>
                                    <FaxNumber>{create_shipment_dictionary["Shipments"]["Shipment"]["Shipper"]["Contact"]["FaxNumber"]}</FaxNumber>
                                    <CellPhone>{create_shipment_dictionary["Shipments"]["Shipment"]["Shipper"]["Contact"]["CellPhone"]}</CellPhone>
                                    <EmailAddress>{create_shipment_dictionary["Shipments"]["Shipment"]["Shipper"]["Contact"]["EmailAddress"]}</EmailAddress>
                                    <Type>{create_shipment_dictionary["Shipments"]["Shipment"]["Shipper"]["Contact"]["Type"]}</Type>
                                </Contact>
                            </Shipper>
                            <Consignee>
                                <Reference1>{create_shipment_dictionary["Shipments"]["Shipment"]["Consignee"]["Reference1"]}</Reference1>
                                <Reference2>{create_shipment_dictionary["Shipments"]["Shipment"]["Consignee"]["Reference2"]}</Reference2>
                                <AccountNumber>{create_shipment_dictionary["Shipments"]["Shipment"]["Consignee"]["AccountNumber"]}</AccountNumber>
                                <PartyAddress>
                                    <Line1>{create_shipment_dictionary["Shipments"]["Shipment"]["Consignee"]["PartyAddress"]["Line1"]}</Line1>
                                    <Line2>{create_shipment_dictionary["Shipments"]["Shipment"]["Consignee"]["PartyAddress"]["Line2"]}</Line2>
                                    <Line3>{create_shipment_dictionary["Shipments"]["Shipment"]["Consignee"]["PartyAddress"]["Line3"]}</Line3>
                                    <City>{create_shipment_dictionary["Shipments"]["Shipment"]["Consignee"]["PartyAddress"]["City"]}</City>
                                    <StateOrProvinceCode>{create_shipment_dictionary["Shipments"]["Shipment"]["Consignee"]["PartyAddress"]["StateOrProvinceCode"]}</StateOrProvinceCode>
                                    <PostCode>{create_shipment_dictionary["Shipments"]["Shipment"]["Consignee"]["PartyAddress"]["PostCode"]}</PostCode>
                                    <CountryCode>{create_shipment_dictionary["Shipments"]["Shipment"]["Consignee"]["PartyAddress"]["CountryCode"]}</CountryCode>
                                    <Longitude>{create_shipment_dictionary["Shipments"]["Shipment"]["Consignee"]["PartyAddress"]["Longitude"]}</Longitude>
                                    <Latitude>{create_shipment_dictionary["Shipments"]["Shipment"]["Consignee"]["PartyAddress"]["Latitude"]}</Latitude>
                                    <BuildingNumber>{create_shipment_dictionary["Shipments"]["Shipment"]["Consignee"]["PartyAddress"]["BuildingNumber"]}</BuildingNumber>
                                    <BuildingName>{create_shipment_dictionary["Shipments"]["Shipment"]["Consignee"]["PartyAddress"]["BuildingName"]}</BuildingName>
                                    <Floor>{create_shipment_dictionary["Shipments"]["Shipment"]["Consignee"]["PartyAddress"]["Floor"]}</Floor>
                                    <Apartment>{create_shipment_dictionary["Shipments"]["Shipment"]["Consignee"]["PartyAddress"]["Apartment"]}</Apartment>
                                    <POBox>{create_shipment_dictionary["Shipments"]["Shipment"]["Consignee"]["PartyAddress"]["POBox"]}</POBox>
                                    <Description>{create_shipment_dictionary["Shipments"]["Shipment"]["Consignee"]["PartyAddress"]["Description"]}</Description>
                                </PartyAddress>
                                <Contact>
                                    <Department>{create_shipment_dictionary["Shipments"]["Shipment"]["Consignee"]["Contact"]["Department"]}</Department>
                                    <PersonName>{create_shipment_dictionary["Shipments"]["Shipment"]["Consignee"]["Contact"]["PersonName"]}</PersonName>
                                    <Title>{create_shipment_dictionary["Shipments"]["Shipment"]["Consignee"]["Contact"]["Title"]}</Title>
                                    <CompanyName>{create_shipment_dictionary["Shipments"]["Shipment"]["Consignee"]["Contact"]["CompanyName"]}</CompanyName>
                                    <PhoneNumber1>{create_shipment_dictionary["Shipments"]["Shipment"]["Consignee"]["Contact"]["PhoneNumber1"]}</PhoneNumber1>
                                    <PhoneNumber1Ext>{create_shipment_dictionary["Shipments"]["Shipment"]["Consignee"]["Contact"]["PhoneNumber1Ext"]}</PhoneNumber1Ext>
                                    <PhoneNumber2>{create_shipment_dictionary["Shipments"]["Shipment"]["Consignee"]["Contact"]["PhoneNumber2"]}</PhoneNumber2>
                                    <PhoneNumber2Ext>{create_shipment_dictionary["Shipments"]["Shipment"]["Consignee"]["Contact"]["PhoneNumber2Ext"]}</PhoneNumber2Ext>
                                    <FaxNumber>{create_shipment_dictionary["Shipments"]["Shipment"]["Consignee"]["Contact"]["FaxNumber"]}</FaxNumber>
                                    <CellPhone>{create_shipment_dictionary["Shipments"]["Shipment"]["Consignee"]["Contact"]["CellPhone"]}</CellPhone>
                                    <EmailAddress>{create_shipment_dictionary["Shipments"]["Shipment"]["Consignee"]["Contact"]["EmailAddress"]}</EmailAddress>
                                    <Type>{create_shipment_dictionary["Shipments"]["Shipment"]["Consignee"]["Contact"]["Type"]}</Type>
                                </Contact>
                            </Consignee>
                            <ThirdParty>
                                <Reference1>{create_shipment_dictionary["Shipments"]["Shipment"]["ThirdParty"]["Reference1"]}</Reference1>
                                <Reference2>{create_shipment_dictionary["Shipments"]["Shipment"]["ThirdParty"]["Reference2"]}</Reference2>
                                <AccountNumber>{create_shipment_dictionary["Shipments"]["Shipment"]["ThirdParty"]["AccountNumber"]}</AccountNumber>
                                <PartyAddress>
                                    <Line1>{create_shipment_dictionary["Shipments"]["Shipment"]["ThirdParty"]["PartyAddress"]["Line1"]}</Line1>
                                    <Line2>{create_shipment_dictionary["Shipments"]["Shipment"]["ThirdParty"]["PartyAddress"]["Line2"]}</Line2>
                                    <Line3>{create_shipment_dictionary["Shipments"]["Shipment"]["ThirdParty"]["PartyAddress"]["Line3"]}</Line3>
                                    <City>{create_shipment_dictionary["Shipments"]["Shipment"]["ThirdParty"]["PartyAddress"]["City"]}</City>
                                    <StateOrProvinceCode>{create_shipment_dictionary["Shipments"]["Shipment"]["ThirdParty"]["PartyAddress"]["StateOrProvinceCode"]}</StateOrProvinceCode>
                                    <PostCode>{create_shipment_dictionary["Shipments"]["Shipment"]["ThirdParty"]["PartyAddress"]["PostCode"]}</PostCode>
                                    <CountryCode>{create_shipment_dictionary["Shipments"]["Shipment"]["ThirdParty"]["PartyAddress"]["CountryCode"]}</CountryCode>
                                    <Longitude>{create_shipment_dictionary["Shipments"]["Shipment"]["ThirdParty"]["PartyAddress"]["Longitude"]}</Longitude>
                                    <Latitude>{create_shipment_dictionary["Shipments"]["Shipment"]["ThirdParty"]["PartyAddress"]["Latitude"]}</Latitude>
                                    <BuildingNumber>{create_shipment_dictionary["Shipments"]["Shipment"]["ThirdParty"]["PartyAddress"]["BuildingNumber"]}</BuildingNumber>
                                    <BuildingName>{create_shipment_dictionary["Shipments"]["Shipment"]["ThirdParty"]["PartyAddress"]["BuildingName"]}</BuildingName>
                                    <Floor>{create_shipment_dictionary["Shipments"]["Shipment"]["ThirdParty"]["PartyAddress"]["Floor"]}</Floor>
                                    <Apartment>{create_shipment_dictionary["Shipments"]["Shipment"]["ThirdParty"]["PartyAddress"]["Apartment"]}</Apartment>
                                    <POBox>{create_shipment_dictionary["Shipments"]["Shipment"]["ThirdParty"]["PartyAddress"]["POBox"]}</POBox>
                                    <Description>{create_shipment_dictionary["Shipments"]["Shipment"]["ThirdParty"]["PartyAddress"]["Description"]}</Description>
                                </PartyAddress>
                                <Contact>
                                    <Department>{create_shipment_dictionary["Shipments"]["Shipment"]["ThirdParty"]["Contact"]["Department"]}</Department>
                                    <PersonName>{create_shipment_dictionary["Shipments"]["Shipment"]["ThirdParty"]["Contact"]["PersonName"]}</PersonName>
                                    <Title>{create_shipment_dictionary["Shipments"]["Shipment"]["ThirdParty"]["Contact"]["Title"]}</Title>
                                    <CompanyName>{create_shipment_dictionary["Shipments"]["Shipment"]["ThirdParty"]["Contact"]["CompanyName"]}</CompanyName>
                                    <PhoneNumber1>{create_shipment_dictionary["Shipments"]["Shipment"]["ThirdParty"]["Contact"]["PhoneNumber1"]}</PhoneNumber1>
                                    <PhoneNumber1Ext>{create_shipment_dictionary["Shipments"]["Shipment"]["ThirdParty"]["Contact"]["PhoneNumber1Ext"]}</PhoneNumber1Ext>
                                    <PhoneNumber2>{create_shipment_dictionary["Shipments"]["Shipment"]["ThirdParty"]["Contact"]["PhoneNumber2"]}</PhoneNumber2>
                                    <PhoneNumber2Ext>{create_shipment_dictionary["Shipments"]["Shipment"]["ThirdParty"]["Contact"]["PhoneNumber2Ext"]}</PhoneNumber2Ext>
                                    <FaxNumber>{create_shipment_dictionary["Shipments"]["Shipment"]["ThirdParty"]["Contact"]["FaxNumber"]}</FaxNumber>
                                    <CellPhone>{create_shipment_dictionary["Shipments"]["Shipment"]["ThirdParty"]["Contact"]["CellPhone"]}</CellPhone>
                                    <EmailAddress>{create_shipment_dictionary["Shipments"]["Shipment"]["ThirdParty"]["Contact"]["EmailAddress"]}</EmailAddress>
                                    <Type>{create_shipment_dictionary["Shipments"]["Shipment"]["ThirdParty"]["Contact"]["Type"]}</Type>
                                </Contact>
                            </ThirdParty>
                            <ShippingDateTime>{create_shipment_dictionary["Shipments"]["Shipment"]["ShippingDateTime"]}</ShippingDateTime>
                            <DueDate>{create_shipment_dictionary["Shipments"]["Shipment"]["DueDate"]}</DueDate>
                            <Comments>{create_shipment_dictionary["Shipments"]["Shipment"]["Comments"]}</Comments>
                            <PickupLocation>{create_shipment_dictionary["Shipments"]["Shipment"]["PickupLocation"]}</PickupLocation>
                            <OperationsInstructions>{create_shipment_dictionary["Shipments"]["Shipment"]["OperationsInstructions"]}</OperationsInstructions>
                            <AccountingInstructions>{create_shipment_dictionary["Shipments"]["Shipment"]["AccountingInstructions"]}</AccountingInstructions>
                            <Details>
                                <Dimensions>
                                    <Length>{create_shipment_dictionary["Shipments"]["Shipment"]["Details"]["Dimensions"]["Length"]}</Length>
                                    <Width>{create_shipment_dictionary["Shipments"]["Shipment"]["Details"]["Dimensions"]["Width"]}</Width>
                                    <Height>{create_shipment_dictionary["Shipments"]["Shipment"]["Details"]["Dimensions"]["Height"]}</Height>
                                    <Unit>{create_shipment_dictionary["Shipments"]["Shipment"]["Details"]["Dimensions"]["Unit"]}</Unit>
                                </Dimensions>
                                <ActualWeight>
                                    <Unit>{create_shipment_dictionary["Shipments"]["Shipment"]["Details"]["ActualWeight"]["Unit"]}</Unit>
                                    <Value>{create_shipment_dictionary["Shipments"]["Shipment"]["Details"]["ActualWeight"]["Value"]}</Value>
                                </ActualWeight>
                                <ChargeableWeight>
                                    <Unit>{create_shipment_dictionary["Shipments"]["Shipment"]["Details"]["ChargeableWeight"]["Unit"]}</Unit>
                                    <Value>{create_shipment_dictionary["Shipments"]["Shipment"]["Details"]["ChargeableWeight"]["Value"]}</Value>
                                </ChargeableWeight>
                                <DescriptionOfGoods>{create_shipment_dictionary["Shipments"]["Shipment"]["Details"]["DescriptionOfGoods"]}</DescriptionOfGoods>
                                <GoodsOriginCountry>{create_shipment_dictionary["Shipments"]["Shipment"]["Details"]["GoodsOriginCountry"]}</GoodsOriginCountry>
                                <NumberOfPieces>{create_shipment_dictionary["Shipments"]["Shipment"]["Details"]["NumberOfPieces"]}</NumberOfPieces>
                                <ProductGroup>{create_shipment_dictionary["Shipments"]["Shipment"]["Details"]["ProductGroup"]}</ProductGroup>
                                <ProductType>{create_shipment_dictionary["Shipments"]["Shipment"]["Details"]["ProductType"]}</ProductType>
                                <PaymentType>{create_shipment_dictionary["Shipments"]["Shipment"]["Details"]["PaymentType"]}</PaymentType>
                                <PaymentOptions>{create_shipment_dictionary["Shipments"]["Shipment"]["Details"]["PaymentOptions"]}</PaymentOptions>
                                <CustomsValueAmount>
                                    <CurrencyCode>{create_shipment_dictionary["Shipments"]["Shipment"]["Details"]["CustomsValueAmount"]["CurrencyCode"]}</CurrencyCode>
                                    <Value>{create_shipment_dictionary["Shipments"]["Shipment"]["Details"]["CustomsValueAmount"]["Value"]}</Value>
                                </CustomsValueAmount>
                                <CashOnDeliveryAmount>
                                    <CurrencyCode>{create_shipment_dictionary["Shipments"]["Shipment"]["Details"]["CashOnDeliveryAmount"]["CurrencyCode"]}</CurrencyCode>
                                    <Value>{create_shipment_dictionary["Shipments"]["Shipment"]["Details"]["CashOnDeliveryAmount"]["Value"]}</Value>
                                </CashOnDeliveryAmount>
                                <InsuranceAmount>
                                    <CurrencyCode>{create_shipment_dictionary["Shipments"]["Shipment"]["Details"]["InsuranceAmount"]["CurrencyCode"]}</CurrencyCode>
                                    <Value>{create_shipment_dictionary["Shipments"]["Shipment"]["Details"]["InsuranceAmount"]["Value"]}</Value>
                                </InsuranceAmount>
                                <CashAdditionalAmount>
                                    <CurrencyCode>{create_shipment_dictionary["Shipments"]["Shipment"]["Details"]["CashAdditionalAmount"]["CurrencyCode"]}</CurrencyCode>
                                    <Value>{create_shipment_dictionary["Shipments"]["Shipment"]["Details"]["CashAdditionalAmount"]["Value"]}</Value>
                                </CashAdditionalAmount>
                                <CashAdditionalAmountDescription>{create_shipment_dictionary["Shipments"]["Shipment"]["Details"]["CashAdditionalAmountDescription"]}</CashAdditionalAmountDescription>
                                <CollectAmount>
                                    <CurrencyCode>{create_shipment_dictionary["Shipments"]["Shipment"]["Details"]["CollectAmount"]["CurrencyCode"]}</CurrencyCode>
                                    <Value>{create_shipment_dictionary["Shipments"]["Shipment"]["Details"]["CollectAmount"]["Value"]}</Value>
                                </CollectAmount>
                                <Services>{create_shipment_dictionary["Shipments"]["Shipment"]["Details"]["Services"]}</Services>
                                <Items>
                                    <ShipmentItem>
                                        <PackageType>{create_shipment_dictionary["Shipments"]["Shipment"]["Details"]["Items"]["ShipmentItem"]["PackageType"]}</PackageType>
                                        <Quantity>{create_shipment_dictionary["Shipments"]["Shipment"]["Details"]["Items"]["ShipmentItem"]["Quantity"]}</Quantity>
                                        <Weight>
                                            <Unit>{create_shipment_dictionary["Shipments"]["Shipment"]["Details"]["Items"]["ShipmentItem"]["Weight"]["Unit"]}</Unit>
                                            <Value>{create_shipment_dictionary["Shipments"]["Shipment"]["Details"]["Items"]["ShipmentItem"]["Weight"]["Value"]}</Value>
                                        </Weight>
                                        <Comments>{create_shipment_dictionary["Shipments"]["Shipment"]["Details"]["Items"]["ShipmentItem"]["Comments"]}</Comments>
                                        <Reference>{create_shipment_dictionary["Shipments"]["Shipment"]["Details"]["Items"]["ShipmentItem"]["Reference"]}</Reference>
                                        <PiecesDimensions>
                                            <Dimensions>
                                                <Length>{create_shipment_dictionary["Shipments"]["Shipment"]["Details"]["Items"]["ShipmentItem"]["PiecesDimensions"]["Dimensions"]["Length"]}</Length>
                                                <Width>{create_shipment_dictionary["Shipments"]["Shipment"]["Details"]["Items"]["ShipmentItem"]["PiecesDimensions"]["Dimensions"]["Width"]}</Width>
                                                <Height>{create_shipment_dictionary["Shipments"]["Shipment"]["Details"]["Items"]["ShipmentItem"]["PiecesDimensions"]["Dimensions"]["Height"]}</Height>
                                                <Unit>{create_shipment_dictionary["Shipments"]["Shipment"]["Details"]["Items"]["ShipmentItem"]["PiecesDimensions"]["Dimensions"]["Unit"]}</Unit>
                                            </Dimensions>
                                        </PiecesDimensions>
                                        <CommodityCode>{create_shipment_dictionary["Shipments"]["Shipment"]["Details"]["Items"]["ShipmentItem"]["CommodityCode"]}</CommodityCode>
                                        <GoodsDescription>{create_shipment_dictionary["Shipments"]["Shipment"]["Details"]["Items"]["ShipmentItem"]["GoodsDescription"]}</GoodsDescription>
                                        <CountryOfOrigin>{create_shipment_dictionary["Shipments"]["Shipment"]["Details"]["Items"]["ShipmentItem"]["CountryOfOrigin"]}</CountryOfOrigin>
                                        <CustomsValue>
                                            <CurrencyCode>{create_shipment_dictionary["Shipments"]["Shipment"]["Details"]["Items"]["ShipmentItem"]["CustomsValue"]["CurrencyCode"]}</CurrencyCode>
                                            <Value>{create_shipment_dictionary["Shipments"]["Shipment"]["Details"]["Items"]["ShipmentItem"]["CustomsValue"]["Value"]}</Value>
                                        </CustomsValue>
                                        <ContainerNumber>{create_shipment_dictionary["Shipments"]["Shipment"]["Details"]["Items"]["ShipmentItem"]["ContainerNumber"]}</ContainerNumber>
                                    </ShipmentItem>
                                </Items>
                                <AdditionalProperties>
                                    <AdditionalProperty>
                                        <CategoryName>{create_shipment_dictionary["Shipments"]["Shipment"]["Details"]["AdditionalProperties"]["AdditionalProperty"]["CategoryName"]}</CategoryName>
                                        <Name>{create_shipment_dictionary["Shipments"]["Shipment"]["Details"]["AdditionalProperties"]["AdditionalProperty"]["Name"]}</Name>
                                        <Value>{create_shipment_dictionary["Shipments"]["Shipment"]["Details"]["AdditionalProperties"]["AdditionalProperty"]["Value"]}</Value>
                                    </AdditionalProperty>
                                </AdditionalProperties>
                                <ContainsDangerousGoods>{create_shipment_dictionary["Shipments"]["Shipment"]["Details"]["ContainsDangerousGoods"]}</ContainsDangerousGoods>
                            </Details>
                            <Attachments>
                                <Attachment>
                                    <FileName>{create_shipment_dictionary["Shipments"]["Shipment"]["Attachments"]["Attachment"]["FileName"]}</FileName>
                                    <FileExtension>{create_shipment_dictionary["Shipments"]["Shipment"]["Attachments"]["Attachment"]["FileExtension"]}</FileExtension>
                                    <FileContents>{create_shipment_dictionary["Shipments"]["Shipment"]["Attachments"]["Attachment"]["FileContents"]}</FileContents>
                                </Attachment>
                            </Attachments>
                            <ForeignHAWB>{create_shipment_dictionary["Shipments"]["Shipment"]["ForeignHAWB"]}</ForeignHAWB>
                            <TransportType_x0020_>{create_shipment_dictionary["Shipments"]["Shipment"]["TransportType_x0020_"]}</TransportType_x0020_>
                            <PickupGUID>{create_shipment_dictionary["Shipments"]["Shipment"]["PickupGUID"]}</PickupGUID>
                            <Number>{create_shipment_dictionary["Shipments"]["Shipment"]["Number"]}</Number>
                            <ScheduledDelivery>
                                <PreferredDeliveryDate>{create_shipment_dictionary["Shipments"]["Shipment"]["ScheduledDelivery"]["PreferredDeliveryDate"]}</PreferredDeliveryDate>
                                <PreferredDeliveryTimeFrame_x0020_>{create_shipment_dictionary["Shipments"]["Shipment"]["ScheduledDelivery"]["PreferredDeliveryTimeFrame_x0020_"]}</PreferredDeliveryTimeFrame_x0020_>
                                <PreferredDeliveryTime>{create_shipment_dictionary["Shipments"]["Shipment"]["ScheduledDelivery"]["PreferredDeliveryTime"]}</PreferredDeliveryTime>
                            </ScheduledDelivery>
                        </Shipment>
                    </Shipments>
                    <LabelInfo>
                        <ReportID>{create_shipment_dictionary["LabelInfo"]["ReportID"]}</ReportID>
                        <ReportType>{create_shipment_dictionary["LabelInfo"]["ReportType"]}</ReportType>
                    </LabelInfo>
                </ShipmentCreationRequest>
            </soap:Body>
            </soap:Envelope>"""
    headers = {
	'Content-Type': 'text/xml; charset=utf-8',
    'SOAPAction':'http://ws.aramex.net/ShippingAPI/v1/Service_1_0/CreateShipments'
    }
    response = requests.request("POST", url, headers=headers, data=payload)
    print(response.text)
    print(response)
    frappe.msgprint((f'Its Done!! The SOAP API is called.'));