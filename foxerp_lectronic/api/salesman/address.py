import frappe
from foxerp_lectronic.utils import createAPIErrorLog
import json

@frappe.whitelist()
def createAddress():
    try:
        if frappe.request.data:
            data = json.loads(frappe.request.data)
            """Creating new address for the customer"""
            if frappe.db.exists("Customer",data.get('customer_id')):
                address = frappe.new_doc('Address')
                address.address_type = data.get('address_type')
                address.address_title = data.get('customer_id')
                address.address_line1 = data.get('address_line1')
                address.address_line2 = data.get('address_line2')
                address.country = data.get('country')
                address.state = data.get('state')
                address.city = data.get('city')
                address.pincode = data.get('pincode')
                address.phone = data.get('phone')
                
                """createDynamicLink"""
                address.set('links', [])
                reference_link_row = address.append('links', {})
                reference_link_row.link_doctype = "Customer"
                reference_link_row.link_name = data.get('customer_id')
                address.save(ignore_permissions=True)
            else :
                return "Customer does not exist"
    except Exception:
        error = frappe.get_traceback()
        createAPIErrorLog(error)
        return error

@frappe.whitelist()
def getAddress(customer_id,address_type=None):
    try:
        """checking whether the customer exists """
        sql_condition = ""
        if address_type:
            sql_condition = " and ad.address_type ='"+address_type+"'" 
        if frappe.db.exists("Customer", customer_id):
            """"returns address list according to customer_ID and address type"""
            address_list = frappe.db.sql("""SELECT ad.name, ad.address_type, COALESCE(ad.address_in_arabic,'') as address_in_arabic,ad.address_line1, ad.country, ad.state, ad.city, ad.pincode  
                                            FROM `tabAddress` ad, `tabDynamic Link` li WHERE li.link_name = "{0}" and li.link_doctype = "Customer"
                                            and li.parent = ad.name {1} ;""".format(customer_id,sql_condition), as_dict=1)
            return address_list
        else:
            return "Customer does not exist"
    except Exception:
        error = frappe.get_traceback()
        createAPIErrorLog(error)
        return error
