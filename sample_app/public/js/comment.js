$(document).on('app_ready', function() {
	$.each(["Lead", "Shipment", "Opportunity", "Quotation", "Supplier Quotation", "Sales Invoice", "Delivery Note",  "Sales Order",
	 "Material Request","Purchase Invoice", "Purchase Receipt", "Purchase Order", "Item", "Customer", "Employee", "Loan", "Task",
	  "Project", "Stock Entry", "Issue"], function(i, doctype) {
		frappe.ui.form.on(doctype, "refresh", function(frm) {
            $(".timeline-message-box").children(".justify-between").children(".actions").children(".action-btn").hide()
		});
	});
});