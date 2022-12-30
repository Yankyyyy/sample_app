# -*- coding: utf-8 -*-
# Copyright (c) 2020, Leader Investment Group
from frappe import _
import json
import requests
import frappe
import jwt
import datetime
from frappe.utils import add_months, today

""" Fox HR Website and Fox HR Product Integration with CRM Module of ERP """


def generate_jwt_token():
    now = datetime.datetime.now() + datetime.timedelta(minutes=20)
    id_token_header = {"typ": "jwt", "alg": "HS256"}
    id_token = dict(
        UserID="1",
        UserName="1",
        ClientID="0",
        EmployeeID="f4a0dd369b3a4d8389413efc4d48b57f",
        RoleId="1",
        Schema="dbo",
        exp=round(now.timestamp())
    )
    id_token_encoded = jwt.encode(
        payload=id_token,
        key="fox-hr@leadergroup.com",
        algorithm="HS256",
        headers=id_token_header
    )
    return frappe.safe_decode(id_token_encoded)


def create_address(ref_doc, ref_doc_name, ref_doc_title, country, city):
    address = frappe.new_doc("Address")
    address.update({
        "address_title": ref_doc_name,
        "address_line1": city,
        "country": country,
        "city": city
    })
    address.insert()
    address.append("links", {
        "link_doctype": ref_doc,
        "link_name": ref_doc_name,
        "link_title": ref_doc_title
    })
    address.save()


@frappe.whitelist()
def updateLead():
    """
        Update or Create Lead
        Field: company, email_id, full_name, no_of_employees, contact_no, designation,
            domain, price, type_of_billing, country, location, message
    """
    data = json.loads(frappe.request.data)
    if not frappe.db.exists('Lead', {'email_id': data.get('email_id')}):
        lead = frappe.new_doc("Lead")
        lead.email_id = data.get('email_id')
    else:
        lead = frappe.get_doc('Lead', {'email_id': data.get('email_id')})
    if data.get('full_name'):
        lead.lead_name = data.get('full_name')
    if data.get('company'):
        lead.company_name = data.get('company')
    if data.get('no_of_employees'):
        lead.no_of_employees = data.get('no_of_employees')
    if data.get('contact_no'):
        lead.phone = data.get('contact_no')
    if data.get('designation') and frappe.db.exists('Designation', data.get('designation')):
        lead.designation = data.get('designation')
    if data.get('domain_name'):
        lead.domain_name = data.get('domain_name')
    if data.get('price'):
        lead.price = data.get('price')
    if data.get('type_of_billing'):
        lead.type_of_billing = data.get('type_of_billing')
    if data.get('location_id'):
        lead.location_id = data.get('location_id')
    if data.get('country_id'):
        lead.country_id = data.get('country_id')
    if data.get('price_slab'):
        lead.price_slab = data.get('price_slab')
    lead.save(ignore_permissions=True)
    frappe.db.commit()
    if data.get('country') and data.get('city'):
        create_address(ref_doc="Lead", ref_doc_name=lead.name, ref_doc_title=lead.lead_name,
                       country=data.get('country'), city=data.get('city'))
    return lead.name


@frappe.whitelist()
def updateCustomer():
    """
        Convert Lead to Customer
        Mode of Payment, Reference Number, Reference Date
    """
    data = json.loads(frappe.request.data)
    lead = frappe.get_doc('Lead', {'email_id': data.get('email_id')})
    start_date = today()
    if lead.type_of_billing == "Monthly":
        end_date = add_months(today(), 1)
    elif lead.type_of_billing == "Quarterly":
        end_date = add_months(today(), 3)
    else:
        end_date = add_months(today(), 12)
    party = make_customer(lead, start_date, end_date)
    is_live = False
    if data.get('is_live'):
        is_live = data.get('is_live')
    create_customer_in_foxhr(lead, start_date, end_date, is_live)
    if data.get('item') and data.get('price'):
        # sales_order = make_sales_order(customer=lead.company_name, company=frappe.db.get_default('Company'), price=data.get('price'),
        #                          item=data.get('item'), start_date=start_date, end_date=end_date)
        # sales_invoice = make_invoice(sales_order)
        subscription = makeSubscription(data, party)
        sales_invoice = getSubscriptionUpdates(subscription)
        # get the first Sales Invoice and create payment entry against it
        make_payment_entry(sales_invoice=sales_invoice[0], mode_of_payment=data.get('mode_of_payment'),
                           reference_number=data.get('reference_number'))
    return "Completed"

