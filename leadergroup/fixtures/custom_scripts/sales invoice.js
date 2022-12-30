frappe.ui.form.on('Sales Invoice', {
    onload: function(frm) {
       if (cur_frm.doc.is_return == 1) {
        set_return_naming_series()
       }
    },
    is_return:function(frm) {
        if(cur_frm.doc.is_return == 1 ){
            set_return_naming_series()
        }else{
            cur_frm.set_value("naming_series", "ACC-SINV-.YYYY.-");
        }
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

function set_return_naming_series() {
    cur_frm.set_value("naming_series", "ACC-SINV-RET-.YYYY.-");
}