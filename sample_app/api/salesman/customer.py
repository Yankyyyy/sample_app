import frappe
import json
from foxerp_lectronic.utils import createAPIErrorLog
from foxerp_lectronic.api.utils.common import upload_attachment
from frappe.contacts.doctype.address.address import get_address_display

@frappe.whitelist()
def updateCustomer(data, customer_id=None):
    #  To create a new Customer or to Update the details of an existing customer
    try:
        reload_flag = 0
        # If comapny id doesn't already exist in the Customer Doctype, a new one is created
        if not customer_id:
            customer = frappe.new_doc("Customer")
            customer.disabled = 1 # on creation, setting a new customer as disabled by default
        else:
            customer = frappe.get_doc("Customer", customer_id)
        customer.customer_name =  data.get("customer_name")
        if data.get("territory"):
            customer.territory = data.get("territory")
        if not customer.account_manager:
            customer.account_manager = frappe.session.user # getting the logged user
        customer.tax_id = data.get("tax_id")
        customer.owner_id = data.get("owner_id")
        customer.commercial_record_number = data.get("commercial_record_number")
        customer.issued_from = data.get("issued_from")
        if data.get("business_type"):
            customer.business_type = data.get("business_type")
        if data.get("shop_name"):
            customer.shop_name = data.get("shop_name")
        if data.get("payment_method"):
            customer.payment_method = data.get("payment_method")
        customer.city = data.get("city")
        customer.customer_group = "All Customer Groups"
        customer.save(ignore_permissions=True)
        #customer_id will be using for linking contact and address
        data["customer_id"] = customer.name
        # reload_flag is used for override address details updating customer doctype from address page
        if customer.customer_primary_address:
            reload_flag = 1
        # create and update contact and address
        customer.customer_primary_contact = update_customer_contact(data, customer.customer_primary_contact)
        if data.get('address'):
            customer.customer_primary_address = update_customer_address(data, customer.customer_primary_address)
        if reload_flag == 1:
            customer.reload()
        else:
            customer.primary_address = get_address_display(customer.customer_primary_address)
        customer.save(ignore_permissions=True)
        if data.get("bank"):
            bank_account = frappe.new_doc("Bank Account")
            bank_account.bank = data.get("bank")
            bank_account.account_name = customer.customer_name
            bank_account.party_type = "Customer"
            bank_account.party = customer.name
            if data.get("iban"):
                bank_account.iban = data.get("iban")
            bank_account.save(ignore_permissions=True)
        frappe.db.commit()
        return customer.name
    except Exception:
        error = frappe.get_traceback()
        createAPIErrorLog(error)
        return error

@frappe.whitelist()
def getCustomerContactList(customer_id):
    """returns contact list according to customer_name"""
    contact_list = frappe.db.sql("""select cnt.name as 'contact_id', cnt.first_name as 'name',
                        cnt.nationality, cnt.designation as 'position', cntp.phone as 'phone_number'
                    from `tabContact` cnt, `tabContact Phone` cntp, `tabDynamic Link` cntd
                        where cntd.link_name= %s and cntd.link_doctype="Customer" 
                            and cntd.parent=cnt.name and cntp.parent=cnt.name""",(customer_id), as_dict=1)
    return contact_list

def update_customer_contact(data, contact_id=None):
    """ create or update the customer Contact """
    if contact_id:
        contact = frappe.get_doc("Contact", contact_id)
    else:
        contact = frappe.new_doc('Contact')
    #in app side we have only one field for name so capturing it in first name field
    contact.first_name = data.get('name') or data.get('customer_name')
    if data.get('nationality'):
        contact.nationality = data.get('nationality')
    if data.get('position'):
        contact.designation = data.get('position')
    contact.is_primary_contact = 1 if data.get("customer_name") else 0

    #updatePhoneNumber (first row will be always updated)
    contact.set('phone_nos', [])
    phone_nos_row = contact.append('phone_nos', {})
    phone_nos_row.phone = data.get('phone_number')
    phone_nos_row.is_primary_mobile_no = 1

    #updateDynamicLink
    contact.set('links', [])
    reference_link_row = contact.append('links', {})
    reference_link_row.link_doctype = "Customer"
    reference_link_row.link_name = data.get('customer_id')
   
    contact.save(ignore_permissions=True)
    return contact.name

