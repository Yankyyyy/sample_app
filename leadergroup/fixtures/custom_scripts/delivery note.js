frappe.ui.form.on('Delivery Note', {
    onload: function(frm) {
	    frm.add_custom_button(__('Workflow Status'), function() {
		    frappe.set_route("query-report", 'Workflow Status Report', {'reference_doctype': 'Delivery Note', 'reference_name': frm.doc.name});
	    }, __("View"));
    },
    before_save:function(frm){
        if (cur_frm.doc.is_return === 0) {
            if(cur_frm.doc.discount_amount<0){
                frappe.throw("Discount cannot be negative");
            }
            for(var i in cur_frm.doc.items){
                if(cur_frm.doc.items[i]["discount_amount"]<0){
                    frappe.throw("Item discount cannot be negative");
                }
            }
        }
    }
})