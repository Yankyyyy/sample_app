# Copyright (c) 2013, Leader Group and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from erpnext import get_company_currency, get_default_company


def execute(filters=None):
	columns, data = [], []
	columns = get_columns(filters)
	
	conditions, filters = get_conditions(filters)
	# get account list of Expense Account
	account_list = frappe.db.get_list('Account',
		filters = {
			'root_type': 'Expense',
			'is_group': 0
		},
		fields = ['name', 'account_number', 'account_name']
	)

	for account in account_list:
		amount = 0
		# get account total amount by debit amount minus credit amount from gl Entry
		gl_data = frappe.db.sql("""select account, (sum(debit) - sum(credit)) as amount
			from `tabGL Entry`
			where docstatus = 1 and is_cancelled != 1
				and account = '{0}' {1};""".format(account.get("name"),conditions),filters, as_dict=1)
		if gl_data:
			amount = gl_data[0].get("amount")
		
		if filters.get("show_zero_values"):
			# ignore amount only with none value
			if amount is not None:
				data.append({
					"account": account.get("name"),
					"account_number": account.get("account_number"),
					"account_name": account.get("account_name"),
					"amount": amount
				})
		else:
			# ignore amount with zero and none values
			if amount:
				data.append({
					"account": account.get("name"),
					"account_number": account.get("account_number"),
					"account_name": account.get("account_name"),
					"amount": amount
				})
	return columns, data

def get_columns(filters):
	columns = [
		{
			"fieldname": "account",
			"label": _("Account"),
			"fieldtype": "Link",
			"options": "Account",
			"width": 350
		},
		{
			"fieldname": "account_number",
			"label": _("Account #"),
			"fieldtype": "Data",
			"width": 120
		},
		{
			"fieldname": "account_name",
			"label": _("Account Name"),
			"fieldtype": "Data",
			"width": 300
		},
		{
			"fieldname": "amount",
			"label": _("Amount ({0})").format(get_company_currency(get_default_company())),
			"fieldtype": "Float",
			"width": 150
		}
	]
	return columns

def get_conditions(filters):
	conditions = ""
	if filters.get("from_date"):
		conditions += 'and posting_date >= %s' % frappe.db.escape(filters.get("from_date"), percent=False)
	if filters.get("to_date"):
		conditions += 'and posting_date <= %s' % frappe.db.escape(filters.get("to_date"), percent=False)
	if filters.get("project"):
		filters.project = frappe.parse_json(filters.get('project'))
		conditions += ' and project in %(project)s'
	return conditions, filters