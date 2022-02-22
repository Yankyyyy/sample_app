# Copyright (c) 2013, Leader Group and contributors
# For license information, please see license.txt

import frappe
from frappe import _

def execute(filters=None):
# function to create a report on Project Tracker. Task DocType is selected as the base Doctype here
	filters.pop('date', None)
	columns, data = [], []
	columns = task_columns()
	task_name_list = frappe.db.get_list("Task", pluck = "name", filters = filters)
	for task_name in task_name_list:
		task_doc = frappe.db.get_value("Task", {"name" : task_name}, ['project', 'technical_manager', 'exp_start_date', 'exp_end_date', 'completed_on', 'description', 'type', 'status', 'issue', 'creation'], as_dict = 1)
		row_data = get_row_data(task_doc)
		data.append(row_data)
	return columns, data

def task_columns():
# function to define columns of the report
    return [
        {
	        "label": _("Project Name"),
	        "fieldname": "project_name",
	        "width": "100"
	    },
	    {
	        "label": _("Client Name"),
	        "fieldname": "client_name",
	        "width": "100"
	    },
	    {
	        "label": _("Activity Details"),
	        "fieldname": "activity_details",
	        "width": "200"
	    },
	    {
	        "label": _("Project Type"),
	        "fieldname": "project_type",
	        "width": "100"
	    },
	    {
	        "label": _("Class"),
	        "fieldname": "class",
	        "width": "100"
	    },
	    {
	        "label": _("Priority"),
	        "fieldname": "priority",
	        "width": "100"
	    },
	    {
	        "label": _("Technical Manager"),
	        "fieldname": "technical_manager",
	        "width": "100"
	    },
	    {
	        "label": _("Owner"),
	        "fieldname": "owner",
	        "width": "100"
	    },
	    {
	        "label": _("Initiation Date"),
	        "fieldname": "initiation_date",
	        "width": "100"
		},
	    {
	        "label": _("Expected Start Date"),
	        "fieldname": "expected_start_date",
	        "width": "100"
	    },
	    {
	        "label": _("Expected End Date"),
	        "fieldname": "expected_end_date",
	        "width": "100"
	    },
	    {
	        "label": _("Completed On"),
	        "fieldname": "completed_on",
	        "width": "100"
	    },
	    {
	        "label": _("Status"),
	        "fieldname": "status",
	        "width": "100"
	    },
	    {
	        "label": _("Issue"),
	        "fieldname": "issue",
	        "width": "100"
	    },
	    {
	        "label": _("Creation"),
	        "fieldname": "creation",
	        "width": "200"
	    }
	]

def get_row_data(task_data):
# function to assign data from fields in the Doctype to the respective columns in the report

	if task_data.project:
		project_data = frappe.get_doc("Project", {"name" : task_data.project})

	if task_data.technical_manager:
		task_data.technical_manager = frappe.db.get_value('User', task_data.technical_manager, 'full_name')

	if project_data.project_manager:
		project_data.project_manager = frappe.db.get_value('User', project_data.project_manager, 'full_name')

	initiation_date = expected_start_date = expected_end_date = completed_date = ''
	if project_data.expected_start_date:
		initiation_date = project_data.expected_start_date.strftime("%d-%m-%Y")
	
	if task_data.exp_start_date:
		expected_start_date = task_data.exp_start_date.strftime("%d-%m-%Y")

	if task_data.exp_end_date:
		expected_end_date = task_data.exp_end_date.strftime("%d-%m-%Y")

	if task_data.completed_on:
		completed_date = task_data.completed_on.strftime("%d-%m-%Y")

	assigned_data = {
		"project_name" : project_data.project_name,
		"client_name" : project_data.customer,
		"activity_details" : task_data.description,
		"project_type" : project_data.project_type,
		"class" : task_data.type,
		"priority": project_data.priority,
		"technical_manager": task_data.technical_manager,
		"owner" : project_data.project_manager,
		"initiation_date" : initiation_date,
		"expected_start_date" : expected_start_date,
		"expected_end_date" : expected_end_date, 
		"completed_on": completed_date,
		"status" : task_data.status,
		"issue": task_data.issue,
		"creation": task_data.creation.strftime("%d-%m-%Y")
	}
	return assigned_data