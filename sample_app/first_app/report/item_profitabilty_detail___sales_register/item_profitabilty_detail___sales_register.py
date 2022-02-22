# Copyright (c) 2013, Leader Group and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from erpnext.erpnext.accounts.report.item_wise_sales_register.item_wise_sales_register import *

def execute(filters=None):
	return execute_one(filters)

def execute_one(filters=None, additional_table_columns=None, additional_query_columns=None):
	if not filters: filters = {}
	additional_table_columnss = [
		dict(fieldtype='Data', label='Unit Cost', fieldname="unit_cost", width=120),
		dict(fieldtype='Data', label='Total Cost', fieldname="total_cost", width=120),
		dict(fieldtype='Data', label='Profit', fieldname="profit", width=120)
	]
	columns = get_columns(additional_table_columnss, filters)

	company_currency = frappe.get_cached_value('Company',  filters.get('company'),  'default_currency')

	item_list = get_items(filters, additional_query_columns)
	if item_list:
		itemised_tax, tax_columns = get_tax_accounts(item_list, columns, company_currency)

	mode_of_payments = get_mode_of_payments(set(d.parent for d in item_list))
	so_dn_map = get_delivery_notes_against_sales_order(item_list)

	data = []
	total_row_map = {}
	skip_total_row = 0
	prev_group_by_value = ''

	if filters.get('group_by'):
		grand_total = get_grand_total(filters, 'Sales Invoice')

	customer_details = get_customer_details()
	item_details = get_item_details()

	for d in item_list:
		customer_record = customer_details.get(d.customer)
		item_record = item_details.get(d.item_code)
		item_val_rate = frappe.get_doc("Item", {"item_code" : d.item_code},["valuation_rate"])
		if item_val_rate.valuation_rate:
			unit_cost = item_val_rate.valuation_rate
		else:
			unit_cost = get_last_purchase_rate(filters, d.item_code, d)
		total_cost = unit_cost * d.qty

		if total_cost == 0 and d.base_net_amount ==0:
			continue
		
		delivery_note = None
		if d.delivery_note:
			delivery_note = d.delivery_note
		elif d.so_detail:
			delivery_note = ", ".join(so_dn_map.get(d.so_detail, []))

		if not delivery_note and d.update_stock:
			delivery_note = d.parent

		row = {
			'item_code': d.item_code,
			'item_name': item_record.item_name if item_record else d.item_name,
			'item_group': item_record.item_group if item_record else d.item_group,
			'description': d.description,
			'invoice': d.parent,
			'posting_date': d.posting_date,
			'customer': d.customer,
			'customer_name': customer_record.customer_name,
			'customer_group': customer_record.customer_group,
		}

		if additional_query_columns:
			for col in additional_query_columns:
				row.update({
					col: d.get(col)
				})

		row.update({
			'debit_to': d.debit_to,
			'mode_of_payment' : ", ".join(mode_of_payments.get(d.parent, [])),
			'territory': d.territory,
			'project': d.project,
			'company': d.company,
			'sales_order': d.sales_order,
			'delivery_note': d.delivery_note,
			'income_account': d.unrealized_profit_loss_account if d.is_internal_customer == 1 else d.income_account,
			'cost_center': d.cost_center,
			'stock_qty': d.stock_qty,
			'stock_uom': d.stock_uom,
			'unit_cost' : unit_cost,
			"total_cost" : total_cost,
			"profit" : d.base_net_amount - total_cost
		})

		if d.stock_uom != d.uom and d.stock_qty:
			row.update({
				'rate': (d.base_net_rate * d.qty)/d.stock_qty,
				'amount': d.base_net_amount
			})
		else:
			row.update({
				'rate': d.base_net_rate,
				'amount': d.base_net_amount
			})

		total_tax = 0
		for tax in tax_columns:
			item_tax = itemised_tax.get(d.name, {}).get(tax, {})
			row.update({
				frappe.scrub(tax + ' Rate'): item_tax.get('tax_rate', 0),
				frappe.scrub(tax + ' Amount'): item_tax.get('tax_amount', 0),
			})
			total_tax += flt(item_tax.get('tax_amount'))

		row.update({
			'total_tax': total_tax,
			'total': d.base_net_amount + total_tax,
			'currency': company_currency
		})

		if filters.get('group_by'):
			row.update({'percent_gt': flt(row['total']/grand_total) * 100})
			group_by_field, subtotal_display_field = get_group_by_and_display_fields(filters)
			data, prev_group_by_value = add_total_row(data, filters, prev_group_by_value, d, total_row_map,
				group_by_field, subtotal_display_field, grand_total, tax_columns)
			add_sub_total_row(row, total_row_map, d.get(group_by_field, ''), tax_columns)

		data.append(row)

	if filters.get('group_by') and item_list:
		total_row = total_row_map.get(prev_group_by_value or d.get('item_name'))
		total_row['percent_gt'] = flt(total_row['total']/grand_total * 100)
		data.append(total_row)
		data.append({})
		add_sub_total_row(total_row, total_row_map, 'total_row', tax_columns)
		data.append(total_row_map.get('total_row'))
		skip_total_row = 1

	return columns, data, None, None, None, skip_total_row



def get_last_purchase_rate(filters, item_code, row):
		condition = ''
		if row.project:
			condition += " AND a.project=%s" % (frappe.db.escape(row.project))
		elif row.cost_center:
			condition += " AND a.cost_center=%s" % (frappe.db.escape(row.cost_center))
		if filters.to_date:
			condition += " AND modified <='%s'" % (filters.to_date)

		last_purchase_rate = frappe.db.sql("""
		select (a.base_rate / a.conversion_factor)
		from `tabPurchase Invoice Item` a
		where a.item_code = %s and a.docstatus=1
		{0}
		order by a.modified desc limit 1""".format(condition), item_code)

		return flt(last_purchase_rate[0][0]) if last_purchase_rate else 0

