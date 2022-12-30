# Copyright (c) 2022, Leader Group and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.utils import cint, flt

from erpnext.accounts.report.trial_balance.trial_balance import validate_filters
from erpnext.accounts.doctype.accounting_dimension.accounting_dimension import (
	get_accounting_dimensions,
	get_dimension_with_children,
)
from erpnext.accounts.report.financial_statements import get_cost_centers_with_children


def execute(filters=None):
	validate_filters(filters)

	show_party_name = is_party_name_visible(filters)

	columns = get_columns(filters, show_party_name)
	data = get_data(filters, show_party_name)

	return columns, data

def get_data(filters, show_party_name):
	if filters.get('party_type') in ('Customer', 'Supplier', 'Employee', 'Member'):
		party_name_field = "{0}_name".format(frappe.scrub(filters.get('party_type')))
	elif filters.get('party_type') == 'Student':
		party_name_field = 'first_name'
	elif filters.get('party_type') == 'Shareholder':
		party_name_field = 'title'
	else:
		party_name_field = 'name'

	if filters.get('cost_center'):
		filters.cost_center = frappe.parse_json(filters.get('cost_center'))

	if filters.get('project'):
		filters.project = frappe.parse_json(filters.get('project'))

	party_filters = {"name": filters.get("party")} if filters.get("party") else {}
	parties = frappe.get_all(filters.get("party_type"), fields = ["name", party_name_field],
		filters = party_filters, order_by="name")
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
	for party in parties:
		row = { "party": party.name }
		if show_party_name:
			row["party_name"] = party.get(party_name_field)

		# opening
		opening_debit, opening_credit = opening_balances.get(party.name, [0, 0])
		row.update({
			"opening_debit": opening_debit,
			"opening_credit": opening_credit
		})

		# within period
		debit, credit = balances_within_period.get(party.name, [0, 0])
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

		# totals
		for col in total_row:
			total_row[col] += row.get(col)

		row.update({
			"currency": company_currency
		})

		has_value = False
		if (opening_debit or opening_credit or debit or credit or closing_debit or closing_credit):
			has_value  =True

		if cint(filters.show_zero_values) or has_value:
			data.append(row)

	# Add total row

	total_row.update({
		"party": "'" + _("Totals") + "'",
		"currency": company_currency
	})
	data.append(total_row)

	return data

def get_opening_balances(filters):
	gle = frappe.db.sql("""
		select party, sum(debit) as opening_debit, sum(credit) as opening_credit
		from `tabGL Entry`
		where company=%(company)s
			and is_cancelled=0
			and ifnull(party_type, '') = %(party_type)s and ifnull(party, '') != ''
			and (posting_date < %(from_date)s or ifnull(is_opening, 'No') = 'Yes')
			{conditions}
		group by party""".format(conditions=get_conditions(filters)),filters, as_dict=True)

	opening = frappe._dict()
	for d in gle:
		opening_debit, opening_credit = toggle_debit_credit(d.opening_debit, d.opening_credit)
		opening.setdefault(d.party, [opening_debit, opening_credit])

	return opening

def get_balances_within_period(filters):
	gle = frappe.db.sql("""
		select party, sum(debit) as debit, sum(credit) as credit
		from `tabGL Entry`
		where company=%(company)s
			and is_cancelled = 0
			and ifnull(party_type, '') = %(party_type)s and ifnull(party, '') != ''
			and posting_date >= %(from_date)s and posting_date <= %(to_date)s
			and ifnull(is_opening, 'No') = 'No'
			{conditions} 
		group by party""".format(conditions=get_conditions(filters)),filters, as_dict=True)

	balances_within_period = frappe._dict()
	for d in gle:
		balances_within_period.setdefault(d.party, [d.debit, d.credit])

	return balances_within_period

def toggle_debit_credit(debit, credit):
	if flt(debit) > flt(credit):
		debit = flt(debit) - flt(credit)
		credit = 0.0
	else:
		credit = flt(credit) - flt(debit)
		debit = 0.0

	return debit, credit

def get_conditions(filters):
	conditions = []

	if filters.get('account'):
		conditions.append("account = %(account)s")
	
	if filters.get('cost_center'):
		filters.cost_center = get_cost_centers_with_children(filters.cost_center)
		conditions.append("cost_center in %(cost_center)s")
	
	if filters.get('project'):
		conditions.append("project in %(project)s")

	accounting_dimensions = get_accounting_dimensions(as_list=False)
	if accounting_dimensions:
		for dimension in accounting_dimensions:
			if not dimension.disabled:
				if filters.get(dimension.fieldname):
					if frappe.get_cached_value('DocType', dimension.document_type, 'is_tree'):
						filters[dimension.fieldname] = get_dimension_with_children(dimension.document_type,
							filters.get(dimension.fieldname))
						conditions.append("{0} in %({0})s".format(dimension.fieldname))
					else:
						conditions.append("{0} in (%({0})s)".format(dimension.fieldname))
	
	return "and {}".format(" and ".join(conditions)) if conditions else ""

def get_columns(filters, show_party_name):
	columns = [
		{
			"fieldname": "party",
			"label": _(filters.party_type),
			"fieldtype": "Link",
			"options": filters.party_type,
			"width": 200
		},
		{
			"fieldname": "opening_debit",
			"label": _("Opening (Dr)"),
			"fieldtype": "Currency",
			"options": "currency",
			"width": 120
		},
		{
			"fieldname": "opening_credit",
			"label": _("Opening (Cr)"),
			"fieldtype": "Currency",
			"options": "currency",
			"width": 120
		},
		{
			"fieldname": "debit",
			"label": _("Debit"),
			"fieldtype": "Currency",
			"options": "currency",
			"width": 120
		},
		{
			"fieldname": "credit",
			"label": _("Credit"),
			"fieldtype": "Currency",
			"options": "currency",
			"width": 120
		},
		{
			"fieldname": "closing_debit",
			"label": _("Closing (Dr)"),
			"fieldtype": "Currency",
			"options": "currency",
			"width": 120
		},
		{
			"fieldname": "closing_credit",
			"label": _("Closing (Cr)"),
			"fieldtype": "Currency",
			"options": "currency",
			"width": 120
		},
		{
			"fieldname": "currency",
			"label": _("Currency"),
			"fieldtype": "Link",
			"options": "Currency",
			"hidden": 1
		}
	]

	if show_party_name:
		columns.insert(1, {
			"fieldname": "party_name",
			"label": _(filters.party_type) + " Name",
			"fieldtype": "Data",
			"width": 200
		})

	return columns

def is_party_name_visible(filters):
	show_party_name = False

	if filters.get('party_type') in ['Customer', 'Supplier']:
		if filters.get("party_type") == "Customer":
			party_naming_by = frappe.db.get_single_value("Selling Settings", "cust_master_name")
		else:
			party_naming_by = frappe.db.get_single_value("Buying Settings", "supp_master_name")

		if party_naming_by == "Naming Series":
			show_party_name = True
	else:
		show_party_name = True

	return show_party_name

