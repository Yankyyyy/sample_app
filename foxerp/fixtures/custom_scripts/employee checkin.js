// Copyright (c) 2018, Frappe Technologies Pvt. Ltd. and contributors
// For license information, please see license.txt

frappe.ui.form.on('Employee Checkin', {
	setup: function() {
		document.getElementsByClassName("leaflet-draw leaflet-control")[0].remove("leaflet-draw leaflet-control"); 
	},
    before_save: function(frm) {
	    frm.doc.latitude = frm.fields_dict.location.map.getCenter()['lat'];
		frm.doc.longitude = frm.fields_dict.location.map.getCenter()['lng'];
    }
});