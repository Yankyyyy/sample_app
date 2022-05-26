# Copyright (c) 2013, Leader Group and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from erpnext.accounts.report.item_wise_sales_register.item_wise_sales_register import *

def execute(filters=None):
	return execute_one(filters)

def execute_one(filters=None, additional_table_columns=None, additional_query_columns=None):
	if not filters: filters = {}

	columns = set_columns(additional_table_columns, filters)

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
		
		delivery_note = None
		total_cost = 0
		unit_cost = 0
		if d.delivery_note:
			delivery_note = d.delivery_note
		elif d.so_detail:
			delivery_note = ", ".join(so_dn_map.get(d.so_detail, []))

		if not delivery_note and d.update_stock:
			delivery_note = d.parent

		if d.delivery_note:
			unit_cost = get_valuation_rate(d.item_code, d)
			total_cost = unit_cost * d.qty

			invoice_list = """select incoming_rate
				from `tabDelivery Note Item` DNI 
					inner join `tabDelivery Note` DN on DN.name = DNI.parent
				where DN.name = '{0}' 
					-- and DN.is_return =1 
					and DNI.item_code = '{1}'
				""".format(d.delivery_note, d.item_code)
			invoice_list = frappe.db.sql(invoice_list, as_dict=1)

			if invoice_list:
				unit_cost = invoice_list[0].get("incoming_rate")
				total_cost = unit_cost * d.qty
		
		if total_cost == 0 and d.base_net_amount ==0:
			continue

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

def get_valuation_rate(item_code, row):
	valuation_rate = 0
	if frappe.db.exists('Product Bundle', item_code):
		bundle_item = frappe.get_all(
			'Product Bundle Item',
			filters = {
				'parent': item_code
			},
			fields = ['item_code', 'qty']
		)
		for item in bundle_item:
			valuation_rate += get_item_valuation_rate(item.get("item_code"), row) * item.get("qty")
	else:
		valuation_rate += get_item_valuation_rate(item_code, row)
	return valuation_rate

def get_item_valuation_rate(item_code, row):
	item_valuation_rate = 0
	condition = "AND sle.posting_date <= '%s'" % (row.posting_date)
	if row.project:
		condition += " AND sle.project=%s" % (frappe.db.escape(row.project))

	valuation_rate = frappe.db.sql("""select
			valuation_rate
		from
			`tabStock Ledger Entry` sle
		where
			sle.item_code = %s and sle.docstatus=1
			{0}
		order by sle.modified desc limit 1""".format(condition), item_code)

	if valuation_rate:
		item_valuation_rate = flt(valuation_rate[0][0])
	else:
		item_valuation_rate = frappe.db.get_value("Item", item_code, "valuation_rate")
	return item_valuation_rate


def set_columns(additional_table_columns, filters):
	columns = []

	if filters.get('group_by') != ('Item'):
		columns.extend(
			[
				{
					'label': _('Item Code'),
					'fieldname': 'item_code',
					'fieldtype': 'Link',
					'options': 'Item',
					'width': 120
				},
				{
					'label': _('Item Name'),
					'fieldname': 'item_name',
					'fieldtype': 'Data',
					'width': 120
				}
			]
		)

	if filters.get('group_by') not in ('Item', 'Item Group'):
		columns.extend([
			{
				'label': _('Item Group'),
				'fieldname': 'item_group',
				'fieldtype': 'Link',
				'options': 'Item Group',
				'width': 120
			}
		])

	columns.extend([
		{
			'label': _('Description'),
			'fieldname': 'description',
			'fieldtype': 'Data',
			'width': 150
		},
		{
			'label': _('Invoice'),
			'fieldname': 'invoice',
			'fieldtype': 'Link',
			'options': 'Sales Invoice',
			'width': 120
		},
		{
			'label': _('Posting Date'),
			'fieldname': 'posting_date',
			'fieldtype': 'Date',
			'width': 120
		}
	])

	if filters.get('group_by') != 'Customer':
		columns.extend([
			{
				'label': _('Customer Group'),
				'fieldname': 'customer_group',
				'fieldtype': 'Link',
				'options': 'Customer Group',
				'width': 120
			}
		])

	if filters.get('group_by') not in ('Customer', 'Customer Group'):
		columns.extend([
			{
				'label': _('Customer'),
				'fieldname': 'customer',
				'fieldtype': 'Link',
				'options': 'Customer',
				'width': 120
			},
			{
				'label': _('Customer Name'),
				'fieldname': 'customer_name',
				'fieldtype': 'Data',
				'width': 120
			}
		])

	if additional_table_columns:
		columns += additional_table_columns

	columns += [
		{
			'label': _('Receivable Account'),
			'fieldname': 'debit_to',
			'fieldtype': 'Link',
			'options': 'Account',
			'width': 80
		},
		{
			'label': _('Mode Of Payment'),
			'fieldname': 'mode_of_payment',
			'fieldtype': 'Data',
			'width': 120
		}
	]

	if filters.get('group_by') != 'Territory':
		columns.extend([
			{
				'label': _('Territory'),
				'fieldname': 'territory',
				'fieldtype': 'Link',
				'options': 'Territory',
				'width': 80
			}
		])


	columns += [
		{
			'label': _('Project'),
			'fieldname': 'project',
			'fieldtype': 'Link',
			'options': 'Project',
			'width': 80
		},
		{
			'label': _('Company'),
			'fieldname': 'company',
			'fieldtype': 'Link',
			'options': 'Company',
			'width': 80
		},
		{
			'label': _('Sales Order'),
			'fieldname': 'sales_order',
			'fieldtype': 'Link',
			'options': 'Sales Order',
			'width': 100
		},
		{
			'label': _("Delivery Note"),
			'fieldname': 'delivery_note',
			'fieldtype': 'Link',
			'options': 'Delivery Note',
			'width': 100
		},
		{
			'label': _('Income Account'),
			'fieldname': 'income_account',
			'fieldtype': 'Link',
			'options': 'Account',
			'width': 100
		},
		{
			'label': _("Cost Center"),
			'fieldname': 'cost_center',
			'fieldtype': 'Link',
			'options': 'Cost Center',
			'width': 100
		},
		{
			'label': _('Stock Qty'),
			'fieldname': 'stock_qty',
			'fieldtype': 'Float',
			'width': 100
		},
		{
			'label': _('Stock UOM'),
			'fieldname': 'stock_uom',
			'fieldtype': 'Link',
			'options': 'UOM',
			'width': 100
		},
		{
			'label': _('Rate'),
			'fieldname': 'rate',
			'fieldtype': 'Float',
			'options': 'currency',
			'width': 100
		},
		{
			'label': _('Amount'),
			'fieldname': 'amount',
			'fieldtype': 'Currency',
			'options': 'currency',
			'width': 100
		},
		{
			'label': _('Unit Cost'),
			'fieldname': 'unit_cost',
			'fieldtype': 'Currency',
			'options': 'currency',
			'width': 100
		},
		{
			'label': _('Total Cost'),
			'fieldname': 'total_cost',
			'fieldtype': 'Currency',
			'options': 'currency',
			'width': 100
		},
		{
			'label': _('Profit'),
			'fieldname': 'profit',
			'fieldtype': 'Currency',
			'options': 'currency',
			'width': 100
		}
	]

	if filters.get('group_by'):
		columns.append({
			'label': _('% Of Grand Total'),
			'fieldname': 'percent_gt',
			'fieldtype': 'Float',
			'width': 80
		})

	return columns
