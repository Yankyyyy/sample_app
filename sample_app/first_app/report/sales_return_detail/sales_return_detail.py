# Copyright (c) 2013, Leader Group and contributors
# For license information, please see license.txt

import frappe
from frappe import _

def execute(filters=None):
	columns, data = [],[]
	columns = get_columns(filters)
	sales_return_data =frappe.db.sql("""select 
	distinct(si.name),si.return_against,si.posting_date,si.customer,si.cost_center,si.grand_total,si.status,sii.delivery_note,sii.warehouse
	from 
	`tabSales Invoice` si ,`tabSales Invoice Item` sii
	where 
	si.is_return =1 and si.docstatus=1 and sii.parent = si.name""", as_dict=1)
	
	for si_return in sales_return_data :
		#sales returns created from sales invoice
		if si_return.get("return_against"):
			dn_details =  get_dn_details(si_return.get("return_against"))
			row_dict ={
			"return_date" : si_return.get("posting_date"),
			"dn_id" : dn_details.get("name") if dn_details  else "",
			"customer" : si_return.get("customer"),
			"location" : si_return.get("warehouse"),
			"cost_center" : si_return.get("cost_center"),
			"status" : si_return.get("status"),
			"si_id" : si_return.get("return_against"),
			"cn_id" : si_return.get("name"),
			"return_amount" : si_return.get("grand_total"),
			"return_reason" : dn_details.get("return_reason") if dn_details else ""
			}
		#sales returns created from delivery note
		else:
			row_dict ={
			"return_date" : si_return.get("posting_date"),
			"dn_id" : si_return.get("delivery_note"),
			"customer" : si_return.get("customer"),
			"location" : si_return.get("warehouse"),
			"cost_center" : si_return.get("cost_center"),
			"status" : si_return.get("status"),
			"si_id" : frappe.db.get_value("Delivery Note Item",{"parent":si_return.get("delivery_note")},"against_sales_invoice"),
			"cn_id" : si_return.get("name"),
			"return_amount" : si_return.get("grand_total"),
			"return_reason" : frappe.db.get_value("Delivery Note",{"name":si_return.get("delivery_note")},"return_reason")
			}
		data.append(row_dict)
	return columns, data

def get_columns(filters):
	columns = []
	columns.extend( 
		[
		{
			"fieldname": "return_date",
			"label": _("Return Date"),
			"fieldtype": "Date",
			"width": 120
		}, 
		{
			"fieldname": "dn_id",
			"label": _("Delivery Note ID"),
			"fieldtype": "Link",
			"options": "Delivery Note",
			"width": 200
		},
		{
			"fieldname": "customer",
			"label": _("Customer"),
			"fieldtype": "Link",
			"options": "Customer",
			"width": 120
		},
		{
			"fieldname": "location",
			"label": _("Location"),
			"fieldtype": "Link",
			"options": "Warehouse",
			"width": 120
		},
		{
			"fieldname": "cost_center",
			"label": _("Cost Center"),
			"fieldtype": "Link",
			"options": "Cost Center",
			"width": 120
		},
		{
			"fieldname": "status",
			"label": _("Status"),
			"fieldtype": "Data",
			"width": 120
		},
		{
			"fieldname": "return_amount",
			"label": _("Return Amount"),
			"fieldtype": "Float",
			"width": 120
		},
		{
			"fieldname": "si_id",
			"label": _("Sales Invoice ID"),
			"fieldtype": "Link",
			"options": "Sales Invoice",
			"width": 120
		},
		{
			"fieldname": "cn_id",
			"label": _("Credit Note ID"),
			"fieldtype": "Link",
			"options": "Sales Invoice",
			"width": 120
		},
		{
			"fieldname": "return_reason",
			"label": _("Return Reason"),
			"fieldtype": "Data",
			"width": 120
		}
		]
	)
	return columns

def get_dn_details(si_name):
	dn_details = frappe.db.sql("""
	select dn.return_reason  ,dn.name from `tabDelivery Note` dn,`tabDelivery Note Item` dni
	where dni.against_sales_invoice = %s and dni.parent = dn.name  and dn.is_return= 1 and dn.docstatus=1 limit 1
	""",(si_name),as_dict = 1)
	return dn_details[0] if dn_details else dn_details
	