def update_customer_address(data, address_id=None):
    """ create or update the address """
    if not address_id:
        addr = frappe.new_doc('Address')
        addr.address_title = data.get("customer_id")
    else:
        addr = frappe.get_doc("Address", address_id)

    addr.address_line1 = data.get('address')
    addr.city = data.get('city')
    addr.country = data.get('country')
    addr.is_primary_address = 1

    #updateDynamicLink
    addr.set('links', [])
    reference_link_row = addr.append('links', {})
    reference_link_row.link_doctype = "Customer"
    reference_link_row.link_name = data.get('customer_id')

    addr.save(ignore_permissions=True)
    return addr.name

@frappe.whitelist()
def updateCreditDetails(customer_id, credit_data=None, contact_person=None, credit_terms=None, other_document_name=None, credit_id=None):
    try:
        if credit_data:
            credit_data = json.loads(credit_data)
        if contact_person:
            contact_person = json.loads(contact_person)
        if credit_terms:
            credit_terms = json.loads(credit_terms)

        if customer_id:
            #update customer credit and payment terms
            customer = frappe.get_doc("Customer",customer_id)
            if credit_data and credit_data.get("expected_monthly_sales"):
                customer.expected_monthly_sales = credit_data.get("expected_monthly_sales")
            if credit_terms and credit_terms.get("payment_terms"): 
                customer.payment_terms = credit_terms.get("payment_terms")
            # update credit limit child table
            if credit_terms and credit_terms.get('credit_limit'):
                update_credit_limits(customer, credit_terms)

            # upload attachment in Customer doctype
            for file in frappe.request.files.to_dict():
                file_url = None
                link_doctype = {
                    "is_private":1,
                    "doctype": "Customer",
                    "docname": customer_id,
                    "fieldname": file
                }
                if frappe.request.files[file]:
                    file_details = upload_attachment(frappe.request.files[file],link_doctype)
                    file_url = file_details.get("file_url")
                setattr(customer, file, file_url)
                if file == "others":
                    customer.other_document_name = other_document_name
            customer.save(ignore_permissions=True)

            if contact_person:
                # create and update contact details
                for i in contact_person:
                    i["customer_id"] = customer_id
                    update_customer_contact(i,i.get("contact_id"))

            if credit_data and credit_data.get("bank"):
                # create and update bank account
                if credit_id:
                    bank_account = frappe.get_doc("Bank Account",credit_id)
                else:
                    bank_account = frappe.new_doc("Bank Account")
                bank_account.bank = credit_data.get("bank")
                bank_account.account_name = customer.customer_name
                bank_account.party_type = "Customer"
                bank_account.party = customer_id
                if credit_data.get("iban"):
                    bank_account.iban = credit_data.get("iban")
                bank_account.save(ignore_permissions=True)
                return {"credit_id": bank_account.name}
        else:
            frappe.throw("Please Provide Customer Id")
    except Exception:
        error = frappe.get_traceback()
        createAPIErrorLog(error)
        return error

def update_credit_limits(customer, credit_terms):
    # update create limit table in customer Doctype
    customer.set('credit_limits', [])
    credit_limits_row = customer.append('credit_limits', {})
    credit_limits_row.credit_limit = credit_terms.get('credit_limit')
    credit_limits_row.company = frappe.db.get_single_value('Global Defaults', 'default_company')