def make_customer(lead, start_date, end_date):
    customer = frappe.new_doc("Customer")
    customer.customer_type = "Company"
    customer.name = lead.company_name
    customer.customer_name = lead.company_name
    customer.lead_name = lead.name
    customer.contact_no = lead.phone
    customer.customer_group = "Individual"
    customer.territory = "Saudi Arabia"
    customer.domain_name = lead.domain_name
    customer.price = lead.price
    customer.so_required = 1
    customer.dn_required = 1
    customer.type_of_billing = lead.type_of_billing
    customer.no_of_employees = lead.no_of_employees
    customer.start_date = start_date
    customer.end_date = end_date
    customer.save(ignore_permissions=True)
    frappe.db.commit()
    return customer.name

@frappe.whitelist()
def updateCustomerPayment():
    """ Update Payment History of the Customer """
    data = json.loads(frappe.request.data)
    # sales_order = make_sales_order(customer=data.get('customer'), company=frappe.db.get_default('Company'), price=data.get('price'),
    #                              item=data.get('item'), start_date=data.get('start_date'), end_date=data.get('end_date'))
    # sales_invoice = make_invoice(sales_order)
    make_payment_entry(sales_invoice=data.get('sales_invoice'), mode_of_payment=data.get('mode_of_payment'),
                       reference_number=data.get('reference_number'))
    customer = frappe.get_doc('Customer', data.get('customer'))
    customer.start_date = data.get('start_date')
    customer.end_date = data.get('end_date')
    customer.save(ignore_permissions=True)
    frappe.db.commit()


@frappe.whitelist()
def verifyDomain():
    """
        Check if requested domain is available or not
        API call to FoxHR Product and return response to Fox HR Website
    """
    data = json.loads(frappe.request.data)
    domain = "Domain not found"
    # api_url = (
    # 	"https://stgapp.leadergroup.com/FoxWeb/Services/Identity/Authentication/ValidateOrganisation"
    # )
    # headers = {
    #   "Content-Type": "application/json"
    # }
    # payload = {
    #     	"OrganisationName": data.get('domain'),
    #     	"EmailId": data.get('email_id')
    # }
    # r = requests.post(api_url, headers=headers, data=json.dumps(payload))
    # response_data = json.loads(r.text)
    # if response_data['response']:
    # 	domain = "Domain verified"
    if frappe.db.exists('Customer', {'domain_name': data.get('domain')}):
        domain = "Domain verified"
    return domain


@frappe.whitelist()
def getDomainInfo():
    """ Return Customer Info to FoxHR Website """
    data = json.loads(frappe.request.data)
    email = data.get('email_id')
    domain = "Domain not found"
    is_live = False
    if data.get('is_live'):
        is_live = data.get('is_live')
    if is_live == 'true':
        api_url = ("https://services.foxerp.com/FoxWeb/Services/WebBFF/Administration/Authentication/ValidateEmail?emailid={}".format(
            email))
    else:
        api_url = ("https://stgapp.leadergroup.com/FoxWeb/Services/Identity/Authentication/ValidateEmail?emailid={}".format(
            email))   

    headers_dict = {
        'Accept': "application/json"
    }
    r = requests.get(api_url, headers=headers_dict)
    response_data = json.loads(r.text)
    if response_data['response']:
        organization_name = response_data['response']['organization_name']
        domain = organization_name+'.foxerp.com'
    return domain


