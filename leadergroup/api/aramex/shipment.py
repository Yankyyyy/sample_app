import frappe
import json
import requests
from bs4 import BeautifulSoup
from frappe import _


@frappe.whitelist()
def create_shipment(doc):
    account_no = '161467'
    doc = json.loads(doc)
    pick_up_address_doc = frappe.get_doc("Address", doc.get("pickup_address_name"))
    delivery_address_doc = frappe.get_doc("Address", doc.get("delivery_address_name"))
    delivery_contact = frappe.db.get_value("Contact", doc.get("delivery_contact_name"), 'first_name')
    if frappe.db.get_value("Contact", doc.get("delivery_contact_name"), 'last_name'):
        delivery_contact += " "+frappe.db.get_value("Contact", doc.get("delivery_contact_name"), 'last_name')
    pickup_contact_person = frappe.db.get_value('User',doc.get("pickup_contact_person"), 'full_name')
    #dimensions
    shipment_parcel = frappe.db.get_list('Shipment Parcel', filters={"parent":doc.get("name") },fields=["*"])

    #generate_item_xml
    delivery_note = against_sales_order = ""
    dn_list = frappe.db.get_list('Shipment Delivery Note', filters={"parent":doc.get("name")},pluck='delivery_note')
    dn_items = frappe.db.get_list("Delivery Note Item",filters={"parent":["in",dn_list]},fields=["*"])
    if dn_list:
        delivery_note = dn_list[0]
        if delivery_note:
            against_sales_order = dn_items[0].against_sales_order
    services = ""
    cod_amount = 0
    if doc.get("is_cod"):
        services = "CODS"
        cod_amount = doc.get("cod_amount")

    items_xml =  ""
    for dn_item in dn_items :
        #form_xml
        item_xml = f"""
                                <ShipmentItem>
                                    <PackageType>string</PackageType>
                                    <Quantity>{dn_item.get("qty")}</Quantity>
                                    <Weight>
                                    <Unit>{dn_item.get("uom")}</Unit>
                                    <Value>100</Value>
                                    </Weight>
                                    <Comments>{dn_item.get("item_code")}</Comments>
                                    <Reference>{dn_item.get("item_code")}</Reference>
                                    <PiecesDimensions>
                                    <Dimensions>
                                        <Length>{shipment_parcel[0]['length']}</Length>
                                        <Width>{shipment_parcel[0]['width']}</Width>
                                        <Height>{shipment_parcel[0]['height']}</Height>
                                        <Unit>string</Unit>
                                    </Dimensions>
                                    </PiecesDimensions>
                                    <CommodityCode>string</CommodityCode>
                                    <GoodsDescription>{dn_item.get("item_code")}</GoodsDescription>
                                    <CountryOfOrigin>string</CountryOfOrigin>
                                    <CustomsValue>
                                    <CurrencyCode>string</CurrencyCode>
                                    <Value>7</Value>
                                    </CustomsValue>
                                    <ContainerNumber>string</ContainerNumber>
                                </ShipmentItem>
                        """
        items_xml += item_xml 

    url = "https://ws.aramex.net/shippingapi.v2/shipping/service_1_0.svc"
    
    payload = f"""<?xml version="1.0" encoding="utf-8"?>
            <soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">
            <soap:Body>
                <ShipmentCreationRequest xmlns="http://ws.aramex.net/ShippingAPI/v1/">
                    <ClientInfo>
                        <UserName>shameem@leadergroup.com</UserName>
                        <Password>Leader@123</Password>
                        <Version>1.0</Version>
                        <AccountNumber>{account_no}</AccountNumber>
                        <AccountPin>664164</AccountPin>
                        <AccountEntity>RUH</AccountEntity>
                        <AccountCountryCode>SA</AccountCountryCode>
                        <Source>100</Source>
                    </ClientInfo>
                    <Transaction>
                        <Reference1>001</Reference1>
                        <Reference2>string</Reference2>
                        <Reference3>string</Reference3>
                        <Reference4>string</Reference4>
                        <Reference5>string</Reference5>
                    </Transaction>
                    <Shipments>
                        <Shipment>
                            <Reference1>{delivery_note}</Reference1>
                            <Reference2>{against_sales_order}</Reference2>
                            <Shipper>
                                <Reference1>{against_sales_order}</Reference1>
                                <Reference2>{delivery_note}</Reference2>
                                <AccountNumber>{account_no}</AccountNumber>
                                <PartyAddress>
                                    <Line1>{pick_up_address_doc.address_line1}</Line1>
                                    <Line2>{pick_up_address_doc.address_line2}</Line2>
                                    <Line3></Line3>
                                    <City>{pick_up_address_doc.city}</City>
                                    <StateOrProvinceCode>string</StateOrProvinceCode>
                                    <PostCode>{pick_up_address_doc.pincode}</PostCode>
                                    <CountryCode>SA</CountryCode>
                                </PartyAddress>
                                <Contact>
                                    <PersonName>{pickup_contact_person}</PersonName>
                                    <CompanyName>{doc.get("pickup_company")}</CompanyName>
                                    <PhoneNumber1>{pick_up_address_doc.phone}</PhoneNumber1>
                                    <PhoneNumber2>5555555</PhoneNumber2>
                                    <CellPhone>{pick_up_address_doc.phone}</CellPhone>
                                    <EmailAddress>{pick_up_address_doc.email_id}</EmailAddress>
                                    <Type>string</Type>
                                </Contact>
                            </Shipper>
                            <Consignee>
                                <AccountNumber>{account_no}</AccountNumber>
                                <PartyAddress>
                                    <Line1>{delivery_address_doc.address_line1}</Line1>
                                    <Line2>{delivery_address_doc.address_line2}</Line2>
                                    <Line3></Line3>
                                    <City>{delivery_address_doc.city}</City>
                                    <StateOrProvinceCode>string</StateOrProvinceCode>
                                    <PostCode>{delivery_address_doc.pincode}</PostCode>
                                    <CountryCode>SA</CountryCode>
                                </PartyAddress>
                                <Contact>
                                    <PersonName>{delivery_contact}</PersonName>
                                    <CompanyName>{doc.get("delivery_customer")}</CompanyName>
                                    <PhoneNumber1>{delivery_address_doc.phone}</PhoneNumber1>
                                    <PhoneNumber2>5555555</PhoneNumber2>
                                    <CellPhone>{delivery_address_doc.phone}</CellPhone>
                                    <EmailAddress>{delivery_address_doc.email_id}</EmailAddress>
                                    <Type>string</Type>
                                </Contact>
                            </Consignee>
                            <ShippingDateTime>{doc.get("pickup_date")}</ShippingDateTime>
                            <Items>
                                {items_xml}
                            </Items>
                            <Details>
                                <Dimensions>
                                    <Length>{shipment_parcel[0]['length']}</Length>
                                    <Width>{shipment_parcel[0]['width']}</Width>
                                    <Height>{shipment_parcel[0]['height']}</Height>
                                    <Unit>cm</Unit>
                                </Dimensions>
                                <ActualWeight>
                                    <Unit>KG</Unit>
                                    <Value>{shipment_parcel[0]['weight']}</Value>
                                </ActualWeight>
                                <ChargeableWeight>
                                    <Unit>KG</Unit>
                                    <Value>{shipment_parcel[0]['weight']}</Value>
                                </ChargeableWeight>
                                <DescriptionOfGoods>{doc.get("description_of_content")}</DescriptionOfGoods>
                                <GoodsOriginCountry>SA</GoodsOriginCountry>
                                <NumberOfPieces>1</NumberOfPieces>
                                <ProductGroup>DOM</ProductGroup>
                                <ProductType>OND</ProductType>
                                <PaymentType>P</PaymentType>
                                <PaymentOptions>CASH</PaymentOptions>
                                <Services>{services}</Services>
                                <CashOnDeliveryAmount>{cod_amount}</CashOnDeliveryAmount>
                            </Details>
                        </Shipment>
                    </Shipments>
                </ShipmentCreationRequest>
            </soap:Body>
            </soap:Envelope>"""
    headers = {
    'Content-Type': 'text/xml; charset=utf-8',
    'SOAPAction':'http://ws.aramex.net/ShippingAPI/v1/Service_1_0/CreateShipments'
    }

    response = requests.request("POST", url, headers=headers, data=payload.encode('utf-8') )

    if response.status_code == 200:
        response_xml = BeautifulSoup(response.text, 'xml')

        if response_xml.find('HasErrors') and response_xml.find('HasErrors').text == "false" :
            shipment_id = response_xml.find('ID').text 
            shipment_doc = frappe.get_doc("Shipment",doc.get("name"))

            #changing property of shipment_id
            shipment_meta = frappe.get_meta('Shipment')
            df = shipment_doc.meta.get_field("shipment_id")
            df.set("allow_on_submit",1)

            shipment_doc.shipment_id = shipment_id
            shipment_doc.save(ignore_permissions=True)
            frappe.db.commit()
            return {"shipment_id":shipment_doc.shipment_id}
        else :
            show_error_notification_list(response_xml) 
               
    else:
        frappe.msgprint((f'Shipment creation unsuccessful.'));
        


