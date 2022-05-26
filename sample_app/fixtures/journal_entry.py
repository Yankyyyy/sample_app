from __future__ import unicode_literals
import frappe
from frappe import _
from frappe.model.workflow import get_workflow

@frappe.whitelist()
def update_return_status_in_je(doc, method): 
    workflow = get_workflow(doc.doctype)
    if doc.reversal_of and doc._action == "submit"  :
        frappe.db.set_value("Journal Entry", {"name": doc.reversal_of}, workflow.workflow_state_field, "Return Issued")
    if doc.reversal_of and doc._action == "cancel"  :
        frappe.db.set_value("Journal Entry", {"name": doc.reversal_of}, workflow.workflow_state_field, "Approved" )