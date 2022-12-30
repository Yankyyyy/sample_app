// Copyright (c) 2022, FoxERP and contributors
// For license information, please see license.txt

frappe.ui.form.on('Recruitment Request', {
	refresh: function(frm){
		frm.trigger('toggle_fields')
		if (frm.doc.__islocal){
			frappe.db.exists('User', 'ceo@leadergroup.com').then(exists => {
				if (exists) {
					frm.set_value('ceo','ceo@leadergroup.com')
				}
			});
		}
	},
	currency: function(frm) {
		frappe.db.get_value("Company", frm.doc.company, "default_currency", function(value){
			if (frm.doc.currency != value['default_currency']){
				frappe.call({
					method: "erpnext.setup.utils.get_exchange_rate",
					args: {
						from_currency: frm.doc.currency,
						to_currency: frm.doc.currency
					},
					callback: function(r) {
						if (r.message) {
							frm.set_value('conversion_rate', r.message)
						}
					}
				});
			}
			else{
				frm.set_value('conversion_rate', 1)
			}
		});
		frm.trigger('calc_amount')
		frm.trigger('toggle_fields')
	},
	conversion_rate: function(frm){
		frm.trigger('calc_salary')
		frm.trigger('calc_amount')
	},
	yearly_salary: function(frm){
		frm.set_value('monthly_salary', frm.doc.yearly_salary/12)
		frm.trigger('calc_amount')
	},
	monthly_salary: function(frm){
		frm.set_value('yearly_salary', frm.doc.monthly_salary*12)
		frm.trigger('calc_amount')
	},
	base_yearly_salary: function(frm){
		frm.set_value('base_monthly_salary', frm.doc.base_yearly_salary/12)
		frm.trigger('calc_salary')
	},
	base_monthly_salary: function(frm){
		frm.set_value('base_yearly_salary', frm.doc.base_monthly_salary*12)
		frm.trigger('calc_salary')
	},
	calc_amount: function(frm){
		frm.doc.base_monthly_salary = frm.doc.monthly_salary * frm.doc.conversion_rate
		frm.doc.base_yearly_salary = frm.doc.yearly_salary * frm.doc.conversion_rate
		frm.refresh_field('base_monthly_salary')
		frm.refresh_field('base_yearly_salary')
	},
	calc_salary: function(frm){
		frm.doc.monthly_salary = frm.doc.base_monthly_salary / frm.doc.conversion_rate
		frm.doc.yearly_salary = frm.doc.base_yearly_salary / frm.doc.conversion_rate
		frm.refresh_field('monthly_salary')
		frm.refresh_field('yearly_salary')
	},
	toggle_fields: function(frm){
		frappe.db.get_value("Company", frm.doc.company, "default_currency", function(value){
			var company_currency = undefined
			if (value){
				company_currency = value['default_currency']
			}
			frappe.get_meta('Recruitment Request').fields.forEach(d => {
				if (d.fieldname=='base_yearly_salary'){
					var base_yearly_salary_label = d.label
					frm.set_df_property("base_yearly_salary","label", base_yearly_salary_label.replace('Company Currency', company_currency))
				}

				if (d.fieldname=='base_monthly_salary'){
					var base_monthly_salary_label = d.label
					frm.set_df_property("base_monthly_salary","label", base_monthly_salary_label.replace('Company Currency', company_currency))
				}

				if (d.fieldname=='yearly_salary'){
					var yearly_salary_label = d.label
					frm.set_df_property("yearly_salary","label", yearly_salary_label + ' (' + frm.doc.currency + ')')
				}

				if (d.fieldname=='monthly_salary'){
					var monthly_salary_label = d.label
					frm.set_df_property("monthly_salary","label", monthly_salary_label + ' (' + frm.doc.currency + ')')
				}
			});
			// if (frm.doc.currency != company_currency){
			// 	frm.set_df_property("conversion_rate","hidden",0)

			// 	frm.set_df_property("base_yearly_salary","hidden",0)
			// 	frm.set_df_property("base_monthly_salary","hidden",0)
			// }
			// else{
			// 	frm.set_df_property("conversion_rate","hidden",1)

			// 	frm.set_df_property("base_yearly_salary","hidden",1)
			// 	frm.set_df_property("base_monthly_salary","hidden",1)
			// }
		});
	}
});