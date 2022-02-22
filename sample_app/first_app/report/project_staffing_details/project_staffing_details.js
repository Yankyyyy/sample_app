// Copyright (c) 2016, Leader Group and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Project Staffing Details"] = {
	"filters": [
		{
			"fieldname": "customer",
			"label": __("Customer"),
			"fieldtype": "Link",
			"options": "Customer"
		},
		{
			"fieldname": "name",
			"label": __("Project"),
			"fieldtype": "Link",
			"options": "Project"
		},
		{
			"fieldname": "date",
			"label": __("Printed On"),
			"fieldtype": "Data",
			"default": moment(frappe.datetime.now_datetime()).format("MM-DD-YYYY HH:mm:ss"),
            read_only: 1
		}
	]
};