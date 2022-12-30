// Copyright (c) 2022, Leader Group and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.provide("leadergroup.cost_center_summary_report");

leadergroup.cost_center_summary_report = {
    "open_general_ledger": function(data) {
        if (!data.name) return;
        frappe.route_options = {
            "company": frappe.query_report.get_filter_value('company'),
            "from_date": frappe.query_report.get_filter_value('from_date'),
            "to_date": frappe.query_report.get_filter_value('to_date'),
            "cost_center": frappe.query_report.get_filter_value('cost_center')
        };
        account = data.name;
        frappe.route_options["account"] = account;
        frappe.set_route("query-report", "General Ledger");
    }
};

frappe.query_reports["Cost Center Summary Report"] = {
	"filters": [
        {
            "fieldname": "company",
            "label": __("Company"),
            "fieldtype": "Link",
            "options": "Company",
            "default": frappe.defaults.get_user_default("Company") || frappe.defaults.get_global_default("Company"),
            "reqd": 1,
            "hidden": 1
        },
		{
			"fieldname":"cost_center",
			"label": __("Cost Center"),
			"fieldtype": "MultiSelectList",
			get_data: function(txt) {
				return frappe.db.get_link_options('Cost Center', txt, {
					company: frappe.query_report.get_filter_value("company")
				});
			}
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
        }
	],
    "formatter": function(value, row, column, data, default_formatter) {
        if (data && column.fieldname=="account_name") {
            value = data.account_name || value;

            column.link_onclick = "leadergroup.cost_center_summary_report.open_general_ledger(" + JSON.stringify(data) + ")";
        }
        value = default_formatter(value, row, column, data);
        return value;
    },
    
    onload: function(report) {
        const views_menu = report.page.add_custom_button_group(__('General Ledger Report'));

        report.page.add_custom_menu_item(views_menu, __("General Ledger"), function() {
            var filters = report.get_values();
            frappe.set_route('query-report', 'General Ledger', filters);
        });
    }
};