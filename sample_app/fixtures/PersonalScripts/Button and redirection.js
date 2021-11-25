frappe.ui.form.on('Customer', {
  refresh: function(frm) {
      frm.add_custom_button(__("Create Sales Order"), function(sub){
            frappe.prompt([
    {
        label: 'Item',
        fieldname: 'item_name',
        fieldtype: 'Link',
        options: 'Item',
    },
    {
        label: 'Select Variant',
        fieldname: 'select_variant',
        fieldtype: 'Data',
        options:'Select Variant',
    },
    {
        label: 'Quantity',
        fieldname: 'quantity_no',
        fieldtype: 'Data',
        options: 'Quantity',
    },
    ], (values) => {
        frappe.new_doc("Sales Order", {"customer": frm.doc.name},
            doc => {
            doc.delivery_date = frappe.datetime.get_today();
            let row = frappe.model.add_child(doc, "items");
            row.item_code = values.item_name;
            row.delivery_date =  frappe.datetime.get_today();
            row.qty = values.quantity_no;
        });
       
    });
        });
  },
});

// Email button

frappe.ui.form.on('Shahaazdt', {
    refresh(frm) {
cur_frm.page.add_action_icon(__("fa fa-envelope-o"), function() {
    frappe.msgprint("Custom email or print");
    new frappe.views.CommunicationComposer();
});
    }
});