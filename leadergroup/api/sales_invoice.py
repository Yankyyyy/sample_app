from __future__ import unicode_literals
import frappe
from num2words import num2words
from uuid import uuid4

@frappe.whitelist()
def set_in_words_arabic(doc, method):
    doc.in_words_arabic = " فقط" +num2words(float(doc.grand_total), lang='ar', to='currency', currency="SAR")

def sales_invoice_uuid(doc, method):
    doc.sales_invoice_uuid = str(uuid4())

# Set sales invoice id in Delivery Note Item doctype
def set_delivery_note_ref(doc, method):
    if doc.items:
        for item in doc.items:
            if frappe.db.exists("Delivery Note", item.delivery_note):
                if frappe.db.exists("Delivery Note Item", item.dn_detail):
                    frappe.db.set_value('Delivery Note Item', item.dn_detail, 'against_sales_invoice', doc.name, update_modified=False)
                    frappe.db.set_value('Delivery Note Item', item.dn_detail, 'si_detail', item.name, update_modified=False)

# Ignore Delivery Note Entry from Sales Invoice
def unlink_delivery_note(doc, method):
    submit_rv = frappe.db.sql(
        """select 
            t1.name
        from `tabDelivery Note` t1
        inner join `tabDelivery Note Item` t2 
            on t1.name = t2.parent
        left join `tabSales Invoice Item` sii 
            on t1.name = sii.delivery_note
        where t2.against_sales_invoice = %s and t1.docstatus = 1
        and sii.name is null""",
        (doc.name),
    )
    if not submit_rv:
        doc.ignore_linked_doctypes += ("Delivery Note",)
