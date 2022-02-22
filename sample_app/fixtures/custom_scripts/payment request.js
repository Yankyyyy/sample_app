frappe.ui.form.on('Payment Request', {
    onload: function(frm) {
	    frm.add_custom_button(__('Workflow Status'), function() {
		    frappe.set_route("query-report", 'Workflow Status Report', {'reference_doctype': 'Payment Request', 'reference_name': frm.doc.name});
	    }, __("View"));
    },    
    refresh: function(frm) {
        if(frm.doc.docstatus == 1) {
    		frm.add_custom_button(__('Create Payment Entry'), function(){
    			frappe.call({
    				method: "erpnext.accounts.doctype.payment_request.payment_request.make_payment_entry",
    				args: {"docname": frm.doc.name},
    				freeze: true,
    				callback: function(r){
    					if(!r.exc) {
    						var doc = frappe.model.sync(r.message);
    						frappe.set_route("Form", r.message.doctype, r.message.name);
                        }
                    }
                });
            }).addClass("btn-primary");
        }
    }
})