@frappe.whitelist()
def getCustomerList():
    # Get customer list as per Account manager
    try:
        filters = {"account_manager": frappe.session.user}
        if frappe.request.data:
            data = json.loads(frappe.request.data)
            if data.get("status") == "Active":
                filters["disabled"] = 0
            elif data.get("status") == "Inactive":
                filters["disabled"] = 1
            if data.get("registration_date"):
                filters["registration_date"] = data.get("registration_date")
            if data.get("mobile_no"):
                filters["mobile_no"] = data.get("mobile_no")
            if data.get("territory"):
                filters["territory"] = data.get("territory")
            if data.get("commercial_record_number"):
                filters["commercial_record_number"] = data.get("commercial_record_number")
            if data.get("owner_id"):
                filters["owner_id"] = data.get("owner_id")
            if data.get("city"):
                filters["city"] = data.get("city")
            if data.get("registration_date"):
                filters["registration_date"] = ['like', data.get("registration_date")]
        data = frappe.db.get_list('Customer',
                filters= filters,
                fields=['name as customer_id', 'customer_name', 'disabled as status',
                    'commercial_record_number', 'payment_method'
                ],
                order_by='name asc'
            )
        for customer in data:
            if customer["status"] == 0:
                customer["status"] = "Active"
            else:
                customer["status"] = "Inactive"                
        return data
    except Exception:
        error = frappe.get_traceback()
        createAPIErrorLog(error)
        return error

@frappe.whitelist()
def getCustomerDetails(customer_id):
    try:
        data = frappe.db.get_list('Customer',
            filters={
                'name': customer_id
            },
            fields=['name as customer_id', 'customer_name', 
                    'territory', 'city', 'disabled as status', 
                    'owner_id', 'shop_name', 
                    'commercial_record_number', 'tax_id', 
                    'payment_method', 'registration_date',
                    'customer_primary_contact', 'customer_primary_address',
                    'business_type', 'issued_from'],
            order_by='name asc'
        )
        for i in data:
            if i["status"] == 1:
                i["status"] = "Inactive"
            else:
                i["status"] = "Active"
            if i["customer_primary_contact"]:
                primary_contact = frappe.get_doc("Contact",i["customer_primary_contact"])
                i['owner_name'] = primary_contact.first_name
                i['phone_number'] = primary_contact.mobile_no
            if i["customer_primary_address"]:    
                primary_address = get_address_display(i["customer_primary_address"])
                i['address'] = primary_address
                i['country'] = frappe.get_value("Address", i["customer_primary_address"], 'country')
            bank_account = frappe.db.get_list('Bank Account',
                filters={
                    'party_type': "Customer",
                    'party': customer_id
                },
                fields=['bank', 'iban'],
                order_by='name asc'
            )
            for bank in bank_account:
                i['bank'] = bank.get("bank")
                i['iban'] = bank.get("iban")
        return data
    except Exception:
        error = frappe.get_traceback()
        createAPIErrorLog(error)
        return error

@frappe.whitelist()
def getPaymentTerms():
    data = frappe.db.get_list('Payment Terms Template', pluck='name')
    return_info = {}
    for name in data :
        payment_record = {}
        doc = frappe.get_doc('Payment Terms Template', name)
        for term in doc.terms:
            payment_record["Payment Term"] = term.payment_term
            payment_record["Credit Days"] = term.credit_days
        return_info[name] = payment_record
    return return_info

@frappe.whitelist()
def getTerritory():
    """Return a list of all Territory which is not a group territory"""
    return frappe.db.get_list('Territory', {"is_group":0},pluck='name')

