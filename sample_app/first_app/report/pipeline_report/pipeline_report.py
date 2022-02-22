# Copyright (c) 2013, Leader Group and contributors
# For license information, please see license.txt

import frappe
from frappe import _

def execute(filters=None):
    filters.pop('date', None)
    columns = get_columns()
    data = []
    data = frappe.db.get_all("Opportunity",
            filters=filters,
            fields=["name",
                    "party_name",
                    'opportunity_name',
                    "converted_by",
                    "sales_stage",
                    "status"
                ],
            order_by="status")
    for opportunity in data:
        opportunity["converted_by"] = frappe.db.get_value('User',opportunity.converted_by, 'full_name')
        next_actions = frappe.db.get_all("Next Action",
            filters={"parent":opportunity.name},
            fields=["action",
                    'owner_name',
                    "status",
                    "action_date"
                ],
            order_by="modified")
        next_action = ''
        owner_name = ''
        for action in next_actions:
            next_action += action.action +"-"+ action.status +" </br>"
            owner_name += action.owner_name +" </br>"
        opportunity["next_action"] = next_action
        opportunity["owner_name"] = owner_name
    return columns, data

def get_columns():
	columns = [
				{
					"label": _("Customer"),
					"fieldname": "party_name",
					"fieldtype": "Link",
					"options": "Customer",
					"width": "150"
				},
				{
					"label": _("Oppurtunity Name"),
					"fieldname": "opportunity_name",
					"fieldtype": "Data",
					"width": "200"
				},
				{
					"label": _("Ownership"),
					"fieldname": "converted_by",
					"fieldtype": "Data",
					"width": "200"
				},
				{
					"label": _("Stage"),
					"fieldname": "sales_stage",
					"fieldtype": "Data",
					"width": "120"
				},
				{
					"label": _("Status"),
					"fieldname": "status",
					"fieldtype": "Data",
					"width": "120"
				},
				{
					"label": _("Next Action"),
					"fieldname": "next_action",
					"fieldtype": "Data",
					"width": "200"
				},
				{
					"label": _("Next Action Owner"),
					"fieldname": "owner_name",
					"fieldtype": "Data",
					"width": "200"
				}
			]
	return columns