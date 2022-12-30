# Copyright (c) 2022, Leader Group and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from erpnext import get_company_currency, get_default_company
from erpnext.accounts.report.financial_statements import get_cost_centers_with_children

def execute(filters=None):
	columns, data = [], []
	columns = get_columns(filters)
	
	conditions, filters = get_conditions(filters)

	data = frappe.db.sql("""select A.name, A.account_name, 
		A.account_number, 
		sum(GL.debit) as debit, sum(GL.credit) as credit
		from `tabGL Entry` GL
		left join `tabAccount` A
			on A.name = GL.account
		where GL.docstatus = 1 and GL.is_cancelled = 0 
			{0} group by GL.account;""".format(conditions),filters, as_dict=1)
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
			"fieldname": "debit",
			"label": _("Debit ({0})").format(get_company_currency(get_default_company())),
			"fieldtype": "Float",
			"width": 120
		},
		{
			"fieldname": "credit",
			"label": _("Credit ({0})").format(get_company_currency(get_default_company())),
			"fieldtype": "Float",
			"width": 120
		}
		]
	)
	return columns


def get_conditions(filters):
	conditions=""
	if filters.get("from_date"):
		conditions += ' and posting_date >= %s'  % frappe.db.escape(filters.get("from_date"), percent=False)
	if filters.get("to_date"):
		conditions += ' and posting_date <= %s' % frappe.db.escape(filters.get("to_date"), percent=False)
	if filters.get("cost_center"):
		conditions += ' and cost_center in %(cost_center)s'
		filters.cost_center = frappe.parse_json(filters.get('cost_center'))
		filters.cost_center = get_cost_centers_with_children(filters.cost_center)
	return conditions, filters