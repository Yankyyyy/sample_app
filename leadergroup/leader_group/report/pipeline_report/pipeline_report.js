// Copyright (c) 2016, Leader Group and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Pipeline Report"] = {
	"filters": [
		{
			"fieldname": "customer_name",
			"label": __("Customer"),
			"fieldtype": "Link",
			"options": "Customer"
		},
		{
			"fieldname": "status",
			"label": __("Status"),
			"fieldtype": "Select",
			"options": "\nOpen\nQuotation\nConverted\nLost\nReplied\nClosed"
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
