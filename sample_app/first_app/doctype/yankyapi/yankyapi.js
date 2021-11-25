// Copyright (c) 2021, Yanky and contributors
// For license information, please see license.txt



// frappe.ui.form.on('YankyAPI', {
// 	refresh: function(frm) {
// 		let doc = this.frm.doc;
// 		erpnext.toggle_naming_series();
// 		frappe.dynamic_link = { doc: doc, fieldname: 'address_line1', doctype: 'YankyAPI' }
// 		if (!this.frm.is_new()) {
// 			frappe.contacts.render_address_and_contact(this.frm);
// 		} else {
// 			frappe.contacts.clear_address_and_contact(this.frm);
// 		}
// 	}
// });

// frappe.provide("erpnext.utils");

// frappe.ui.form.on('YankyAPI', {
// 	refresh: function(frm) {
// 		if (!cur_frm.doc.__islocal) {
// 			$(frm.fields_dict['address_html'].wrapper)
// 				.html(frappe.render_template("address_list", cur_frm.doc.__onload));
// 		}
// 	}
// });

// cur_frm.add_fetch("address_line1", "address_type", "address_type");
// cur_frm.add_fetch("address_line1", "address_line1", "address_line1");
// cur_frm.add_fetch("address_line1", "city", "city");
// cur_frm.add_fetch("address_line1", "state", "state");
// cur_frm.add_fetch("address_line1", "country", "country");
// cur_frm.add_fetch("address_line1", "pincode", "pincode");

// frappe.ui.form.on("YankyAPI", "address_list", function(frm, cdt, cdn){
//     var d = locals[cdt][cdn],
//     wrapper = frm.fields_dict[d.address_list1].grid.grid_rows_by_docname[cdn].fields_dict["address_list1"].wrapper;
//     $("<div>Loading...</div>").appendTo(wrapper);
// }


// Copyright (c) 2019, Frappe Technologies Pvt. Ltd. and Contributors
// License: GNU General Public License v3. See license.txt

// frappe.provide("erpnext");
// cur_frm.email_field = "email_id";

// erpnext.LeadController = frappe.ui.form.Controller.extend({
// 	setup: function () {
// 		this.frm.make_methods = {
// 			'Customer': this.make_customer,
// 			'Quotation': this.make_quotation,
// 			'Opportunity': this.make_opportunity
// 		};

// 		this.frm.toggle_reqd("lead_name", !this.frm.doc.organization_lead);
// 	},

// 	onload: function () {
// 		this.frm.set_query("customer", function (doc, cdt, cdn) {
// 			return { query: "erpnext.controllers.queries.customer_query" }
// 		});

// 		this.frm.set_query("lead_owner", function (doc, cdt, cdn) {
// 			return { query: "frappe.core.doctype.user.user.user_query" }
// 		});

// 		this.frm.set_query("contact_by", function (doc, cdt, cdn) {
// 			return { query: "frappe.core.doctype.user.user.user_query" }
// 		});
// 	},

// 	refresh: function () {
// 		let doc = this.frm.doc;
// 		erpnext.toggle_naming_series();
// 		frappe.dynamic_link = { doc: doc, fieldname: 'name', doctype: 'Lead' }

// 		if (!this.frm.is_new() && doc.__onload && !doc.__onload.is_customer) {
// 			this.frm.add_custom_button(__("Customer"), this.make_customer, __("Create"));
// 			this.frm.add_custom_button(__("Opportunity"), this.make_opportunity, __("Create"));
// 			this.frm.add_custom_button(__("Quotation"), this.make_quotation, __("Create"));
// 		}

// 		if (!this.frm.is_new()) {
// 			frappe.contacts.render_address_and_contact(this.frm);
// 		} else {
// 			frappe.contacts.clear_address_and_contact(this.frm);
// 		}
// 	},

// 	make_customer: function () {
// 		frappe.model.open_mapped_doc({
// 			method: "erpnext.crm.doctype.lead.lead.make_customer",
// 			frm: cur_frm
// 		})
// 	},

// 	make_opportunity: function () {
// 		frappe.model.open_mapped_doc({
// 			method: "erpnext.crm.doctype.lead.lead.make_opportunity",
// 			frm: cur_frm
// 		})
// 	},

// 	make_quotation: function () {
// 		frappe.model.open_mapped_doc({
// 			method: "erpnext.crm.doctype.lead.lead.make_quotation",
// 			frm: cur_frm
// 		})
// 	},

// 	organization_lead: function () {
// 		this.frm.toggle_reqd("lead_name", !this.frm.doc.organization_lead);
// 		this.frm.toggle_reqd("company_name", this.frm.doc.organization_lead);
// 	},

// 	company_name: function () {
// 		if (this.frm.doc.organization_lead && !this.frm.doc.lead_name) {
// 			this.frm.set_value("lead_name", this.frm.doc.company_name);
// 		}
// 	},

// 	contact_date: function () {
// 		if (this.frm.doc.contact_date) {
// 			let d = moment(this.frm.doc.contact_date);
// 			d.add(1, "day");
// 			this.frm.set_value("ends_on", d.format(frappe.defaultDatetimeFormat));
// 		}
// 	}
// });

// $.extend(cur_frm.cscript, new erpnext.LeadController({ frm: cur_frm }));


// frappe.ui.form.on('Sales Invoice', {
//   setup: function(frm){
//     refresh: function(frm) {

//       $(frm.fields_dict['my_html_field'].wrapper)
//         .html(`<div>${frm.fields_dict.my_source_field.value}</div>`);

//       console.log(`### ${frm.fields_dict.my_source_field.value} ###`);