@frappe.whitelist()
def getCustomerAccountsInfo():

	import datetime
	data = json.loads(frappe.request.data)
	if data.get("start_date") and data.get("end_date"):
		start_date = data.get("start_date")
		end_date = data.get("end_date")
	else:
		start_date = (datetime.datetime.now()- datetime.timedelta(days=30)).strftime("%d/%m/%Y")
		end_date = datetime.datetime.now().strftime("%d/%m/%Y")
	sales_order_list = frappe.db.get_list("Sales Order", pluck = "name",  filters=[
		{'customer': data.get("customer")},
        ['transaction_date','>', start_date],
		['transaction_date','<', end_date]
	])
	return_data = {}
	entire_records = {}
	index = 0
	total_period = 0
	for sales_order in sales_order_list:
		individual_record = {}
		sales_record = frappe.get_doc("Sales Order", {"name": sales_order})
		individual_record["Customer Name"] = sales_record.customer
		individual_record["Sales Order Id"] = sales_record.name 
		individual_record["Payment Status"] = sales_record.status
		individual_record["Created Date"] = sales_record.transaction_date
		if sales_record.payment_schedule:
			for payment_records in sales_record.payment_schedule:
				individual_record["Due Date"] = payment_records.due_date
				individual_record["Payment Term"] = payment_records.payment_term
		sales_invoice_id = frappe.get_list("Sales Invoice",  pluck = "name",  filters={
		'sales_order' : sales_record.name
    	})
		if not sales_invoice_id:
			sales_invoice_id = ["null"]
		individual_record["Sales Invoice ID"] = sales_invoice_id[0]
		delivery_note_id = frappe.get_list("Delivery Note",  pluck = "name",  filters={
		'against_sales_order' : sales_record.name
    	})
		if not delivery_note_id:
			delivery_note_id = ["null"]
			individual_record["Warehouse"] = "null"
		else:
			delivery_note = frappe.get_doc("Delivery Note", {"name" : delivery_note_id[0]},["set_warehouse"])
			individual_record["Warehouse"] = delivery_note.set_warehouse
		individual_record["Delivery Note ID"] = delivery_note_id[0]
		individual_record["Credit Status"] = "null"
		individual_record["Credit Limit"] = "null"
		individual_record["Total"] = sales_record.grand_total - sales_record.advance_paid
		total_period += sales_record.grand_total - sales_record.advance_paid
		entire_records[index] = individual_record
		index += 1
	return_data["Account Records"] = entire_records
	return_data["Total for the period"] = total_period
	return return_data

@frappe.whitelist()
def getCreditDetails(customer_id):
    # Get Credit details for salesman app
    try:
        data = {}
        attachment = {}
        bank = iban = credit_id = None
        hostname = frappe.utils.get_url()
        customer = frappe.get_doc("Customer", customer_id)
        bank_account = frappe.db.get_list('Bank Account',
            filters={
                'party_type': "Customer",
                'party': customer_id
            },
            fields=['name', 'bank', 'iban'],
            order_by='name asc'
        )
        for i in bank_account:
            credit_id = i.get("name")
            bank = i.get("bank")
            iban = i.get("iban")

        if customer.get("trade_register_license"):
            attachment["trade_register_license"] = hostname + customer.get("trade_register_license")
        if customer.get("promisery_note"):
            attachment["promisery_note"] = hostname + customer.get("promisery_note")
        if customer.get("property_rending_contract"):
            attachment["property_rending_contract"] = hostname + customer.get("property_rending_contract")
        if customer.get("id_of_the_account_owner_authorized_person"):
            attachment["id_of_the_account_owner_authorized_person"] = hostname + customer.get("id_of_the_account_owner_authorized_person")
        if customer.get("chamber_of_commerce"):
            attachment["chamber_of_commerce"] = hostname + customer.get("chamber_of_commerce")
        if customer.get("others"):
            attachment["others"] = hostname + customer.get("others")
            attachment["other_document_name"] = customer.get("other_document_name")

        data["customer_id"] = customer_id
        data["credit_id"] = credit_id
        data["credit_data"] ={
            "bank": bank,
            "iban": iban,
            "business_type": customer.get("business_type"),
            "expected_monthly_sales": customer.get("expected_monthly_sales")
        }
        data["contact_person"] = getCustomerContactList(customer_id)
        data["attachment"] = attachment
        payment_terms = customer.get("payment_terms")
        credit_days = ""
        if payment_terms:
            doc = frappe.get_doc('Payment Terms Template', payment_terms)
            for term in doc.terms:
                credit_days = term.credit_days
        data["credit_terms"] ={
            "payment_terms": customer.get("payment_terms"),
            "credit_limit": customer.credit_limits[0].get("credit_limit") if customer.credit_limits else 0,
            "credit_days": credit_days
        }
        return data
    except Exception:
        error = frappe.get_traceback()
        createAPIErrorLog(error)
        return error
