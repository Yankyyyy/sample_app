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
        if not project.expected_end_date or project.status == "Completed":
            days_remaining = 0
        else:
            days_remaining = date_diff(project.expected_end_date, frappe.utils.nowdate())
        project["project_manager"] = frappe.db.get_value('User', project.project_manager, 'full_name')         
        project["days_remaining"] = days_remaining
        if (not project.expected_end_date and not project.expected_start_date) or project.status == "Completed":
            percentage_days_remaining = 0
        else:
            percentage_days_remaining = round(flt(days_remaining/date_diff(project.expected_end_date, project.expected_start_date)),2)
        project["percentage_days_remaining"] = percentage_days_remaining
        if project.sales_order:
            project_value = frappe.db.get_value('Sales Order', project.sales_order, 'grand_total')
            delivered_value = flt(frappe.db.sql("""select ifnull(sum(amount), 0)
				from `tabDelivery Note Item` where against_sales_order="%s" and docstatus=1""" %
				(project.sales_order))[0][0])  
            invoiced_value = flt(frappe.db.sql("""select ifnull(sum(base_net_amount), 0)
				from `tabSales Invoice Item` where sales_order="%s" and docstatus=1""" %
				(project.sales_order))[0][0])
            collected_value = flt(frappe.db.sql("""select ifnull(sum(paid_amount), 0)
				from `tabPayment Entry` where project="%s" and docstatus=1""" %
				(project.name))[0][0])
            if delivered_value and project_value:    
                project["delivery_percentage"] = round((delivered_value/project_value)*100, 2)
            if invoiced_value and delivered_value:
                project["invoiced_percentage"] = round((invoiced_value/delivered_value)*100, 2)
            if collected_value and invoiced_value:
                project["collected_invoiced_percentage"] = round((collected_value/invoiced_value)*100, 2)
            project["project_value"] = project_value
            project["delivered_value"] = delivered_value
            project["invoiced_value"] = invoiced_value
            project["collected_value"] = collected_value      
    return columns, data

def get_columns():
	return [
		{
			"fieldname": "customer",
			"label": _("Customer"),
			"fieldtype": "Link",
			"options": "Customer",
			"width": 200
		},
		{
			"fieldname": "project_name",
			"label": _("Project"),
			"fieldtype": "Data",
			"width": 200
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
			"fieldname": "days_remaining",
			"label": _("Days Remaining"),
			"fieldtype": "Data",
			"width": 120
		},
		{
			"fieldname": "percentage_days_remaining",
			"label": _("Percentage of Days Remaining"),
			"fieldtype": "Percent",
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
			"fieldname": "delivery_percentage",
			"label": _("Delivery %"),
			"fieldtype": "Percent",
			"width": 120
		},
		{
			"fieldname": "invoiced_percentage",
			"label": _("Invoiced Deliverables %"),
			"fieldtype": "Percent",
			"width": 120
		},
		{
			"fieldname": "collected_invoiced_percentage",
			"label": _("Collected Invoiced %"),
			"fieldtype": "Percent",
			"width": 120
		},
		{
			"fieldname": "project_value",
			"label": _("Project Value"),
			"fieldtype": "Data",
			"width": 120
		},
		{
			"fieldname": "delivered_value",
			"label": _("Delivered Value"),
			"fieldtype": "Data",
			"width": 120
		},
		{
			"fieldname": "invoiced_value",
			"label": _("Invoiced Value"),
			"fieldtype": "Data",
			"width": 120
		},
		{
			"fieldname": "collected_value",
			"label": _("Collected Value"),
			"fieldtype": "Data",
			"width": 120
		}
	]