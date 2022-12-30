frappe.ui.form.on('Project', {
	onload: function(frm) {
		frm.set_query("project_manager", function(frm) {
			return {
				query:"leadergroup.api.project.get_managers",
				filters:{
					role: "Projects Manager"
				}
			}
		});
	}
})