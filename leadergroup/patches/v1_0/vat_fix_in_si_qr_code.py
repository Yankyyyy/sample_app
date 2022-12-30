import frappe
from erpnext.regional.saudi_arabia.utils import create_qr_code, delete_qr_code_file

def execute():
    frappe.reload_doc('Accounts', 'doctype', 'Sales Invoice')
    sales_invoice_list = frappe.db.get_list('Sales Invoice',
                            filters = {
                                'docstatus': ['!=', 2],
                                'taxes_and_charges': ['!=', ""],
                                'discount_amount': ['>', 0]
                            },
                            pluck = 'name'
                        )
    for name in sales_invoice_list:
        print('name')
        sales_invoice = frappe.get_doc('Sales Invoice', name)
        delete_qr_code_file(sales_invoice)
        create_qr_code(sales_invoice)
    frappe.reload_doc('Accounts', 'doctype', 'Sales Invoice')