def make_sales_order(customer, price, company, item, start_date, end_date):
    from erpnext.controllers.accounts_controller import get_default_taxes_and_charges
    """ Create Sales Order for FoxHR transaction"""
    uom = frappe.db.exists('UOM', 'Nos') or frappe.db.get_single_value('Stock Settings', 'stock_uom')
    sales_order = frappe.new_doc('Sales Order')
    sales_order.customer = customer
    sales_order.transaction_date = today()
    sales_order.delivery_date = today()
    sales_order.company = company
    sales_order.order_type = "Sales"
    
    item_line=sales_order.append('items')
    item_line.item_code = item
    item_line.description = "For period from " + start_date + " to " + end_date
    item_line.qty = 1
    item_line.uom = uom
    item_line.conversion_factor = 1
    item_line.rate = price
    item_line.amount = item_line.rate
    sales_order.disable_rounded_total=1
    taxes = get_default_taxes_and_charges("Sales Taxes and Charges Template", company=company)
    if taxes.get('taxes'):
        sales_order.update(taxes)
    sales_order.run_method("set_missing_values")
    sales_order.run_method("calculate_taxes_and_totals")
    sales_order.insert(ignore_permissions=True)
    sales_order.submit()
    frappe.db.commit()
    return sales_order.name

def make_invoice(sales_order):
    from erpnext.selling.doctype.sales_order.sales_order import make_sales_invoice
    sales_invoice = make_sales_invoice(sales_order, ignore_permissions=True)
    sales_invoice = sales_invoice.insert(ignore_permissions=True)
    sales_invoice.submit()
    frappe.db.commit()
    return sales_invoice.name

def make_payment_entry(sales_invoice, mode_of_payment, reference_number):
    """ Create Payment Entry for the Sales Invoice created online for Fox HR """
    from erpnext.accounts.doctype.sales_invoice.sales_invoice import get_bank_cash_account
    sales_invoice = frappe.get_doc('Sales Invoice', sales_invoice)
    payment_entry_dict = {
        "company": sales_invoice.company,
        "payment_type": 'Receive',
        "reference_no": reference_number,
        "reference_date": today(),
        "party_type": 'Customer',
        "party": sales_invoice.customer,
        "posting_date": today(),
        "paid_amount": sales_invoice.grand_total,
        "received_amount": sales_invoice.grand_total
    }
    payment_entry = frappe.new_doc("Payment Entry")
    payment_entry.update(payment_entry_dict)
    payment_entry.mode_of_payment = mode_of_payment
    payment_entry.paid_to = get_bank_cash_account(
        mode_of_payment, sales_invoice.company).get("account")
    payment_entry.append("references", {
        'reference_doctype': 'Sales Invoice',
        'reference_name': sales_invoice.name,
        "due_date": sales_invoice.due_date,
        'total_amount': sales_invoice.grand_total,
        'outstanding_amount': sales_invoice.grand_total,
        'allocated_amount': sales_invoice.grand_total
    })
    payment_entry.insert(ignore_permissions=True)
    payment_entry.submit()
    frappe.db.commit()


def create_customer_in_foxhr(lead, start_date, end_date, is_live):
    """ Create Customer in FoxHR """
    token = generate_jwt_token()
    customer = "Error creating customer"
    if is_live == "true":
        api_url = "https://services.foxerp.com/FoxWeb/Services/WebBFF/ProductManagement/ProductManagement/InsertClientDetailsFromERPWeb"
    else:
        api_url = "https://stgapp.leadergroup.com/FoxWeb/Services/WebBFF/ProductManagement/ProductManagement/InsertClientDetailsFromERPWeb"

    headers_dict = {
        'Content-Type': "application/json",
        'Authorization': 'Bearer '+token
    }
    domain_name = lead.domain_name.split(".", 1)[0]
    payload = {
        "ClientName": lead.company_name,
        "RegisteredName": lead.company_name,
        "LocationId": int(lead.location_id),
        "CountryId": int(lead.country_id),
        "WebAppHostingDetails": domain_name,
        "SlabPrice": int(lead.price_slab),
        "ClientPackageTypeID": "W",
        "BillingTypeID": 1,
        "ContractSlabID": 1,
        "AMCPricingMethodID": 1,
        "AuditReportLogicID": 2,
        "BillingAuditReportTypeID": 1,
        "BillingStartDate": start_date,
        "BillingEndDate": end_date,
        "AuditReportGenerationDate": start_date,
        "DisplayName": lead.lead_name,
        "UserName": lead.email_id,
        "NoOfEmployees": lead.no_of_employees,
        "TypeOfCompany": 1,
        "Designation": lead.designation,
        "ContactNo": lead.phone
    }
    r = requests.post(api_url, headers=headers_dict, data=json.dumps(payload))
    response_data = json.loads(r.text)
    if response_data['response']:
        customer = "Customer created successfully"
    return customer

