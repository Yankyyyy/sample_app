from __future__ import unicode_literals
import frappe
import json
from frappe.utils import nowdate, get_year_start, get_year_ending, format_date

@frappe.whitelist()
def getGeneralLedger():
    # General Ledger Report API with data
    from erpnext.accounts.report.general_ledger.general_ledger import execute
    filters = {}
    if frappe.request.data:
        filters = json.loads(frappe.request.data)

    if not filters.get('company'):
        filters['company'] = frappe.defaults.get_user_default("Company") or frappe.defaults.get_global_default("Company")
    
    if not filters.get('from_date'):
        filters['from_date'] = format_date(get_year_start(nowdate()), "yyyy-mm-dd")
    
    if not filters.get('to_date'):
        filters['to_date'] = format_date(get_year_ending(nowdate()), "yyyy-mm-dd")
    
    if not filters.get('group_by'):
        filters['group_by'] = 'Group by Voucher (Consolidated)'

    if not filters.get('include_dimensions'):
        filters['include_dimensions'] = 1

    filters = frappe._dict(filters)
    columns, res = execute(filters)
    return res


@frappe.whitelist()
def getStockLedger():
    # Stock Ledger Report API with data
    from erpnext.stock.report.stock_ledger.stock_ledger import execute
    filters = {}
    if frappe.request.data:
        filters = json.loads(frappe.request.data)

    if not filters.get('company'):
        filters['company'] = frappe.defaults.get_user_default("Company") or frappe.defaults.get_global_default("Company")

    if not filters.get('from_date'):
        filters['from_date'] = format_date(get_year_start(nowdate()), "yyyy-mm-dd")

    if not filters.get('to_date'):
        filters['to_date'] = format_date(get_year_ending(nowdate()), "yyyy-mm-dd")

    filters = frappe._dict(filters)
    columns, res = execute(filters)
    return res


@frappe.whitelist()
def getSalesRegister():
    # Sales Register Report API with data
    from erpnext.accounts.report.sales_register.sales_register import execute
    filters = {}
    if frappe.request.data:
        filters = json.loads(frappe.request.data)

    if not filters.get('company'):
        filters['company'] = frappe.defaults.get_user_default("Company") or frappe.defaults.get_global_default("Company")

    if not filters.get('from_date'):
        filters['from_date'] = format_date(get_year_start(nowdate()), "yyyy-mm-dd")

    if not filters.get('to_date'):
        filters['to_date'] = format_date(get_year_ending(nowdate()), "yyyy-mm-dd")

    filters = frappe._dict(filters)
    columns, res = execute(filters)
    return res