@frappe.whitelist()
def track_shipments(shipment, shipment_id):
    shipment_doc = frappe.get_doc("Shipment",shipment)
    pick_up_address_doc = frappe.get_doc("Address", shipment_doc.pickup_address_name)
    delivery_address_doc = frappe.get_doc("Address", shipment_doc.delivery_address_name)
    account_no = '161467'
    
    url = "https://ws.aramex.net/shippingapi.v2/tracking/service_1_0.svc"
    
    payload = f"""<?xml version="1.0" encoding="utf-8"?>
            <soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">
            <soap:Body>
                <ShipmentTrackingRequest xmlns="http://ws.aramex.net/ShippingAPI/v1/">
                    <ClientInfo>
                        <UserName>shameem@leadergroup.com</UserName>
                        <Password>Leader@123</Password>
                        <Version>1.0</Version>
                        <AccountNumber>{account_no}</AccountNumber>
                        <AccountPin>664164</AccountPin>
                        <AccountEntity>RUH</AccountEntity>
                        <AccountCountryCode>SA</AccountCountryCode>
                        <Source>100</Source>
                    </ClientInfo>
                    <Transaction>
                        <Reference1>001</Reference1>
                        <Reference2>string</Reference2>
                        <Reference3>string</Reference3>
                        <Reference4>string</Reference4>
                        <Reference5>string</Reference5>
                    </Transaction>
                    <Shipments>
                        <string>{shipment_id}</string>
                    </Shipments>
                    <GetLastTrackingUpdateOnly>0</GetLastTrackingUpdateOnly>
                </ShipmentTrackingRequest>
            </soap:Body>
            </soap:Envelope>"""
    headers = {
    'Content-Type': 'text/xml; charset=utf-8',
    'SOAPAction':'http://ws.aramex.net/ShippingAPI/v1/Service_1_0/TrackShipments'
    }
    response = requests.request("POST", url, headers=headers, data=payload.encode('utf-8'))
    
    if response.status_code == 200:
        response_xml = BeautifulSoup(response.text, 'xml')
        if response_xml.find('HasErrors') and response_xml.find('HasErrors').text == "false":
            tracking_status_info = response_xml.find('UpdateDescription').text 
           

            shipment_meta = frappe.get_meta('Shipment')
            df = shipment_doc.meta.get_field("tracking_status_info")
            df.set("allow_on_submit",1)

            shipment_doc.tracking_status_info = tracking_status_info
            shipment_doc.save(ignore_permissions=True)
            frappe.db.commit()
            return shipment_doc.tracking_status_info
        else:
            show_error_notification_list(response_xml)
    else:
        frappe.msgprint((f'Shipment tracking was unsuccessful.'));
    
    #     Staging Credentials
    #     <ClientInfo>
    #     <UserName>armx.ruh.it@gmail.com</UserName>
    #     <Password>YUre@9982</Password>
    #     <Version>1.0</Version>
    #     <AccountNumber>{account_no}</AccountNumber>
    #     <AccountPin>442543</AccountPin>
    #     <AccountEntity>RUH</AccountEntity>
    #     <AccountCountryCode>SA</AccountCountryCode>
    #     <Source>100</Source>
    # </ClientInfo>

