// Copyright (c) 2022, Leader Group and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Opportunity Completion Percentage"] = {
	"filters": [
		{
			"fieldname":"status",
			"label": __("Status"),
			"fieldtype": "Select",
			"options": "Open\nIn Progress\nClosed",
			"default": "Open",
			"reqd":1
		}
	]
};
