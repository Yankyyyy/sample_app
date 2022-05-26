# Copyright (c) 2013, Leader Group and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from leadergroup.leader_group.report.item_profitabilty_detail___sales_register.item_profitabilty_detail___sales_register import get_valuation_rate
from erpnext.accounts.report.item_wise_sales_register.item_wise_sales_register import get_delivery_notes_against_sales_order

def execute(filters=None):
	columns = get_columns()
	data = []
	temp = []
	data = frappe.db.get_all("Item",
				fields=["item_code",
						"item_name",
						"description",
						"item_group"])
	
	conditions = get_conditions(filters)

	for item in data:
		quantity = 0
		base_net_amount = 0
		total_cost = 0
		unit_price = 0
		sales_invoice_data = frappe.db.sql("""
			select
				`tabSales Invoice Item`.name, `tabSales Invoice Item`.parent,
				`tabSales Invoice Item`.item_code,`tabSales Invoice Item`.base_net_amount,
				`tabSales Invoice Item`.price_list_rate, `tabSales Invoice Item`.qty,
				`tabSales Invoice Item`.modified, `tabSales Invoice`.project,
				`tabSales Invoice`.posting_date, `tabSales Invoice Item`.delivery_note,
				`tabSales Invoice Item`.so_detail, `tabSales Invoice`.update_stock
			from `tabSales Invoice`, `tabSales Invoice Item`
			where `tabSales Invoice`.name = `tabSales Invoice Item`.parent
				and `tabSales Invoice`.docstatus = 1 and `tabSales Invoice Item`.item_code = '{0}' {1}
			""".format(item.item_code, conditions), filters, as_dict=1)
		
		so_dn_map = get_delivery_notes_against_sales_order(sales_invoice_data)
		
		for sales_data in sales_invoice_data:
			unit_price = 0
			delivery_note = None
			if sales_data.delivery_note:
				delivery_note = sales_data.delivery_note
			elif sales_data.so_detail:
				delivery_note = ", ".join(so_dn_map.get(sales_data.so_detail, []))

			if not delivery_note and sales_data.update_stock:
				delivery_note = sales_data.parent

			if sales_data.delivery_note:
				unit_price = get_valuation_rate(sales_data.get("item_code"), sales_data)
				invoice_list = """select incoming_rate
					from `tabDelivery Note Item` DNI 
						inner join `tabDelivery Note` DN on DN.name = DNI.parent
					where DN.name = '{0}' 
						-- and DN.is_return =1 
						and DNI.item_code = '{1}'
					""".format(sales_data.delivery_note, sales_data.item_code)
				invoice_list = frappe.db.sql(invoice_list, as_dict=1)

				if invoice_list:
					unit_price = invoice_list[0].get("incoming_rate")
			quantity += sales_data.qty
			base_net_amount += sales_data.base_net_amount
			total_cost += unit_price * sales_data.qty
		item["qty"] = quantity
		item["total_sold_value"] = base_net_amount
		item["total_cost"] = total_cost
		item["profit"] = base_net_amount - total_cost
		if total_cost == 0.0 and base_net_amount == 0.0:
			temp.append(item)
	for i in temp:
		data.remove(i)
	return columns, data

def get_columns():
	return [
		{
			"fieldname": "item_code",
			"label": _("Item Code"),
			"fieldtype": "Link",
			"options": "Item",
			"width": 200
		},
		{
			"fieldname": "item_name",
			"label": _("Item Name"),
			"fieldtype": "Link",
			"options": "Item",
			"width": 200
		},
		{
			"fieldname": "description",
			"label": _("Item Description"),
			"fieldtype": "Data",
			"width": 200
		},
		{
			"fieldname": "item_group",
			"label": _("Item Group"),
			"fieldtype": "Link",
			"options": "Item Group",
			"width": 200
		},
		{
			"fieldname": "qty",
			"label": _("Total Sold Quantity"),
			"fieldtype": "Int",
			"width": 150
		},
		{
			"fieldname": "total_sold_value",
			"label": _("Total Sold Value"),
			"fieldtype": "Currency",
			"width": 150
		},
		{
			"fieldname": "total_cost",
			"label": _("Total Cost of Item"),
			"fieldtype": "Currency",
			"width": 150
		},
		{
			"fieldname": "profit",
			"label": _("Profit"),
			"fieldtype": "Currency",
			"width": 150
		}
	]

def get_conditions(filters):
	conditions = ""

	for opts in (("company", " and company=%(company)s"),
		("customer", " and `tabSales Invoice`.customer = %(customer)s"),
		("item_code", " and `tabSales Invoice Item`.item_code = %(item_code)s"),
		("from_date", " and `tabSales Invoice`.posting_date>=%(from_date)s"),
		("to_date", " and `tabSales Invoice`.posting_date<=%(to_date)s")):
			if filters.get(opts[0]):
				conditions += opts[1]

	if filters.get("mode_of_payment"):
		conditions += """ and exists(select name from `tabSales Invoice Payment`
			where parent=`tabSales Invoice`.name
				and ifnull(`tabSales Invoice Payment`.mode_of_payment, '') = %(mode_of_payment)s)"""

	if filters.get("warehouse"):
		conditions +=  """and ifnull(`tabSales Invoice Item`.warehouse, '') = %(warehouse)s"""

	if filters.get("brand"):
		conditions +=  """and ifnull(`tabSales Invoice Item`.brand, '') = %(brand)s"""

	if filters.get("item_group"):
		conditions +=  """and ifnull(`tabSales Invoice Item`.item_group, '') = %(item_group)s"""

	return conditions
