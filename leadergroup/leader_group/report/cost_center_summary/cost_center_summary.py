# Copyright (c) 2022, Leader Group and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.utils import cint, flt


def execute(filters=None):
	columns = get_columns()
	data = get_data(filters)

	return columns, data

def get_data(filters):
	cost_center_list = frappe.get_list("Cost Center", 
                filters={
        			'company': filters.company
    			},order_by="name")
	company_currency = frappe.get_cached_value('Company',  filters.company,  "default_currency")
	opening_balances = get_opening_balances(filters)
	balances_within_period = get_balances_within_period(filters)

	data = []
	# total_debit, total_credit = 0, 0
	total_row = frappe._dict({
		"opening_debit": 0,
		"opening_credit": 0,
		"debit": 0,
		"credit": 0,
		"closing_debit": 0,
		"closing_credit": 0
	})
	for cost_center in cost_center_list:
		row = { "cost_center": cost_center.name }

		# opening
		opening_debit, opening_credit = opening_balances.get(cost_center.name, [0, 0])
		row.update({
			"opening_debit": opening_debit,
			"opening_credit": opening_credit
		})

		# within period
		debit, credit = balances_within_period.get(cost_center.name, [0, 0])
		row.update({
			"debit": debit,
			"credit": credit
		})

		# closing
		closing_debit, closing_credit = toggle_debit_credit(opening_debit + debit, opening_credit + credit)
		row.update({
			"closing_debit": closing_debit,
			"closing_credit": closing_credit
		})

		row.update({
			"currency": company_currency
		})

		has_value = False
		if (opening_debit or opening_credit or debit or credit or closing_debit or closing_credit):
			has_value  =True

		if cint(filters.show_zero_values) or has_value:
			data.append(row)

	return data

def get_opening_balances(filters):
	gle = frappe.db.sql("""
		select cost_center as name, 
		sum(debit) as opening_debit, sum(credit) as opening_credit
		from `tabGL Entry`
		where company=%(company)s
			and is_cancelled=0
			and (posting_date < %(from_date)s or ifnull(is_opening, 'No') = 'Yes')
		group by cost_center""",filters, as_dict=True)

	opening = frappe._dict()
	for d in gle:
		opening_debit, opening_credit = toggle_debit_credit(d.opening_debit, d.opening_credit)
		opening.setdefault(d.name, [opening_debit, opening_credit])

	return opening

def get_balances_within_period(filters):
	gle = frappe.db.sql("""
		select cost_center as name, 
		sum(debit) as debit, sum(credit) as credit
		from `tabGL Entry`
		where company=%(company)s
			and is_cancelled = 0
			and posting_date >= %(from_date)s and posting_date <= %(to_date)s
			and ifnull(is_opening, 'No') = 'No'
		group by cost_center""",filters, as_dict=True)

	balances_within_period = frappe._dict()
	for d in gle:
		balances_within_period.setdefault(d.name, [d.debit, d.credit])

	return balances_within_period

def toggle_debit_credit(debit, credit):
	if flt(debit) > flt(credit):
		debit = flt(debit) - flt(credit)
		credit = 0.0
	else:
		credit = flt(credit) - flt(debit)
		debit = 0.0

	return debit, credit

def get_columns():
	columns = [
		{
			"fieldname": "cost_center",
			"label": _("Cost Center"),
			"fieldtype": "Link",
			"options": "Cost Center",
			"width": 200
		},
		{
			"fieldname": "opening_debit",
			"label": _("Opening (Dr)"),
			"fieldtype": "Currency",
			"options": "currency",
			"width": 150
		},
		{
			"fieldname": "opening_credit",
			"label": _("Opening (Cr)"),
			"fieldtype": "Currency",
			"options": "currency",
			"width": 150
		},
		{
			"fieldname": "debit",
			"label": _("Debit"),
			"fieldtype": "Currency",
			"options": "currency",
			"width": 150
		},
		{
			"fieldname": "credit",
			"label": _("Credit"),
			"fieldtype": "Currency",
			"options": "currency",
			"width": 150
		},
		{
			"fieldname": "closing_debit",
			"label": _("Closing (Dr)"),
			"fieldtype": "Currency",
			"options": "currency",
			"width": 150
		},
		{
			"fieldname": "closing_credit",
			"label": _("Closing (Cr)"),
			"fieldtype": "Currency",
			"options": "currency",
			"width": 150
		},
		{
			"fieldname": "currency",
			"label": _("Currency"),
			"fieldtype": "Link",
			"options": "Currency",
			"hidden": 1
		}
	]
	return columns