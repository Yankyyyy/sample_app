// Copyright (c) 2022, Leader Group and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Detailed VAT Input Purchases"] = {
    "filters": [
        {
            "fieldname": "company",
            "label": "Company",
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
            "fieldname":"invoice_type",
            "label": __("Invoice Type"),
            "fieldtype": "Select",
            "options": "Purchase\nPurchase Adjustment",
            "default": "Purchase",
            "reqd": 1
        },
        {
            "fieldname":"invoice",
            "label": __("Invoice"),
            "fieldtype": "Select",
            "options": "\nLocal Purchase\nFinancial Charges\nBusiness Expenses",
        },
        {
            "fieldname":"account_list",
            "label": __("VAT Type"),
            "fieldtype": "MultiSelectList",
            get_data: function(txt) {
                return frappe.db.get_link_options('Account', txt, {
                    company: frappe.query_report.get_filter_value("company"),
                    account_type: "Tax",
                    account_name: ['like', '%VAT%']
                });
            }
        },
        {
            "fieldname": "date",
            "label": __("Printed On"),
            "fieldtype": "Data",
            "default": moment(frappe.datetime.now_datetime()).format("MM-DD-YYYY HH:mm:ss"),
            "read_only": 1
        }
    ],
    onload: function(report) {
        report.page.add_inner_button(__("GAZT Return"), function() {
            var filters = report.get_values();
            frappe.set_route('query-report', 'GAZT Return', filters);
        });
    }
};
