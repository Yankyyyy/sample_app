frappe.ui.form.on('Landed Cost Voucher', {
    validate: function(frm) {
        if (frappe.datetime.nowdate() < frm.doc.posting_date){
            frm.set_value("posting_date", undefined);
            frappe.throw('Posting Date should be Less than or Equal to Today Date');
        }
    }
})