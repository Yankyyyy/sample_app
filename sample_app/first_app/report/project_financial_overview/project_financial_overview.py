# Copyright (c) 2013, Leader Group and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.utils import date_diff, flt

def execute(filters=None):
    filters.pop('date', None)
    columns = get_columns()
    data = []
    data = frappe.db.get_all("Project",
            filters=filters,
            fields=["name",
                    "project_name",
                    'status',
                    "customer",
                    "expected_start_date",
                    "expected_end_date",
                    "project_manager",
                    "payment_collection_method",
                    "sales_order"
                ],
            order_by="expected_end_date")
    for project in data:
        project["project_manager"] = frappe.db.get_value('User', project.project_manager, 'full_name')         
        project_cost = flt(frappe.db.sql("""select ifnull(sum(debit), 0)
				from `tabJournal Entry Account` where project="%s" and docstatus=1""" %
				(project.name))[0][0])
        project["project_cost"] = project_cost
        if project.sales_order:
            project_value = frappe.db.get_value('Sales Order', project.sales_order, 'base_grand_total')
            project["margin_percentage"] = round(((project_value-project_cost)/project_value)*100) 
            invoiced_value = flt(frappe.db.sql("""select ifnull(sum(base_net_amount), 0)
				from `tabSales Invoice Item` where sales_order="%s" and docstatus=1""" %
				(project.sales_order))[0][0])
            collected_value = flt(frappe.db.sql("""select ifnull(sum(paid_amount), 0)
				from `tabPayment Entry` where project="%s" and docstatus=1""" %
				(project.name))[0][0])
            if invoiced_value:
                project["invoiced_percentage"] = round((invoiced_value/project_value)*100, 2)
            collected_invoiced_percentage = 0    
            if collected_value:
                collected_invoiced_percentage = round((collected_value/project_value)*100, 2)
            project["collected_invoiced_percentage"] = collected_invoiced_percentage   
            project["project_value"] = project_value
            project["invoiced_value"] = invoiced_value
            project["collected_value"] = collected_value
            if (invoiced_value - collected_value) > 0:
                project["balance_to_collect"] = invoiced_value - collected_value
                project["balance_to_collect_percentage"] = 100 - collected_invoiced_percentage
    return columns, data

def get_columns():
	return [
		{
			"fieldname": "customer",
			"label": _("Customer"),
			"fieldtype": "Link",
			"options": "Customer",
			"width": 150
		},
		{
			"fieldname": "project_name",
			"label": _("Project Name"),
			"fieldtype": "Data",
			"width": 150
		},
		{
			"fieldname": "project_manager",
			"label": _("Project Manager"),
			"fieldtype": "Data",
			"width": 120
		},
		{
			"fieldname": "expected_start_date",
			"label": _("Start Date"),
			"fieldtype": "Date",
			"width": 120
		},
		{
			"fieldname": "expected_end_date",
			"label": _("End Date"),
			"fieldtype": "Date",
			"width": 120
		},
		{
			"fieldname": "payment_collection_method",
			"label": _("Payment Type"),
			"fieldtype": "Data",
			"width": 120
		},
		{
			"fieldname": "status",
			"label": _("Status"),
			"fieldtype": "Data",
			"width": 120
		},
		{
			"fieldname": "project_cost",
			"label": _("Project Cost"),
			"fieldtype": "Data",
			"width": 120
		},
		{
			"fieldname": "project_value",
			"label": _("Project Value"),
			"fieldtype": "Data",
			"width": 120
		},
		{
			"fieldname": "margin_percentage",
			"label": _("Margin %"),
			"fieldtype": "Percent",
			"width": 120
		},
		{
			"fieldname": "invoiced_value",
			"label": _("Invoiced Value"),
			"fieldtype": "Data",
			"width": 120
		},
		{
			"fieldname": "invoiced_percentage",
			"label": _("Invoiced Deliverables %"),
			"fieldtype": "Percent",
			"width": 120
		},
		{
			"fieldname": "collected_value",
			"label": _("Collected Value"),
			"fieldtype": "Data",
			"width": 120
		},
		{
			"fieldname": "collected_invoiced_percentage",
			"label": _("Collected Invoiced %"),
			"fieldtype": "Percent",
			"width": 120
		},
		{
			"fieldname": "balance_to_collect",
			"label": _("Balance to Collect"),
			"fieldtype": "Data",
			"width": 120
		},
		{
			"fieldname": "balance_to_collect_percentage",
			"label": _("Balance to Collect %"),
			"fieldtype": "Percent",
			"width": 120
		}
	]