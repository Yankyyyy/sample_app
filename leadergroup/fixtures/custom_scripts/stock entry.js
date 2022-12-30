frappe.ui.form.on('Stock Entry', {
    onload: function(frm) {
	    frm.add_custom_button(__('Workflow Status'), function() {
		    frappe.set_route("query-report", 'Workflow Status Report', {'reference_doctype': 'Stock Entry', 'reference_name': frm.doc.name});
	    }, __("View"));
    }
})