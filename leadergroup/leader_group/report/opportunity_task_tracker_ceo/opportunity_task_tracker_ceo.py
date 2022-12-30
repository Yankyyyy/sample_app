# Copyright (c) 2022, Leader Group and contributors
# For license information, please see license.txt

import frappe
from frappe import _

def execute(filters=None):
	columns, data = [], []
	columns = get_columns() 	
	opportunity = frappe.get_list('Opportunity',fields=["*"], filters=filters)
	for opt in opportunity:
		next_action = frappe.get_list('Next Action',fields={'*'}, filters={"parent":opt["name"]})	
		if(next_action):
			for ch in next_action:  
				report_data = {		
							'customer_name' : opt["party_name"],
							'opportunity_name' : opt["opportunity_name"],
							"opportunity_desc" :  opt["description"],
							"type" : opt["sales_stage"],
							"project_value" : opt["opportunity_amount"],
							"case_design" : opt["case_design"],
							"weight" : ch["progress"],
							"receiving_date" : ch["action_date"],
							"closing_date" : ch["completed_date"]      							
						}
				
				data.append(report_data)
		else:
			report_data = {
					'customer_name' : opt["party_name"],
					'opportunity_name' : opt["opportunity_name"],
					"opportunity_desc" :  opt["description"],
					"type" : opt["sales_stage"],					
					"project_value" : opt["opportunity_amount"],
					"case_design" : opt["case_design"],
					"weight" : "",
					"receiving_date" : "",
					"closing_date" : ""
     			}
			data.append(report_data)
	return columns, data

def get_columns():
	"""return columns"""
	columns = [    	
		{"label": _("Customer Name"),"fieldname": "customer_name","width": 180},
		{"label": _("Opportunity Name"),"fieldname": "opportunity_name","width": 180},
		{"label": _("Opportunity Description"),"fieldname": "opportunity_desc","width": 200},
		{"label": _("Type"),"fieldname": "type","width": 120},
		{"label": _("Project Value"),"fieldname": "project_value","width": 100},
		{"label": _("Case Design"),"fieldname": "case_design","width": 100},
		{"label": _("Weight"),"fieldname": "weight","fieldtype": "Percent","width": 100},
		{"label": _("Receiving/Start Date"),"fieldname": "receiving_date","width": 120},
		{"label": _("Closing Date"),"fieldname": "closing_date","width": 120},
	]
	return columns