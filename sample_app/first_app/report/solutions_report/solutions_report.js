// Copyright (c) 2016, Leader Group and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Solutions Report"] = {
	"filters": [
		{
			"fieldname": "parent",
			"label": __("Solution"),
			"fieldtype": "Link",
			"options": "Solution"
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
