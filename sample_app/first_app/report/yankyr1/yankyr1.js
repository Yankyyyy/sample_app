// Copyright (c) 2016, Yanky and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["YankyR1"] = {
	"filters": [
	{
		"label": ("Employee ID"),
		"fieldname": "employee_id_filter",
		"fieldtype": "Link",
		"options": "Employee"
	// },
	// {
	// 	"label": ("First Name"),
	// 	"fieldname": "first_name_filter",
	// 	"fetch from": "employee_id_filter.first_name"
	// },
	// {
	// 	"label": ("Second Name"),
	// 	"fieldname": "last_name_filter",
	// 	"fetch from": "employee_id_filter.last_name"
	// },
	// {
	// 	"label": ("Full Name"),
	// 	"fieldname": "employee_name_filter",
	// 	"fetch from": "employee_id_filter.employee_name"
	// },
	// {
	// 	"label": ("Phone Number"),
	// 	"fieldname": "cell_number_filter",
	// 	"fetch from": "employee_id_filter.cell_number"
	// },
	// {
	// 	"label": ("Email"),
	// 	"fieldname": "personal_email_filter",
	// 	"fetch from": "employee_id_filter.personal_email"
	}
	]
};
