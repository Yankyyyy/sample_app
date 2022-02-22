frappe.ui.form.on('Task', {
	onload: function(frm) {
		frm.set_query("technical_manager", function(frm) {
			return {
				query:"leadergroup.api.project.get_managers",
				filters:{
					role: "Projects Manager"
				}
			}
		});
	}
})