# Copyright (c) 2013, Leader Group and contributors
# For license information, please see license.txt

import frappe
from frappe import _

def execute(filters=None):
	columns = get_columns()
	data = []
	temp = []
	data = frappe.db.get_all("Item",
				fields=["item_code",
						"item_name",
						"description",
						"item_group",
      					"valuation_rate"])
	
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
				`tabSales Invoice Item`.modified
			from `tabSales Invoice`, `tabSales Invoice Item`
			where `tabSales Invoice`.name = `tabSales Invoice Item`.parent
				and `tabSales Invoice`.docstatus = 1 and `tabSales Invoice Item`.item_code = '{0}' {1}
			""".format(item.item_code, conditions), filters, as_dict=1)
		
		for sales_data in sales_invoice_data:
			quantity += sales_data.qty
			base_net_amount += sales_data.base_net_amount
			if item.valuation_rate:
				unit_price = item.valuation_rate
			else:
				unit_price = get_last_purchase_rate(sales_data.modified, item.item_code)
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
			"fieldtype": "Float",
			"width": 150
		},
		{
			"fieldname": "total_cost",
			"label": _("Total Cost of Item"),
			"fieldtype": "Float",
			"width": 150
		},
		{
			"fieldname": "profit",
			"label": _("Profit"),
			"fieldtype": "Float",
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

def get_last_purchase_rate(date, item_code):
	condition = ''
	if date:
		condition += " AND date(posting_date) <= '%s'" % (date)

	last_purchase_rate = frappe.db.sql("""
		select (a.base_rate / a.conversion_factor)
		from `tabPurchase Invoice Item` a, `tabPurchase Invoice` b
		where a.item_code = %s and a.docstatus=1
		{0}
		order by b.posting_date desc limit 1""".format(condition), item_code)

	return float(last_purchase_rate[0][0]) if last_purchase_rate else 0.0