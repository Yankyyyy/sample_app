// Copyright (c) 2016, Leader Group and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Workflow Status Report"] = {
	"filters": [
		{
			"fieldname":"comment_type",
			"label": __("Comment Type"),
			"fieldtype": "Data",
            "default": "Workflow",
            "hidden": 1
		}, 
		{
			"fieldname":"reference_doctype",
			"label": __("Reference Type"),
			"fieldtype": "Select",
			"options": [
				"",
				{
					label: __("Sales Order"),
					value: "Sales Order",
				},
				{
					label: __("Purchase Order"),
					value: "Purchase Order",
				},
				{
					label: __("Material Request"),
					value: "Material Request",
				},
				{
					label: __("Payment Request"),
					value: "Payment Request",
				},
				{
					label: __("Delivery Note"),
					value: "Delivery Note",
				},
				{
					label: __("Stock Entry"),
					value: "Stock Entry",
				},
				{
					label: __("Purchase Receipt"),
					value: "Purchase Receipt",
				},
			],
			"reqd": 1,
            "default": "Sales Order",
            // on_change: function() {
            //     frappe.query_report.set_filter_value('reference_name', "");
            //                 frappe.query_report.refresh();
            // },
		},
		{
			"fieldname":"reference_name",
			"label": __("Reference Document"),
            // "fieldtype": "MultiSelectList",
            "fieldtype": "Data",
            "hidden": 1
            // get_data: function(txt) {
            //                 let ref_doc = frappe.query_report.get_filter_value('reference_doctype');
            //     return frappe.db.get_link_options(ref_doc, txt);
            // },
		}  
	]
};
