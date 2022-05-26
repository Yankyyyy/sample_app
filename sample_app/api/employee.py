from __future__ import unicode_literals
import frappe

@frappe.whitelist()
def set_employee_autoname(doc, method):
    emp_name = doc.first_name 
    if doc.middle_name :
        emp_name += " "+ doc.middle_name
    if doc.last_name :
        emp_name += " "+ doc.last_name
    doc.name = doc.employee_number +"-"+ emp_name