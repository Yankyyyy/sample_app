# Copyright (c) 2013, Leader Group and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.utils import formatdate

def execute(filters=None):
    columns, data = [], []
    columns = get_columns()

    # if not filters.get("reference_name"):
    #     del filters["reference_name"]
    # else:
    #     reference_name = filters.get("reference_name")[0]
    #     filters.reference_name = reference_name

    data = frappe.db.get_all("Comment",
            filters=filters,
            fields=["owner",
                    "reference_name",
                    "creation",
                    'content'
                ],
            order_by="creation")
    for d in data:
        d['creation'] = formatdate(d['creation'])
        d['owner'] =  frappe.get_value('User', d.owner, 'full_name')
        workflow = frappe.get_value('Workflow', {'document_type': filters["reference_doctype"], 'is_active': 1}, 'name')
        transition = frappe.get_value('Workflow Transition', {'parent': workflow, 'next_state': d.content}, ['state', 'action'], as_dict=1)
        if transition:
            d['previous_transition'] = transition.state
            d['action'] = transition.action
    return columns, data

def get_columns():
    return [
        {
            "fieldname": "reference_name",
            "label": _("Reference Name"),
            "fieldtype": "Data",
            "width": 180
        },
        {
            "fieldname": "owner",
            "label": _("Approved By"),
            "fieldtype": "Data",
            "width": 200
        },
        {
            "fieldname": "creation",
            "label": _("Approved On"),
            "fieldtype": "DateTime",
            "width": 180
        },
        {
            "fieldname": "previous_transition",
            "label": _("From State"),
            "fieldtype": "Data",
            "width": 300
        },
        {
            "fieldname": "action",
            "label": _("Action"),
            "fieldtype": "Data",
            "width": 120
        },
        {
            "fieldname": "content",
            "label": _("To State"),
            "fieldtype": "Data",
            "width": 300
        },
    ]