frappe.ui.form.on("Journal Entry", {
    refresh: function(frm) {
        setTimeout(() => {
            if(frm.doc.docstatus == 1 && frm.doc.workflow_state=="Return Issued" ) {
				frm.remove_custom_button('Reverse Journal Entry',"Actions")
            }
        }, 10);
    }
});