// Copyright (c) 2022, Leader Group and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Opportunity Open Task"] = {
	"filters": [
		{
			"fieldname": "converted_by",
			"label": __("Owner"),
			"fieldtype": "Link",
			"options": "User"
		},
		{
			"fieldname": "status",
			"label": __("Status"),
			"fieldtype": "Select",
			"options": "\nOpen\nQuotation\nConverted\nLost\nReplied\nClosed"
		}	
	]
};