@frappe.whitelist()
def makeSubscription(data=None, party=None, subscription=None):
    """
        Update or Create subscription
        Field: party_type, company, party, start_date, end_date, trial_period_start,
            follow_calendar_months, generate_new_invoices_past_due_date, days_until_due,
            cancel_at_end_of_period, generate_invoice_at_beginning_of_period, plans, qty
    """
    from erpnext.controllers.accounts_controller import get_default_taxes_and_charges
    if not data:
        data = json.loads(frappe.request.data)
    if not frappe.db.exists('Subscription', {'name': data.get('subscription')}):
         subscription = frappe.new_doc("Subscription")
    else:
        subscription = frappe.get_doc("Subscription", subscription)
    subscription.party_type = "Customer"
    subscription.company = frappe.db.get_default('Company')
    subscription.follow_calendar_months = 1
    subscription.generate_new_invoices_past_due_date = 1
    if not party:
        subscription.party = data.get('party')
    else:
        subscription.party = party
    if data.get('start_date'):
        subscription.start_date = data.get('start_date')
    if data.get('end_date'):
        subscription.end_date = data.get('end_date')
    if data.get('trial_period_start'):
        subscription.trial_period_start = data.get('trial_period_start')
    if data.get('days_until_due'):
        subscription.days_until_due = data.get('days_until_due')
    if data.get('cancel_at_end_of_period'):
        subscription.cancel_at_end_of_period = data.get('cancel_at_end_of_period')
    if data.get('generate_invoice_at_beginning_of_period'):
        subscription.generate_invoice_at_beginning_of_period = data.get('generate_invoice_at_beginning_of_period')
    else:
        subscription.generate_invoice_at_beginning_of_period = 1
    plan_line = subscription.append('plans')
    plan_line.plan = data.get('plan')
    plan_line.qty = data.get('quantity')
    tax = get_default_taxes_and_charges("Sales Taxes and Charges Template", company=subscription.company)
    subscription.sales_tax_template = tax.get('name')
    subscription.save(ignore_permissions=True)
    frappe.db.commit()
    return subscription.name


@frappe.whitelist()
def getSubscriptionUpdates(subscription):
    """
    Use this to get the latest state of the given `Subscription`
    """
    invoices = []
    subscription = frappe.get_doc("Subscription", subscription)
    subscription.process()
    for invoice in subscription.invoices:
        invoices.append(invoice.invoice)
    return invoices

@frappe.whitelist()
def getSubscriptionPlan(cost, billing_interval):
    # Get Subscription Plan
    if billing_interval == "Quaterly":
        billing_interval_count = 3
    if billing_interval == "Half Yearly":
        billing_interval_count = 6
    if billing_interval == "Yearly":
        billing_interval_count = 12
    subscription_name = frappe.db.exists("Subscription Plan", {
                    'cost' : cost,
                    'billing_interval_count' : billing_interval_count
                })
    if subscription_name:
        return subscription_name
    else:
        return "Subscription Plan doesn't exist"

