# Copyright (c) 2013, Yanky and contributors
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
                    "customer",
                    "expected_start_date",
                    "expected_end_date",
                    "project_manager",
                    "staff_count_as_per_rfb",
                ],
            order_by="name")
    
    for project in data:
        if project.expected_end_date and project.expected_start_date:
            total_months = round(flt(date_diff(project.expected_end_date, project.expected_start_date)/30),2)
        else:
            total_months = ""
        if project.expected_end_date:
            months_remaining = round(flt(date_diff(project.expected_end_date, frappe.utils.nowdate())/30),2)
        else:
            months_remaining = ""
        project["project_manager"] = frappe.db.get_value('User', project.project_manager, 'full_name')
        project["total_months"] = total_months       
        project["months_remaining"] = months_remaining
        if project.staff_count_as_per_rfb:
            current_staff_count = frappe.db.count('Project User', filters={"parent":project.name})
        else:
            current_staff_count = ""
        project["current_staff_count"] = current_staff_count
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
			"fieldname": "name",
			"label": _("Project"),
			"fieldtype": "Link",
			"options": "Project",
			"width": 200
		},
		{
			"fieldname": "project_manager",
			"label": _("Project Manager"),
			"fieldtype": "Data",
			"width": 200
		},
		{
			"fieldname": "current_staff_count",
			"label": _("Current Staff Count"),
			"fieldtype": "Data",
			"width": 150
		},
		{
			"fieldname": "staff_count_as_per_rfb",
			"label": _("Staff Count as per rfb"),
			"fieldtype": "Int",
			"width": 150
		},
		{
			"fieldname": "total_months",
			"label": _("Project Lifetime(months)"),
			"fieldtype": "Data",
			"width": 150
		},
		{
			"fieldname": "months_remaining",
			"label": _("Remaining Time(months)"),
			"fieldtype": "Data",
			"width": 150
		}
	]