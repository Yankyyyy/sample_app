// Copyright (c) 2018, Frappe Technologies Pvt. Ltd. and Contributors
// License: GNU General Public License v3. See license.txt

frappe.query_reports["Statement Of Employee"] = {
	"filters": [
		{
			"fieldname":"company",
			"label": __("Company"),
			"fieldtype": "Link",
			"options": "Company",
			"default": frappe.defaults.get_user_default("Company"),
			"reqd": 1
		},
		{
            "fieldname": "employee",
            "label": __("Employee"),
            "fieldtype": "Link",
            "options": "Employee",
            "reqd": 1,
			"on_change":function(query_report){

				frappe.query_report.set_filter_value(
					"period" ,"Period : "+ 
					frappe.query_report.get_filter_value('from_date')
					 + "-" + 
					 frappe.query_report.get_filter_value('to_date')
					 )
			}
        },
		{
			"fieldname":"from_date",
			"label": __("From Date"),
			"fieldtype": "Date",
			"default": frappe.datetime.add_months(frappe.datetime.get_today(), -1),
			"reqd": 1,
			"width": "60px"
		},
		{
			"fieldname":"to_date",
			"label": __("To Date"),
			"fieldtype": "Date",
			"default": frappe.datetime.get_today(),
			"reqd": 1,
			"width": "60px"
		},
		{
            "fieldname": "period",
            "label": __("Period"),
            "fieldtype": "Data",	
            "read_only": 1,
			"width": "120px"
        }
	]
}

erpnext.utils.add_dimensions('General Ledger', 15)