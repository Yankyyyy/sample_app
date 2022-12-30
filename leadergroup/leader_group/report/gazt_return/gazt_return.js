// Copyright (c) 2016, Leader Group and contributors
// For license information, please see license.txt
/* eslint-disable */
frappe.provide("leadergroup.gazt_return");

leadergroup.gazt_return = {
    "open_vat_details_report": function(data) {
        if (!data.invoice_name || data.account_list.length == 0) return;
        frappe.route_options = {
            "company": frappe.query_report.get_filter_value('company'),
            "from_date": frappe.query_report.get_filter_value('from_date'),
            "to_date": frappe.query_report.get_filter_value('to_date')
        };
        const account_list = []
        for (let i = 0; i < data.account_list.length; i++) {
            account_list[i] = data.account_list[i].name;
        }
        frappe.route_options["account_list"] = account_list;

        if (data.invoice_name == "sales"){
            frappe.set_route("query-report", "Detailed VAT Output Sales");
        }

        if (data.invoice_name == "purchase"){
            frappe.route_options["invoice"] = "Local Purchase";
            frappe.set_route("query-report", "Detailed VAT Input Purchases");
        }

        if (data.invoice_name == "financial"){
            frappe.route_options["invoice"] = "Financial Charges";
            frappe.set_route("query-report", "Detailed VAT Input Purchases");
        }

        if (data.invoice_name == "business"){
            frappe.route_options["invoice"] = "Business Expenses";
            frappe.set_route("query-report", "Detailed VAT Input Purchases");
        }

        if (data.invoice_name == "input rcm"){
            frappe.set_route("query-report", "Detailed RCM Purchases");
        }
    }
};

frappe.query_reports["GAZT Return"] = {
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
            "fieldname":"from_date",
            "label": __("From Date"),
            "fieldtype": "Date",
            "default": frappe.datetime.add_months(frappe.datetime.get_today(), -1),
            "reqd": 1
        },
        {
            "fieldname":"to_date",
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
        if (data && column.fieldname=="particulars") {
            value = data.particulars || value;

            column.link_onclick = "leadergroup.gazt_return.open_vat_details_report(" + JSON.stringify(data) + ")";
        }
        value = default_formatter(value, row, column, data);
        return value;
    },
    
    onload: function(report) {
        const views_menu = report.page.add_custom_button_group(__('VAT Details Reports'));

        report.page.add_custom_menu_item(views_menu, __("Output Sales"), function() {
            var filters = report.get_values();
            filters["invoice_type"] = "Sales";
            frappe.set_route('query-report', 'Detailed VAT Output Sales', filters);
        });

        report.page.add_custom_menu_item(views_menu, __("Output Sales Adjustment"), function() {
            var filters = report.get_values();
            filters["invoice_type"] = "Sales Adjustment";
            frappe.set_route('query-report', 'Detailed VAT Output Sales', filters);
        });

        report.page.add_custom_menu_item(views_menu, __("Input Purchases"), function() {
            var filters = report.get_values();
            filters["invoice_type"] = "Purchase";
            frappe.set_route('query-report', 'Detailed VAT Input Purchases', filters);
        });

        report.page.add_custom_menu_item(views_menu, __("Input Purchases Adjustment"), function() {
            var filters = report.get_values();
            filters["invoice_type"] = "Purchase Adjustment";
            frappe.set_route('query-report', 'Detailed VAT Input Purchases', filters);
        });

        report.page.add_custom_menu_item(views_menu, __("RCM Purchases"), function() {
            var filters = report.get_values();
            filters["invoice_type"] = "RCM";
            frappe.set_route('query-report', 'Detailed RCM Purchases', filters);
        });

        report.page.add_custom_menu_item(views_menu, __("RCM Purchases Adjustment"), function() {
            var filters = report.get_values();
            filters["invoice_type"] = "RCM Adjustment";
            frappe.set_route('query-report', 'Detailed RCM Purchases', filters);
        });
    }
};
