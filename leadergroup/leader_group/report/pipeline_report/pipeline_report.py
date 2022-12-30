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
            fields=['*'],
            order_by="status")
    for opportunity in data:
        opportunity["converted_by"] = frappe.db.get_value('User',opportunity.converted_by, 'full_name')
        next_actions = frappe.db.get_all("Next Action",
            filters={"parent":opportunity.name},
            fields=["action","owner_name","status","action_date","action_type","progress","expected_date","completed_date"],
            order_by="idx")

        next_action = []
        owner_name = []
        action_type = []
        action_date = []
        action = []
        progress = []
        expected_date = []
        completed_date = []
        actions_status = []
    
        for actions in next_actions:
            if actions.action :
                action.append(actions.action)
            if actions.action_type :
                action_type.append(actions.action_type)
            if actions.progress :
                progress.append(str(actions.progress))
            if actions.action_date :
                action_date.append(str(actions.action_date))
            if actions.expected_date :
                expected_date.append(str(actions.expected_date))
            if actions.completed_date :
                completed_date.append(str(actions.completed_date))
            if actions.owner_name :
                owner_name.append(actions.owner_name)
            if actions.status :
                actions_status.append(actions.status)
            if actions.status and actions.action :
                next_action.append(actions.action +"-"+ actions.status)
        
        action = ', '.join(action)
        action_type  = ', '.join(action_type)
        progress = ', '.join(progress)
        action_date = ', '.join(action_date)
        expected_date = ', '.join(expected_date)
        completed_date = ', '.join(completed_date)
        owner_name = ', '.join(owner_name)
        actions_status = ', '.join(actions_status)
        next_action = ', '.join(next_action)
        opportunity["action"] = action
        opportunity["owner_name"] = owner_name
        opportunity["action_type"] = action_type
        opportunity["action_date"] = action_date
        opportunity["next_action"] = next_action
        opportunity["status"] = actions_status
        opportunity["progress"] = progress
        opportunity["expected_date"] = expected_date
        opportunity["completed_date"] = completed_date
    return columns, data

def get_columns():
	columns = [
				{
					"label": _("Name"),
					"fieldname": "name",
					"fieldtype": "Data",
					"width": "180"
				},
				{
					"label": _("Customer"),
					"fieldname": "party_name",
					"fieldtype": "Link",
					"options": "Customer",
					"width": "180"
				},
				{
					"label": _("Opportunity Name"),
					"fieldname": "opportunity_name",
					"fieldtype": "Data",
					"width": "250"
				},
					{
					"label": _("Owner Name"),
					"fieldname": "owner_name",
					"fieldtype": "Data",
					"width": "200"
				},
					{
					"label": _("Action Type"),
					"fieldname": "action_type",
					"fieldtype": "Data",
					"width": "200"
				},
					{
					"label": _("Action Date"),
					"fieldname": "action_date",
					"fieldtype": "Data",
					"width": "150"
				},
					{
					"label": _("Action"),
					"fieldname": "action",
					"fieldtype": "Data",
					"width": "150"
				},
					{
					"label": _("Expected Date"),
					"fieldname": "expected_date",
					"fieldtype": "Data",
					"width": "200"
				},
					{
					"label": _("Completed Date"),
					"fieldname": "completed_date",
					"fieldtype": "Data",
					"width": "150"
				},
					{
					"label": _("Status"),
					"fieldname": "status",
					"fieldtype": "Data",
					"width": "120"
				},
					{
					"label": _("Progress%"),
					"fieldname": "progress",
					"fieldtype": "Data",
					"width": "120"
				},
					{
					"label": _("Next Contact By"),
					"fieldname": "contact_by",
					"fieldtype": "Data",
					"width": "200"
				},
					{
					"label": _("Opportunity From"),
					"fieldname": "opportunity_from",
					"fieldtype": "Data",
					"width": "180"
				},
     
				{
					"label": _("Ownership"),
					"fieldname": "converted_by",
					"fieldtype": "Data",
					"width": "180"
				},
				{
					"label": _("Stage"),
					"fieldname": "sales_stage",
					"fieldtype": "Data",
					"width": "120"
				},
					{
					"label": _("Source"),
					"fieldname": "source",
					"fieldtype": "Link",
					"options": "Lead Source",
					"width": "120"
				},
				   {
					"label": _("Next Action"),
					"fieldname": "next_action",
					"fieldtype": "Data",
					"width": "250"
				},
					{
					"label": _("Lost Reason"),
					"fieldname": "order_lost_reason",
					"fieldtype": "Small Text",
					"width": "200"
				},
					{
					"label": _("Next Contact Date"),
					"fieldname": "contact_date",
					"fieldtype": "Date",
					"width": "150"
				},
					{
					"label": _("Opportunity Date"),
					"fieldname": "transaction_date",
					"fieldtype": "Date",
					"width": "200"
				},
					{
					"label": _("To Discuss"),
					"fieldname": "to_discuss",
					"fieldtype": "Small Text",
					"width": "250"
				},
		 			{
					"label": _("Tender Number"),
					"fieldname": "tender_number",
					"fieldtype": "Data",
					"width": "180"
				},
					{
					"label": _("Tender Price"),
					"fieldname": "tender_price",
					"fieldtype": "Currency",
					"width": "120"
				},
					{
					"label": _("Tender Issue Date"),
					"fieldname": "tender_issue_date",
					"fieldtype": "Date",
					"width": "180"
				},
					{
					"label": _("Tender Link"),
					"fieldname": "tender_link",
					"fieldtype": "Data",
					"width": "200"
				},
					{
					"label": _("Tender Submission Date"),
					"fieldname": "tender_submission_date",
					"fieldtype": "Date",
					"width": "180"
				},
					{
					"label": _("Solution"),
					"fieldname": "solution",
					"fieldtype": "Link",
					"options": "Solution",
					"width": "200"
				},
					{
					"label": _("Description"),
					"fieldname": "description",
					"fieldtype": "Long Text",
					"width": "250"
				},
					{
					"label": _("Expected Closing Date"),
					"fieldname": "expected_closing",
					"fieldtype": "Date",
					"width": "180"
				},
					{
					"label": _("Proposal Deadline"),
					"fieldname": "proposal_deadline",
					"fieldtype": "Date",
					"width": "180"
				},
					{
					"label": _("First Response Time"),
					"fieldname": "first_response_time",
					"fieldtype": "Duration",
					"width": "150"
				},
					{
					"label": _("Probability (%)"),
					"fieldname": "probability",
					"fieldtype": "Percent",
					"width": "120"
				},
					{
					"label": _("Case Design"),
					"field_type": "Data",
					"fieldname": "case_design",
					"width": "180"
				},
					{
					"label": _("SDM"),
					"fieldname": "sdm",
					"fieldtype": "Link",
					"options": "User",
					"width": "180"
				},
					{
					"label": _("Sales Representative"),
					"fieldname": "sales_rep",
					"fieldtype": "Link",
     				"options": "User",
					"width": "180"
				}			
			]
	return columns