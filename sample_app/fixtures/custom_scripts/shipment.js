frappe.ui.form.on('Shipment', {
	refresh: function(frm) {
		if (frm.doc.docstatus === 1 && !frm.doc.shipment_id) {
			frm.add_custom_button(__('Create Shipment'), function() {
				return frm.events.create_shipment(frm);
			});
		}
		if (frm.doc.shipment_id) {
			frm.add_custom_button(__('Print Shipping Label'), function() {
				return frm.events.print_shipping_label(frm);
			});
            // if (frm.doc.tracking_status != 'Delivered') {
            //     frm.add_custom_button(__('Update Tracking'), function() {
            //         return frm.events.update_tracking(frm, frm.doc.service_provider, frm.doc.shipment_id);
            //     });
            // }
		}
	},

	create_shipment: function(frm) {
		if (!frm.doc.shipment_id) {
    		let delivery_notes = [];
    		(frm.doc.shipment_delivery_note || []).forEach((d) => {
    			delivery_notes.push(d.delivery_note);
    		});
    		frappe.call({
    			method: "leadergroup.api.aramex.shipment.create_shipment",
    			freeze: true,
    			freeze_message: __("Creating Shipment"),
    			args: {
    				doc: frm.doc
    			},
    			callback: function(r) {
    				if (!r.exc) {
    					frm.reload_doc();
    					frappe.msgprint({
    							message: __("Shipment {0} has been created.", [r.message.shipment_id.bold()]),
    							title: __("Shipment Created"),
    							indicator: "green"
    						});
                        // frm.events.update_tracking(frm, r.message.shipment_id);
    				}
    			}
    		});
		}
		else {
			frappe.throw(__("Shipment already created"));
		}
	},

	print_shipping_label: function(frm) {
		frappe.call({
			method: "leadergroup.api.aramex.shipment.print_shipping_label",
			freeze: true,
			freeze_message: __("Printing Shipping Label"),
			args: {
				shipment_id: frm.doc.shipment_id
			},
			callback: function(r) {
				if (r.message) {
					window.open(r.message);
				}
			}
		});
	},

	update_tracking: function(frm, shipment_id) {
		let delivery_notes = [];
		(frm.doc.shipment_delivery_note || []).forEach((d) => {
			delivery_notes.push(d.delivery_note);
		});
		frappe.call({
			method: "leadergroup.api.aramex.shipment.track_shipments",
			freeze: true,
			freeze_message: __("Updating Tracking"),
			args: {
				shipment: frm.doc.name,
				shipment_id: shipment_id
			},
			callback: function(r) {
				if (!r.exc) {
					frm.reload_doc();
				}
			}
		});
	}
});