@frappe.whitelist()
def getSubscriptionDetails(customer):
    sub_details = []
    
    #get subscription list of customer
    sub_list = frappe.db.get_list('Subscription',
                                  filters={
                                        'party': customer
                                    },
                                  order_by='name')
    
    for sub in sub_list:
        #get all the subscription details
        subscription = {}
        details = {}
        invoices = []
        plans = []
        invoice_no = []
        plan_name = []
        subscription = frappe.db.sql("""SELECT DISTINCT 
                                s.name, s.party_type, s.party, s.company,s.status, s.start_date, 
                                s.end_date, s.cancelation_date, s.trial_period_start,s.trial_period_end,
                                s.follow_calendar_months, s.generate_new_invoices_past_due_date, s.current_invoice_start,
                                s.current_invoice_end, s.days_until_due, sp.plan, sp.qty, si.invoice,s.sales_tax_template,
                                s.purchase_tax_template, s.cancel_at_period_end,s.generate_invoice_at_period_start,
                                s.apply_additional_discount, s.additional_discount_percentage, s.additional_discount_amount,s.cost_center, s.employee, s.days_until_due
                                FROM 
                                `tabSubscription` s
                                join `tabSubscription Plan Detail` sp on s.name = sp.parent
                                join `tabSubscription Invoice` si on s.name = si.parent
                                WHERE
                                s.name = "{0}" ;""".format(sub.name), as_dict=1)
        
        for invoice in subscription:
            if not invoice.get("invoice") in invoice_no:
                inv_dict = {}
                invoice_no.append(frappe.db.get_value('Sales Invoice',invoice.get("invoice"),"name"))
                inv_dict["invoice_no"] = frappe.db.get_value('Sales Invoice',invoice.get("invoice"),"name")
                inv_dict["due_date"] = frappe.db.get_value('Sales Invoice',invoice.get("invoice"),"due_date")
                inv_dict["status"] = frappe.db.get_value('Sales Invoice',invoice.get("invoice"),"status")
                inv_dict["grand_total"] = frappe.db.get_value('Sales Invoice',invoice.get("invoice"),"grand_total")
                invoices.append(inv_dict)
                
        for plan in subscription:
            if not plan.get("plan") in plan_name :
                plan_dict = {}
                plan_name.append(plan.get("plan"))
                plan_dict["plan_name"] = plan.get("plan")
                plan_dict["plan_qty"] = plan.get("qty")
                plans.append(plan_dict)
                
        #assign the values to their corresponding keys in a new dictionary variable   
        details["name"] = subscription[0]["name"]
        details["party_type"] = subscription[0]["party_type"]
        details["party"] = subscription[0]["party"]
        details["company"] = subscription[0]["company"]
        details["status"] = subscription[0]["status"]
        details["start_date"] = subscription[0]["start_date"]
        details["end_date"] = subscription[0]["end_date"]
        details["cancelation_date"] = subscription[0]["cancelation_date"]
        details["trial_period_start"] = subscription[0]["trial_period_start"]
        details["trial_period_end"] = subscription[0]["trial_period_end"]
        details["current_invoice_start"] = subscription[0]["current_invoice_start"]
        details["current_invoice_end"] = subscription[0]["current_invoice_end"]
        details["follow_calendar_months"] = subscription[0]["follow_calendar_months"]
        details["cancel_at_period_end"] = subscription[0]["cancel_at_period_end"]
        details["generate_new_invoices_past_due_date"] = subscription[0]["generate_new_invoices_past_due_date"]
        details["generate_invoice_at_period_start"] = subscription[0]["generate_invoice_at_period_start"]
        details["plans"] = plans
        details["sales_tax_template"] = subscription[0]["sales_tax_template"]
        details["purchase_tax_template"] = subscription[0]["purchase_tax_template"]
        details["apply_additional_discount"] = subscription[0]["apply_additional_discount"]
        details["additional_discount_percentage"] = subscription[0]["additional_discount_percentage"]
        details["additional_discount_amount"] = subscription[0]["additional_discount_amount"]
        details["invoices"] = invoices
        details["cost_center"] = subscription[0]["cost_center"]
        details["employee"] = subscription[0]["employee"]

        sub_details.append(details)
    return sub_details

@frappe.whitelist()
def cancelSubscription(subscription):
    """
    Cancels a `Subscription`. This will stop the `Subscription` from further invoicing the
    `Subscriber` but all already outstanding invoices will not be affected.
    """
    try:
        subscription = frappe.get_doc("Subscription", subscription)
        subscription.cancel_subscription()
        return _("Subscription Cancelled Successfully")
    except Exception as e:
        return e