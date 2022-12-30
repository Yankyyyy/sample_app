// Copyright (c) 2021, Leader Group and contributors
// For license information, please see license.txt

frappe.ui.form.on('Solution', {
	// refresh: function(frm) {

	// }
});

//on selection of code maturity level field will be auto populated according to the code choosed
frappe.ui.form.on("Solution Offerings", {
	code: function (frm, cdt, cdn) {
			var code_maturity_level_map = {
				"0":"Not Ready",
				"1":"To be updated",
				"2":"In Progress",
				"3":"Ready"
				}
			var row = locals[cdt][cdn];
			row.maturity_level = code_maturity_level_map[row.code]
			refresh_field(frm.doc.solution_offerings);
		}			
});