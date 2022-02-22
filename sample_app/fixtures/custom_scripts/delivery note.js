frappe.ui.form.on('Delivery Note', {
    onload: function(frm) {
	    frm.add_custom_button(__('Workflow Status'), function() {
		    frappe.set_route("query-report", 'Workflow Status Report', {'reference_doctype': 'Delivery Note', 'reference_name': frm.doc.name});
	    }, __("View"));
    }
})