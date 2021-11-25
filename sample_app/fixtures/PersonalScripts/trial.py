import frappe

def trial1(doc, event):

	frappe.msgprint((f'Its Done!! The controller hooks {event} is used here.'));