@frappe.whitelist()
def print_shipping_label(shipment_id):
    account_no = '161467'
    url = "https://ws.aramex.net/shippingapi.v2/shipping/service_1_0.svc"
    
    payload = f"""<?xml version="1.0" encoding="utf-8"?>
            <soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">
            <soap:Body>
                <LabelPrintingRequest xmlns="http://ws.aramex.net/ShippingAPI/v1/">
                <ClientInfo>
                    <UserName>shameem@leadergroup.com</UserName>
                    <Password>Leader@123</Password>
                    <Version>1.0</Version>
                    <AccountNumber>{account_no}</AccountNumber>
                    <AccountPin>664164</AccountPin>
                    <AccountEntity>RUH</AccountEntity>
                    <AccountCountryCode>SA</AccountCountryCode>
                    <Source>100</Source>
                </ClientInfo>
                <ShipmentNumber>{shipment_id}</ShipmentNumber>
                <LabelInfo>
                    <ReportID>9201</ReportID>
                    <ReportType>URL</ReportType>
                </LabelInfo>
                </LabelPrintingRequest>
            </soap:Body>
            </soap:Envelope>"""
            
    headers = {
    'Content-Type': 'text/xml; charset=utf-8',
    'SOAPAction':'http://ws.aramex.net/ShippingAPI/v1/Service_1_0/PrintLabel'
    }
    response = requests.request("POST", url, headers=headers, data=payload.encode('utf-8'))

    if response.status_code == 200:
        response_xml = BeautifulSoup(response.text, 'xml')
        if response_xml.find('HasErrors') and response_xml.find('HasErrors').text == "false":
            label = response_xml.find('LabelURL').text
            return label
        else:
            show_error_notification_list(response_xml)  
    else:
        frappe.msgprint((f'Label creation was unsuccessful.'))


def show_error_notification_list(response_xml) :
    """catch all errors from aramex response and show it as a message  when respose code is 200"""
    error_notification_xml = response_xml.select("Notifications Notification Message")
    error_notification_list = [message.get_text()+ "<br>" for message in error_notification_xml ]
    frappe.throw(_(error_notification_list))