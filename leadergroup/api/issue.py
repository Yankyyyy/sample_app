from __future__ import unicode_literals
import frappe

def validate(doc, method):
    if doc.raised_by:
        project = frappe.db.get_value('user-permission', {'user': doc.raised_by, 'allow': 'Project'}, 'for_value')
        if project:
            doc.project = project
            doc.project_manager = frappe.db.get_value('Project', project, 'project_manager_name')