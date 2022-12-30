# Copyright (c) 2022, Leader Group and contributors
# For license information, please see license.txt

import frappe
from frappe import _

def execute(filters=None):
	columns, data = [], []
	columns= get_columns_data()
	action_data = get_action_data(filters)
	chart = get_action_chart(action_data)
	for action,action_avg in action_data.items():
		row_dict ={
			"action":action,
			"action_avg":str(action_avg) + "%"
		}
		data.append(row_dict)
	return columns, data,None,chart

def get_columns_data():
	columns = []
	columns.extend( 
		[
		{
		"fieldname": "action",
		"label": _("Actions"),
		"fieldtype": "Data",
		"width": 120
		}, 
		{
			"fieldname": "action_avg",
			"label": _("Average of Progress(%)"),
			"fieldtype": "Data",
			"width": 200
		}
		]
	)
	return columns

def get_action_data(filters):
	actions_list = frappe.db.get_list('Next Action', fields=["action", "progress", "weightage"], filters={"status":filters.get("status")})
	opportunity_total_weight = sum(action_temp.get("weightage") for action_temp in actions_list )
	action_progress_dict={}
	
	for action in actions_list:
		action_progress_dict.update({
			action.get("action") :calculate_action_progress(action,opportunity_total_weight)
		})
	return action_progress_dict

def calculate_action_progress(action,opportunity_total_weight):
	try:
		action_avg = round((action.get("weightage") / (opportunity_total_weight)) * action.get("progress"))
		return action_avg
	except ZeroDivisionError:
		return 0

def get_action_chart(action_data):
	chart_data ={
	'labels':list(action_data.keys()),
		'datasets': [
		{
			'name':_('Average of Progress (%)'),
			'values': [avg for key,avg in action_data.items()] 
		}
		]
	}
	chart = {
            "title": "Average of Progress (%)",
			"data": chart_data,
			"type": 'bar',
            'height': 100
		}
	return chart