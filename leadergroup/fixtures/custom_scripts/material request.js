frappe.ui.form.on('Material Request', {
    onload: function(frm) {
	    frm.add_custom_button(__('Workflow Status'), function() {
		    frappe.set_route("query-report", 'Workflow Status Report', {'reference_doctype': 'Material Request', 'reference_name': frm.doc.name});
	    }, __("View"));
		$.each(frm.doc.items, function(i,d){
			d.employee = undefined
		})
    }
});

frappe.ui.form.on('Material Request Item', {
	employee: function(frm,cdt,cdn) {
	    let child = locals[cdt][cdn]
	    if (child.employee){
	    frappe.model.set_value(cdt,cdn,'update_flag',1)
	}
	}
});