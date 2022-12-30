// Copyright (c) 2022, Leader Group and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Opportunity Task Tracker CEO"] = {
	"filters": [
		{
			"fieldname":"party_name",
			"label": __("Customer"),
			"fieldtype": "Link",
			"options": "Customer",
		},
		{
			"fieldname":"converted_by",
			"label": __("Ownership"),
			"fieldtype": "Link",
			"options": "User",
		},
		{
			"fieldname":"status",
			"label": __("Status"),
			"fieldtype": "Select",
			"options": ["Open","Quotation","Converted","Lost","Replied","Closed"],
		},
	]
};
