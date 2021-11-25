import json
import frappe
from frappe.utils import add_months, today
from erpnext.accounts.party import get_party_account

"""For HR Website and Fox HR Products Integration with CRM Module of ERP"""

def create_address(
    ref_doc,
    ref_doc_name,
    ref_doc_title,
    country,
    city,
    ):
    address = frappe.new_doc('Address')
    address.update({
        'address_title': ref_doc_name,
        'address_line1': city,
        'country': country,
        'city': city,
        })
    address.insert()
    address.append('links', {'link_doctype': ref_doc,
                   'link_name': ref_doc_name,
                   'link_title': ref_doc_title})
    address.save()


@frappe.whitelist()
def updateLead():
    """Update or Create Lead
....Field: company, email_id, full_name, no_of_employees, contact_no, designation,
....domain, price, type_of_billing, country, location, message"""

    data = json.loads(frappe.request.data)
    if not frappe.db.exists('Lead', {'email_id': data.get('email_id')}):
        lead = frappe.new_doc('Lead')
        lead.email_id = data.get('email_id')
    else:
        lead = frappe.get_doc('Lead', {'email_id': data.get('email_id'
                              )})
    if data.get('full_name'):
        lead.lead_name = data.get('full_name')
    if data.get('company'):
        lead.company_name = data.get('company')
    if data.get('contact_no'):
        lead.phone = data.get('contact_no')
    if data.get('designation') and frappe.db.exists('Designation',
            data.get('designation')):
        lead.designation = data.get('designation')
    if data.get('domain_name'):
        lead.domain_name = data.get('domain_name')
    if data.get('price'):
        lead.price = data.get('price')
    lead.save(ignore_permissions=True)
    frappe.db.commit()
    create_address(ref_doc='Lead', ref_doc_name=lead.name,
                   ref_doc_title=lead.lead_name,
                   country=data.get('country'), city=data.get('city'))


@frappe.whitelist()
def updateCustomer():
    """Convert Lead to Customer
....Mode of Payment, Reference Number, Reference Date"""

    data = json.loads(frappe.request.data)
    lead = frappe.get_doc('Lead', {'email_id': data.get('email_id')})
    start_date = today()
    end_date = add_months(today(), 12)
    make_customer(lead, start_date, end_date)
    if data.get('item') and data.get('price'):
        sales_invoice = make_invoice(
            customer=lead.company_name,
            company=frappe.db.get_default('Company'),
            price=data.get('price'),
            item=data.get('item'),
            start_date=start_date,
            end_date=end_date,
            )
        make_payment_entry(sales_invoice=sales_invoice,
                           mode_of_payment=data.get('mode_of_payment'),
                           reference_number=data.get('reference_number'
                           ))


def make_customer(lead, start_date, end_date):
    customer = frappe.new_doc('Customer')
    customer.company_type = 'Company'
    customer.name = lead.company_name
    customer.customer_name = lead.company_name
    customer.lead_name = lead.company_name
    customer.contact_no = lead.phone
    customer.customer_group = frappe.db.get_default('Customer Group')
    customer.domain_name = lead.domain_name
    customer.price = lead.price
    customer.so_required = 1
    customer.dn_required = 1
    customer.start_date = start_date
    customer.end_date = end_date
    customer.save(ignore_permissions=True)
    frappe.db.commit()


@frappe.whitelist()
def updateCustomerPayment():
    """Update Payment History of the Customer"""

    data = json.loads(frappe.request.data)
    sales_invoice = make_invoice(
        customer=data.get('customer'),
        company=frappe.db.get_default('Company'),
        price=data.get('price'),
        item=data.get('item'),
        start_date=data.get('start_date'),
        end_date=data.get('end_date'),
        )
    make_payment_entry(sales_invoice=sales_invoice,
                       mode_of_payment=data.get('mode_of_payment'),
                       reference_number=data.get('reference_number'))
    customer = frappe.get_doc('Customer', data.get('customer'))
    customer.start_date = data.get('start_date')
    customer.end_date = data.get('end_date')
    customer.save(ignore_permissions=True)
    frappe.db.commit()


@frappe.whitelist()
def verifyDomain():
    """Check if requested  domain is avialable or not
....API call to FoxHR Product and return response to FoxHR Website"""

    data = json.loads(frappe.request.data)
    domain = data.get('domain')
    return domain


@frappe.whitelist()
def getCustomerInfo():
    """Return Customer Info to FoxHR Website"""

    data = json.loads(frappe.request.data)
    customer = frappe.get_doc('Customer', data.get('email_id'))
    return customer


def make_invoice(
    customer,
    company,
    price,
    item,
    start_date,
    end_date,
    ):
    """Create Sales Invoice for the online payment for Fox HR"""

    uom = frappe.db.exists('UOM', 'Nos') \
        or frappe.db.get_single_value('Stock Settings', 'Stock UOM')
    sales_invoice = frappe.new_doc('Sales Invoice')
    sales_invoice.customer = customer
    sales_invoice.due_date = today()
    sales_invoice.company = company
    sales_invoice.is_pos = 0
    sales_invoice.debit_to = get_party_account('Customer', customer,
            company)

    item_line = sales_invoice.append('items')
    item_line.item_code = item
    item_line.description = 'For period from ' + start_date + ' to ' \
        + end_date
    item_line.qty = 1
    item_line.uom = uom
    item_line.conversion_factor = 1
    item_line.income_account = frappe.db.get_value('Company', company,
            'default_income_account')
    item_line.rate = price
    item_line.amount = item_line.rate
    sales_invoice.set_missing_values()
    sales_invoice.insert(ignore_permissions=True)
    sales_invoice.submit()
    return sales_invoice.name


def make_payment_entry(sales_invoice, mode_of_payment,
                       reference_number):
    """Create Payment Entry fro the Sales Invoice created online for Fox HR"""

    from erpnext.accounts.doctype.sales_invoice.sales_invoice import get_bank_cash_account
    sales_invoice = frappe.get_doc('Sales Invoice', sales_invoice)
    payment_entry_dict = {
        'company': sales_invoice.company,
        'payment_type': 'Recieve',
        'reference_no': reference_number,
        'reference_date': today(),
        'party_type': 'Customer',
        'party': sales_invoice.customer,
        'posting_date': today(),
        'paid_amount': sales_invoice.grand_total,
        'recieve_amount': sales_invoice.grand_total,
        }
    payment_entry = frappe.new_doc('Payment Entry')
    payment_entry.update(payment_entry_dict)
    payment_entry.mode_of_payment = mode_of_payment
    payment_entry.paid_to = get_bank_cash_account(mode_of_payment,
            sales_invoice.company).get('account')
    payment_entry.append('references', {
        'reference_doctype': 'Sales Invoice',
        'reference_name': sales_invoice.name,
        'due_date': sales_invoice.due_date,
        'total_amount': sales_invoice.grand_total,
        'outstanding_amount': sales_invoice.grand_total,
        'allocated_amount': sales_invoice.grand_total,
        })
    payment_entry.insert(ignore_permissions=True)
    payment_entry.submit()


def create_customer_in_foxhr():
    """Create Customer in Fox HR"""
    pass
