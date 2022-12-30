# Copyright (c) 2022, Leader Group and contributors
# For license information, please see license.txt

import frappe
from frappe import _

def execute(filters=None):
	columns, data = [], []
	columns = get_columns() 	
	opportunity = frappe.get_list('Opportunity',fields=["*"], filters=filters)
	for opt in opportunity:
		cust_county = frappe.get_value("Address",opt["customer_address"],"county")
		if(opt["opportunity_from"] == "Customer"):
			industry = frappe.get_value("Customer",opt["party_name"],"industry")
			cust_type = frappe.get_value("Customer",opt["party_name"],"customer_type")			
		else:
			industry = frappe.get_value("Lead",opt["party_name"],"industry")
			cust_type = ""
		next_action = frappe.get_list('Next Action',fields={'*'}, filters={"parent":opt["name"]})	
		if(next_action):
			for ch in next_action:  
				report_data = {		
							'sales_office': opt['territory'],
							'cust_county': cust_county,
							'industry' : industry,
							'cust_type' : cust_type,
							'customer_name' : opt["party_name"],
							'opportunity_name' : opt["opportunity_name"],
							"opportunity_desc" :  opt["description"],
							"type" : opt["sales_stage"],
							"project_value" : opt["opportunity_amount"],
							"case_design" : opt["case_design"],
							"sales_rep" : opt["sales_rep"],
							"sdm" : opt["sdm"],
							"case_tender_task" : ch["action"],
							"weight" : ch["progress"],
							"presales_order" : ch["owner_name"],
							"next_action" : ch["action_type"],
							"receiving_date" : ch["action_date"],
							"closing_date" : ch["completed_date"]
						}
				data.append(report_data)
		else:
			report_data = {'sales_office': opt['territory'],
					'cust_county': cust_county,
					'industry' : industry,
					'cust_type' : cust_type,
					'customer_name' : opt["party_name"],
					'opportunity_name' : opt["opportunity_name"],
					"opportunity_desc" :  opt["description"],
					"type" : opt["sales_stage"],
					"project_value" : opt["opportunity_amount"],
					"case_design" : opt["case_design"],
					"sales_rep" : opt["sales_rep"],
					"sdm" : opt["sdm"],
     				"case_tender_task" : "",
					"weight" : "",
					"presales_order" : "",
					"next_action" : "",
					"receiving_date" : "",
					"closing_date" : ""}
			data.append(report_data)
	return columns, data

def get_columns():
	"""return columns"""
	columns = [    	
		{"label": _("Sales Office"),"fieldname": "sales_office","width": 180},
		{"label": _("Customer County"),"fieldname": "cust_county","width": 180},
		{"label": _("Industry"),"fieldname": "industry","width": 150},
		{"label": _("Customer Type"),"fieldname": "cust_type","width": 150},
		{"label": _("Customer Name"),"fieldname": "customer_name","width": 200},
		{"label": _("Opportunity Name"),"fieldname": "opportunity_name","width": 200},
		{"label": _("Opportunity Desc."),"fieldname": "opportunity_desc","width": 250},
		{"label": _("Type"),"fieldname": "type","width": 100},
		{"label": _("Project Value"),"fieldname": "project_value","width": 100},
		{"label": _("Case Design"),"fieldname": "case_design","width": 100},
		{"label": _("Case Tender Tasks"),"fieldname": "case_tender_task","width": 150},
		{"label": _("Weight"),"fieldname": "weight","fieldtype": "Percent","width": 100},
		{"label": _("Presales Owner"),"fieldname": "presales_order","width": 150},
		{"label": _("Next Action"),"fieldname": "next_action","width": 180 },
		{"label": _("Receiving/Start Date"),"fieldname": "receiving_date","width": 120},
		{"label": _("Closing Date"),"fieldname": "closing_date","width": 120},
		{"label": _("Sales Rep"),"fieldname": "sales_rep","width": 180 },
		{"label": _("SDM"),"fieldname": "sdm","width": 180 },	
	]
	return columns