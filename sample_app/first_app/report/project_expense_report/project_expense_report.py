# Copyright (c) 2013, Leader Group and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from erpnext import get_company_currency, get_default_company


def execute(filters=None):
	columns, data = [], []
	columns = get_columns(filters)
	
	conditions = get_conditions(filters)
	#returning all je account child table data accoridng to project chosen and Expense account and Date
	je_data = frappe.db.sql("""select 
								jea.account,jea.debit_in_account_currency,jea.credit_in_account_currency 
								from 
								`tabJournal Entry Account` jea , `tabJournal Entry` je
								where
								jea.parent = je.name  and
								jea.account in (select name from `tabAccount` where root_type='Expense') 
								%s""" %conditions, as_dict=1)
								

	for je_row in je_data:
		row_dict ={
			"account_number": frappe.db.get_value("Account",je_row.get("account"),"account_number"),
			"account_name":frappe.db.get_value("Account",je_row.get("account"),"account_name"),
			"amount":je_row.get("debit_in_account_currency")
		}
		data.append(row_dict)
	return columns, data

def get_columns(filters):
	columns = []
	columns.extend( 
		[
		{
		"fieldname": "account_number",
		"label": _("Account #"),
		"fieldtype": "Data",
		"width": 120
		}, 
		{
			"fieldname": "account_name",
			"label": _("Account Name"),
			"fieldtype": "Link",
			"options": "Account",
			"width": 200
		},
		{
			"fieldname": "amount",
			"label": _("Amount ({0})").format(get_company_currency(get_default_company())),
			"fieldtype": "Float",
			"width": 120
		}
		]
	)
	return columns

def get_conditions(filters):
	conditions=""
	if filters.get("from_date"):
		conditions += 'and je.posting_date >= %s'  % frappe.db.escape(filters.get("from_date"), percent=False)
	if filters.get("to_date"):
		conditions +='and je.posting_date <= %s' % frappe.db.escape(filters.get("to_date"), percent=False)
	if filters.get("project"):
		conditions +='and jea.project = %s' % frappe.db.escape(filters.get("project"), percent=False)
	return conditions