import frappe
from frappe import _

@frappe.whitelist()
def send_email_for_next_action():
    """sending email to owner accoring to action date"""
    if frappe.db.exists('Email Template', "Opportunity Next Action"):
        next_action_template = frappe.get_doc('Email Template', "Opportunity Next Action")
        next_actions_list = frappe.db.get_list('Next Action',fields=['*'],filters={"action_date":frappe.utils.nowdate(),"status":["!=","Closed"]})

        for action in next_actions_list :
            message = frappe.render_template(next_action_template.response, action)
            frappe.sendmail(
                recipients= action.owner,
                subject=next_action_template.subject,
                message=message,
                reference_doctype=action.parenttype,
                reference_name=action.parent
            )
    else: 
        frappe.msgprint(_('Please Configure "Opportunity Next Action" Email Template'))