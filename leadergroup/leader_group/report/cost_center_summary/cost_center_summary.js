// Copyright (c) 2022, Leader Group and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Cost Center Summary"] = {
	"filters": [
		{
            "fieldname": "company",
            "label": __("Company"),
            "fieldtype": "Link",
            "options": "Company",
            "default": frappe.defaults.get_user_default("Company") || frappe.defaults.get_global_default("Company"),
            "reqd": 1
        },
		{
            "fieldname": "from_date",
            "label": __("From Date"),
            "fieldtype": "Date",
            "default": frappe.datetime.add_months(frappe.datetime.get_today(), -1),
            "reqd": 1
        },
        {
            "fieldname": "to_date",
            "label": __("To Date"),
            "fieldtype": "Date",
            "default": frappe.datetime.get_today(),
            "reqd": 1
        },
        {
            "fieldname": "printed_on",
            "label": __("Printed On"),
            "fieldtype": "Data",
            "default": moment(frappe.datetime.now_datetime()).format("MM-DD-YYYY HH:mm:ss"),
            "read_only": 1
        },
		{
			"fieldname": "show_zero_values",
			"label": __("Show zero values"),
			"fieldtype": "Check"
		}
	]
};
