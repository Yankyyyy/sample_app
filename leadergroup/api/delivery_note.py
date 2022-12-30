import imp
import frappe
from frappe import _
from erpnext.stock.doctype.delivery_note.delivery_note import DeliveryNote

class LeadergroupDeliveryNote(DeliveryNote):
	def check_next_docstatus(self):
		submit_rv = frappe.db.sql(
			"""select 
				t1.name
			from `tabSales Invoice` t1
			inner join `tabSales Invoice Item` t2 
				on t1.name = t2.parent
			left join `tabDelivery Note Item` dni 
				on t1.name = dni.against_sales_invoice
			where t2.delivery_note = %s and t1.docstatus = 1
			and dni.name is null""",
			(self.name),
		)
		if submit_rv:
			frappe.throw(_("Sales Invoice {0} has already been submitted").format(submit_rv[0][0]))

		submit_in = frappe.db.sql(
			"""select t1.name
			from `tabInstallation Note` t1, `tabInstallation Note Item` t2
			where t1.name = t2.parent and t2.prevdoc_docname = %s and t1.docstatus = 1""",
			(self.name),
		)
		if submit_in:
			frappe.throw(_("Installation Note {0} has already been submitted").format(submit_in[0][0]))

# Ignore Sales Invoice Entry if it is interlink with Delivery Note again
def unlink_sales_invoice(doc, method):
	submit_rv = frappe.db.sql(
		"""select 
			t1.name
		from `tabSales Invoice` t1
		inner join `tabSales Invoice Item` t2 
			on t1.name = t2.parent
		left join `tabDelivery Note Item` dni 
			on t1.name = dni.against_sales_invoice
		where t2.delivery_note = %s and t1.docstatus = 1
		and dni.name is null""",
		(doc.name),
	)
	if not submit_rv:
		doc.ignore_linked_doctypes += ("Sales Invoice",)