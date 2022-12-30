from . import __version__ as app_version

app_name = "leadergroup"
app_title = "Leader Group"
app_publisher = "Leader Group"
app_description = "Leader Group ERP"
app_icon = "octicon octicon-file-directory"
app_color = "grey"
app_email = "k.chauhan@leadergroup.com"
app_license = "Proprietary Software of Leader Group"
app_logo_url = "/assets/leadergroup/images/FoxERP_logo@4x1.jpg"

# Includes in <head>
# ------------------

# include js, css files in header of desk.html
app_include_css = "/assets/css/leadergroup.css"
app_include_js = "/assets/leadergroup/js/comment.js"

# include js, css files in header of web template
web_include_css = "/assets/css/leadergroup-web.css"
# web_include_js = "/assets/leadergroup/js/leadergroup.js"

# include custom scss in every website theme (without file extension ".scss")
# website_theme_scss = "leadergroup/public/scss/website"

# include js, css files in header of web form
# webform_include_js = {"doctype": "public/js/doctype.js"}
# webform_include_css = {"doctype": "public/css/doctype.css"}

# include js in page
# page_js = {"page" : "public/js/file.js"}

# include js in doctype views
# doctype_js = {"doctype" : "public/js/doctype.js"}
# doctype_list_js = {"doctype" : "public/js/doctype_list.js"}
# doctype_tree_js = {"doctype" : "public/js/doctype_tree.js"}
# doctype_calendar_js = {"doctype" : "public/js/doctype_calendar.js"}

# Home Pages
# ----------

# application home page (will override Website Settings)
# home_page = "login"

# website user home page (by Role)
# role_home_page = {
#	"Role": "home_page"
# }

accounting_dimension_doctypes = ["Purchase Order"]

# Generators
# ----------

# automatically create page for each record of this doctype
# website_generators = ["Web Page"]

# Installation
# ------------

# before_install = "leadergroup.install.before_install"
# after_install = "leadergroup.install.after_install"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "leadergroup.notifications.get_notification_config"

# Permissions
# -----------
# Permissions evaluated in scripted ways

# permission_query_conditions = {
# 	"Event": "frappe.desk.doctype.event.event.get_permission_query_conditions",
# }
#
# has_permission = {
# 	"Event": "frappe.desk.doctype.event.event.has_permission",
# }

# DocType Class
# ---------------
# Override standard doctype classes

override_doctype_class = {
	"Delivery Note": "leadergroup.api.delivery_note.LeadergroupDeliveryNote"
}

# Document Events
# ---------------
# Hook on document methods and events

doc_events = {
    "Issue": {
        "validate": "leadergroup.api.issue.validate"
    },
	"Material Request": {
		"before_save": "leadergroup.api.accounting_dimensions.after_save"
	},
	"Purchase Order": {
		"before_save": "leadergroup.api.accounting_dimensions.after_save"
	},
	"Employee":{
		"autoname": "leadergroup.api.employee.set_employee_autoname"
	},
	"Sales Invoice":{
		"before_save": "leadergroup.api.sales_invoice.set_in_words_arabic",
		"before_insert": "leadergroup.api.sales_invoice.sales_invoice_uuid",
		"before_submit": "leadergroup.api.sales_invoice.set_delivery_note_ref",
		"on_cancel": "leadergroup.api.sales_invoice.unlink_delivery_note"
	},
	"Journal Entry":{
		"on_submit": "leadergroup.api.journal_entry.update_return_status_in_je",
		"on_cancel": "leadergroup.api.journal_entry.update_return_status_in_je"
	},
	"Account": {
		"autoname": "leadergroup.api.account.autoname"
	},
	"Delivery Note": {
		"on_cancel": "leadergroup.api.delivery_note.unlink_sales_invoice"
	}
}



# Scheduled Tasks
# ---------------

scheduler_events = {
 	"daily": [
 		"leadergroup.api.opportunity.send_email_for_next_action"
 	]
 }

# Testing
# -------

# before_tests = "leadergroup.install.before_tests"

# Overriding Methods
# ------------------------------
#
# override_whitelisted_methods = {
# 	"frappe.desk.doctype.event.event.get_events": "leadergroup.event.get_events"
# }
#
# each overriding function accepts a `data` argument;
# generated from the base implementation of the doctype dashboard,
# along with any modifications made in other Frappe apps
# override_doctype_dashboards = {
# 	"Task": "leadergroup.task.get_dashboard_data"
# }

# exempt linked doctypes from being automatically cancelled
#
# auto_cancel_exempted_doctypes = ["Auto Repeat"]


# User Data Protection
# --------------------

user_data_fields = [
	{
		"doctype": "{doctype_1}",
		"filter_by": "{filter_by}",
		"redact_fields": ["{field_1}", "{field_2}"],
		"partial": 1,
	},
	{
		"doctype": "{doctype_2}",
		"filter_by": "{filter_by}",
		"partial": 1,
	},
	{
		"doctype": "{doctype_3}",
		"strict": False,
	},
	{
		"doctype": "{doctype_4}"
	}
]

# Authentication and authorization
# --------------------------------

# auth_hooks = [
# 	"leadergroup.auth.validate"
# ]

