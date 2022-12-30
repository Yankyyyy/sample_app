frappe.ui.form.on('Purchase Receipt', {
    onload: function(frm) {
	    frm.add_custom_button(__('Workflow Status'), function() {
		    frappe.set_route("query-report", 'Workflow Status Report', {'reference_doctype': 'Purchase Receipt', 'reference_name': frm.doc.name});
	    }, __("View"));
    }
})