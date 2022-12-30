import frappe
from leadergroup.utils import get_invoice_type_code,get_return_invoice_value
import hashlib
from base64 import b64encode
from frappe import _


@frappe.whitelist()
def getSalesInvoiceXml(sales_invoice_id, is_previous_invoice=None):
    type_code = get_invoice_type_code(sales_invoice_id) 
    type_val = get_return_invoice_value(sales_invoice_id)
    si_data = frappe.get_doc("Sales Invoice",sales_invoice_id)
    supplier_add = frappe.get_doc("Address",si_data.company_address)
    cust_add = frappe.get_doc("Address",si_data.customer_address)
    company_id = frappe.get_value("Company",si_data.company,"tax_id")
    count = 0
    items_xml, supplier_country, cust_country = "", "", ""
    
 
    if(supplier_add.get("country")):
        supplier_country = frappe.get_value("Country",supplier_add.country,"code")            

    if(cust_add.get("country")):
        cust_country = frappe.get_value("Country",cust_add.country,"code")       
        
    for item in si_data.items:
        item_xml = f"""
    <cac:InvoiceLine>
        <cbc:ID>{count+1}</cbc:ID>
        <cbc:InvoicedQuantity unitCode="{item.get("uom")}">{item.get("qty")}</cbc:InvoicedQuantity>
        <cbc:LineExtensionAmount currencyID="{si_data.currency}">{item.get("amount")}</cbc:LineExtensionAmount>
        <cac:TaxTotal>
            <cbc:TaxAmount currencyID="{si_data.currency}">{(item.get("amount")*si_data.taxes[0].rate)/100}</cbc:TaxAmount>
            <cbc:RoundingAmount currencyID="{si_data.currency}">{item.get("net_amount")}</cbc:RoundingAmount>
        </cac:TaxTotal>
        <cac:Item>
            <cbc:Name>{item.get("item_name")}</cbc:Name>
            <cac:ClassifiedTaxCategory>
                <cbc:ID>S</cbc:ID>
                <cbc:Percent>{si_data.taxes[0].rate}</cbc:Percent>
                <cac:TaxScheme>
                    <cbc:ID>VAT</cbc:ID>
                </cac:TaxScheme>
            </cac:ClassifiedTaxCategory>
        </cac:Item>
        <cac:Price>
            <cbc:PriceAmount currencyID="{si_data.currency}">{item.get("rate")}</cbc:PriceAmount>
        </cac:Price>
    </cac:InvoiceLine>"""
        items_xml += item_xml
        count+=1
    
    if(is_previous_invoice==1):
        invoice_xml = f"""
<Invoice xsi:schemaLocation="urn:oasis:names:specification:ubl:schema:xsd:Invoice-2 UBL-Invoice-2.0.xsd" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns="urn:oasis:names:specification:ubl:schema:xsd:Invoice-2" xmlns:cac="urn:oasis:names:specification:ubl:schema:xsd:CommonAggregateComponents-2" xmlns:cbc="urn:oasis:names:specification:ubl:schema:xsd:CommonBasicComponents-2" xmlns:ccts="urn:oasis:names:specification:ubl:schema:xsd:CoreComponentParameters-2" xmlns:sdt="urn:oasis:names:specification:ubl:schema:xsd:SpecializedDatatypes-2" xmlns:udt="urn:un:unece:uncefact:data:specification:UnqualifiedDataTypesSchemaModule:2">
    <cbc:UBLVersionID>2.0</cbc:UBLVersionID>
    <cbc:CustomizationID>urn:oasis:names:specification:ubl:xpath:Invoice-2.0:sbs-1.0-draft</cbc:CustomizationID>
    <cbc:ProfileID>reporting:1.0</cbc:ProfileID>
    <cbc:ID>{si_data.name}</cbc:ID>
    <cbc:UUID>{si_data.sales_invoice_uuid}</cbc:UUID>
    <cbc:IssueDate>{si_data.posting_date}</cbc:IssueDate>
    <cbc:IssueTime>{si_data.posting_time}</cbc:IssueTime>
    <cbc:InvoiceTypeCode name="{type_code}">{type_val}</cbc:InvoiceTypeCode>
    <cbc:DocumentCurrencyCode>{si_data.currency}</cbc:DocumentCurrencyCode>
    <cbc:TaxCurrencyCode>{si_data.currency}</cbc:TaxCurrencyCode>
    <cbc:LineCountNumeric>2</cbc:LineCountNumeric>
    <cac:AdditionalDocumentReference>
        <cbc:ID>ICV</cbc:ID>
        <cbc:UUID>{si_data.name[14:]}</cbc:UUID>
    </cac:AdditionalDocumentReference>
    <cac:AccountingSupplierParty>
        <cac:Party>
            <cac:PartyIdentification>
                <cbc:ID schemeID="MLS">123457890</cbc:ID>
            </cac:PartyIdentification>
            <cac:PostalAddress>
                <cbc:StreetName>{supplier_add.get("address_line1")}</cbc:StreetName>
                <cbc:BuildingNumber>{supplier_add.get("address_line2")}</cbc:BuildingNumber>
                <cbc:PlotIdentification>1234</cbc:PlotIdentification>
                <cbc:CitySubdivisionName>{supplier_add.get("county")}</cbc:CitySubdivisionName>
                <cbc:CityName>{supplier_add.get("city")}</cbc:CityName>
                <cbc:PostalZone>{supplier_add.get("pincode")}</cbc:PostalZone>
                <cbc:CountrySubentity>Riyadh Region</cbc:CountrySubentity>
                <cac:Country>
                    <cbc:IdentificationCode>{supplier_country.upper()}</cbc:IdentificationCode>
                </cac:Country>
            </cac:PostalAddress>
            <cac:PartyTaxScheme>
                <cbc:CompanyID>{company_id}</cbc:CompanyID>
                <cac:TaxScheme>
                    <cbc:ID>VAT</cbc:ID>
                </cac:TaxScheme>
            </cac:PartyTaxScheme>
            <cac:PartyLegalEntity>
                <cbc:RegistrationName>{si_data.company}</cbc:RegistrationName>
            </cac:PartyLegalEntity>
        </cac:Party>
    </cac:AccountingSupplierParty>
    <cac:AccountingCustomerParty>
        <cac:Party>
            <cac:PartyIdentification>
                <cbc:ID schemeID="SAG">123C12345678</cbc:ID>
            </cac:PartyIdentification>
            <cac:PostalAddress>
                <cbc:StreetName>{cust_add.get("address_line1")}</cbc:StreetName>
                <cbc:BuildingNumber>{cust_add.get("address_line2")}</cbc:BuildingNumber>
                <cbc:PlotIdentification>1235</cbc:PlotIdentification>
                <cbc:CitySubdivisionName>{cust_add.get("county")}</cbc:CitySubdivisionName>
                <cbc:CityName>{cust_add.get("city")}</cbc:CityName>
                <cbc:PostalZone>{cust_add.get("pincode")}</cbc:PostalZone>
                <cbc:CountrySubentity>Riyadh Region</cbc:CountrySubentity>
                <cac:Country>
                    <cbc:IdentificationCode>{cust_country.upper()}</cbc:IdentificationCode>
                </cac:Country>
            </cac:PostalAddress>
            <cac:PartyTaxScheme>
                <cac:TaxScheme>
                    <cbc:ID>VAT</cbc:ID>
                </cac:TaxScheme>
            </cac:PartyTaxScheme>
            <cac:PartyLegalEntity>
                <cbc:RegistrationName>{si_data.customer}</cbc:RegistrationName>
            </cac:PartyLegalEntity>
        </cac:Party>
    </cac:AccountingCustomerParty>
    <cac:Delivery>
        <cbc:ActualDeliveryDate>2022-10-25</cbc:ActualDeliveryDate>
    </cac:Delivery>
    <cac:PaymentMeans>
        <cbc:PaymentMeansCode>42</cbc:PaymentMeansCode>
    </cac:PaymentMeans>
    <cac:TaxTotal>
        <cbc:TaxAmount currencyID="{si_data.currency}">{si_data.total_taxes_and_charges}</cbc:TaxAmount>
        <cac:TaxSubtotal>
            <cbc:TaxableAmount currencyID="{si_data.currency}">{si_data.total}</cbc:TaxableAmount>
            <cbc:TaxAmount currencyID="{si_data.currency}">{si_data.total_taxes_and_charges}</cbc:TaxAmount>
            <cac:TaxCategory>
                    <cbc:ID>S</cbc:ID>
                    <cbc:Percent>{si_data.taxes[0].rate}</cbc:Percent>
                    <cac:TaxScheme>
                        <cbc:ID>VAT</cbc:ID>
                    </cac:TaxScheme>
            </cac:TaxCategory>
        </cac:TaxSubtotal>
    </cac:TaxTotal>
    <cac:TaxTotal>
        <cbc:TaxAmount currencyID="{si_data.currency}">{si_data.total_taxes_and_charges}</cbc:TaxAmount>
    </cac:TaxTotal>
    <cac:LegalMonetaryTotal>
        <cbc:LineExtensionAmount currencyID="{si_data.currency}">{si_data.total}</cbc:LineExtensionAmount>
        <cbc:TaxExclusiveAmount currencyID="{si_data.currency}">{si_data.total}</cbc:TaxExclusiveAmount>
        <cbc:TaxInclusiveAmount currencyID="{si_data.currency}">{si_data.grand_total}</cbc:TaxInclusiveAmount>
        <cbc:AllowanceTotalAmount currencyID="{si_data.currency}">{si_data.total_advance}</cbc:AllowanceTotalAmount>
        <cbc:PayableAmount currencyID="{si_data.currency}">{si_data.outstanding_amount}</cbc:PayableAmount>
    </cac:LegalMonetaryTotal>{items_xml}
</Invoice>"""
    else:
        invoice_xml = f"""
<Invoice xsi:schemaLocation="urn:oasis:names:specification:ubl:schema:xsd:Invoice-2 UBL-Invoice-2.0.xsd" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns="urn:oasis:names:specification:ubl:schema:xsd:Invoice-2" xmlns:cac="urn:oasis:names:specification:ubl:schema:xsd:CommonAggregateComponents-2" xmlns:cbc="urn:oasis:names:specification:ubl:schema:xsd:CommonBasicComponents-2" xmlns:ccts="urn:oasis:names:specification:ubl:schema:xsd:CoreComponentParameters-2" xmlns:sdt="urn:oasis:names:specification:ubl:schema:xsd:SpecializedDatatypes-2" xmlns:udt="urn:un:unece:uncefact:data:specification:UnqualifiedDataTypesSchemaModule:2">
    <cbc:UBLVersionID>2.0</cbc:UBLVersionID>
    <cbc:CustomizationID>urn:oasis:names:specification:ubl:xpath:Invoice-2.0:sbs-1.0-draft</cbc:CustomizationID>
    <cbc:ProfileID>reporting:1.0</cbc:ProfileID>
    <cbc:ID>{si_data.name}</cbc:ID>
    <cbc:UUID>{si_data.sales_invoice_uuid}</cbc:UUID>
    <cbc:IssueDate>{si_data.posting_date}</cbc:IssueDate>
    <cbc:IssueTime>{si_data.posting_time}</cbc:IssueTime>
    <cbc:InvoiceTypeCode name="{type_code}">{type_val}</cbc:InvoiceTypeCode>
    <cbc:DocumentCurrencyCode>{si_data.currency}</cbc:DocumentCurrencyCode>
    <cbc:TaxCurrencyCode>{si_data.currency}</cbc:TaxCurrencyCode>
    <cbc:LineCountNumeric>2</cbc:LineCountNumeric>
    <cac:AdditionalDocumentReference>
        <cbc:ID>ICV</cbc:ID>
        <cbc:UUID>{si_data.name[14:]}</cbc:UUID>
    </cac:AdditionalDocumentReference>
    <cac:AdditionalDocumentReference>
        <cbc:ID>PIH</cbc:ID>
        <cac:Attachment>
            <cbc:EmbeddedDocumentBinaryObject mimeCode="text/plain">{generate_previous_invoice_hash(sales_invoice_id)}</cbc:EmbeddedDocumentBinaryObject>
        </cac:Attachment>
    </cac:AdditionalDocumentReference>
    <cac:AccountingSupplierParty>
        <cac:Party>
            <cac:PartyIdentification>
                <cbc:ID schemeID="MLS">123457890</cbc:ID>
            </cac:PartyIdentification>
            <cac:PostalAddress>
                <cbc:StreetName>{supplier_add.get("address_line1")}</cbc:StreetName>
                <cbc:BuildingNumber>{supplier_add.get("address_line2")}</cbc:BuildingNumber>
                <cbc:PlotIdentification>1234</cbc:PlotIdentification>
                <cbc:CitySubdivisionName>{supplier_add.get("county")}</cbc:CitySubdivisionName>
                <cbc:CityName>{supplier_add.get("city")}</cbc:CityName>
                <cbc:PostalZone>{supplier_add.get("pincode")}</cbc:PostalZone>
                <cbc:CountrySubentity>Riyadh Region</cbc:CountrySubentity>
                <cac:Country>
                    <cbc:IdentificationCode>{supplier_country.upper()}</cbc:IdentificationCode>
                </cac:Country>
            </cac:PostalAddress>
            <cac:PartyTaxScheme>
                <cbc:CompanyID>{company_id}</cbc:CompanyID>
                <cac:TaxScheme>
                    <cbc:ID>VAT</cbc:ID>
                </cac:TaxScheme>
            </cac:PartyTaxScheme>
            <cac:PartyLegalEntity>
                <cbc:RegistrationName>{si_data.company}</cbc:RegistrationName>
            </cac:PartyLegalEntity>
        </cac:Party>
    </cac:AccountingSupplierParty>
    <cac:AccountingCustomerParty>
        <cac:Party>
            <cac:PartyIdentification>
                <cbc:ID schemeID="SAG">123C12345678</cbc:ID>
            </cac:PartyIdentification>
            <cac:PostalAddress>
                <cbc:StreetName>{cust_add.get("address_line1")}</cbc:StreetName>
                <cbc:BuildingNumber>{cust_add.get("address_line2")}</cbc:BuildingNumber>
                <cbc:PlotIdentification>1235</cbc:PlotIdentification>
                <cbc:CitySubdivisionName>{cust_add.get("county")}</cbc:CitySubdivisionName>
                <cbc:CityName>{cust_add.get("city")}</cbc:CityName>
                <cbc:PostalZone>{cust_add.get("pincode")}</cbc:PostalZone>
                <cbc:CountrySubentity>Riyadh Region</cbc:CountrySubentity>
                <cac:Country>
                    <cbc:IdentificationCode>{cust_country.upper()}</cbc:IdentificationCode>
                </cac:Country>
            </cac:PostalAddress>
            <cac:PartyTaxScheme>
                <cac:TaxScheme>
                    <cbc:ID>VAT</cbc:ID>
                </cac:TaxScheme>
            </cac:PartyTaxScheme>
            <cac:PartyLegalEntity>
                <cbc:RegistrationName>{si_data.customer}</cbc:RegistrationName>
            </cac:PartyLegalEntity>
        </cac:Party>
    </cac:AccountingCustomerParty>
    <cac:Delivery>
        <cbc:ActualDeliveryDate>2022-10-25</cbc:ActualDeliveryDate>
    </cac:Delivery>
    <cac:PaymentMeans>
        <cbc:PaymentMeansCode>42</cbc:PaymentMeansCode>
    </cac:PaymentMeans>
    <cac:TaxTotal>
        <cbc:TaxAmount currencyID="{si_data.currency}">{si_data.total_taxes_and_charges}</cbc:TaxAmount>
        <cac:TaxSubtotal>
            <cbc:TaxableAmount currencyID="{si_data.currency}">{si_data.total}</cbc:TaxableAmount>
            <cbc:TaxAmount currencyID="{si_data.currency}">{si_data.total_taxes_and_charges}</cbc:TaxAmount>
            <cac:TaxCategory>
                    <cbc:ID>S</cbc:ID>
                    <cbc:Percent>{si_data.taxes[0].rate}</cbc:Percent>
                    <cac:TaxScheme>
                        <cbc:ID>VAT</cbc:ID>
                    </cac:TaxScheme>
            </cac:TaxCategory>
        </cac:TaxSubtotal>
    </cac:TaxTotal>
    <cac:TaxTotal>
        <cbc:TaxAmount currencyID="{si_data.currency}">{si_data.total_taxes_and_charges}</cbc:TaxAmount>
    </cac:TaxTotal>
    <cac:LegalMonetaryTotal>
        <cbc:LineExtensionAmount currencyID="{si_data.currency}">{si_data.total}</cbc:LineExtensionAmount>
        <cbc:TaxExclusiveAmount currencyID="{si_data.currency}">{si_data.total}</cbc:TaxExclusiveAmount>
        <cbc:TaxInclusiveAmount currencyID="{si_data.currency}">{si_data.grand_total}</cbc:TaxInclusiveAmount>
        <cbc:AllowanceTotalAmount currencyID="{si_data.currency}">{si_data.total_advance}</cbc:AllowanceTotalAmount>
        <cbc:PayableAmount currencyID="{si_data.currency}">{si_data.outstanding_amount}</cbc:PayableAmount>
    </cac:LegalMonetaryTotal>{items_xml}
</Invoice>"""

        xml_filename = si_data.name + ".xml"

        _file = frappe.get_doc({
            "doctype": "File",
            "file_name": xml_filename,
            "attached_to_doctype": si_data.doctype,
            "attached_to_name": si_data.name,
            "is_private": True,
            "content": invoice_xml
        })
        _file.save()
    return invoice_xml

@frappe.whitelist()
def generate_previous_invoice_hash(sales_invoice_id):
    invoice_xml = getSalesInvoiceXml(sales_invoice_id, 1)
    hashed_string = hashlib.sha256(invoice_xml.encode('utf-8')).hexdigest().encode("ascii")
    previous_invoice_hash = b64encode(hashed_string).decode("ascii")
    return previous_invoice_hash