# Copyright (c) 2022, Leader Group and contributors
# For license information, please see license.txt

import frappe
from frappe import _

def execute(filters=None):
	columns, data = [], []
	columns = get_columns()
	data = get_data(filters, data)

	return columns, data

def get_data(filters, data):
	closing_debit = 0
	closing_credit = 0
	opening_balances = frappe.db.sql("""select sum(debit) as debit, sum(credit) as credit
		from `tabGL Entry`
		where company = %(company)s
			and is_cancelled = 0
			and (posting_date < %(from_date)s or ifnull(is_opening, 'No') = 'Yes')
			and cost_center = %(cost_center)s ; """, filters, as_dict = True)
			
	closing_debit, closing_credit = toggle_debit_credit(opening_balances[0].debit, opening_balances[0].credit)

	data.append({
		'date' : filters.get('from_date'),
		'description': "Opening Balance",
		'debit' : closing_debit,
		'credit' : closing_credit
	})

	gle = frappe.db.sql("""select posting_date as date, 
		remarks as description,
		debit, credit, voucher_type, voucher_no
		from `tabGL Entry`
		where company=%(company)s
			and is_cancelled = 0
			and posting_date >= %(from_date)s and posting_date <= %(to_date)s
			and ifnull(is_opening, 'No') = 'No'
			and cost_center = %(cost_center)s order by posting_date asc; """, filters, as_dict=True)

	if gle:
		for i in gle:
			i['debit'], i['credit'] = toggle_debit_credit(i.get('debit'), i.get('credit'))
			closing_debit += i.get('debit')
			closing_credit += i.get('credit')
		data.extend(gle)
		
	else:
		data.append({
			'debit': 0,
			'credit': 0
		})

	closing_debit, closing_credit = toggle_debit_credit(closing_debit, closing_credit)
	data.append({
		'date' : filters.get('to_date'),
		'description' : "Closing Balance",
		'debit': closing_debit,
		'credit': closing_credit
	})

	return data

def toggle_debit_credit(debit, credit):
	if debit > credit:
		debit = debit - credit
		credit = 0.0
	else:
		credit = credit - debit
		debit = 0.0

	return debit, credit

def get_columns():
	columns = [
		{
			"fieldname": "date",
			"label": _("Date"),
			"fieldtype": "Date",
			"width": 200
		},
		{
			"fieldname": "description",
			"label": _("Description"),
			"fieldtype": "Data",
			"width": 200
		},
		{
			"fieldname": "debit",
			"label": _("Debit"),
			"fieldtype": "Currency",
			"width": 200
		},
		{
			"fieldname": "credit",
			"label": _("Credit"),
			"fieldtype": "Currency",
			"width": 200
		},
		{
			"fieldname": "voucher_no",
			"label": _("Voucher Number"),
			"fieldtype": "Dynamic Link",
			"options": "voucher_type",
			"width": 200
		},
		{
			"fieldname": "voucher_type",
			"label": _("Voucher Type"),
			"fieldtype": "Link",
			"options": "DocType",
			"width": 150
		}
	]
	return columns