# Copyright (c) 2022, Leader Group and contributors
# For license information, please see license.txt

import frappe
from frappe import _

def execute(filters=None):
	columns, data = [], []

	data = frappe.db.get_list('Opportunity',
		filters = filters,
		fields=['distinct opportunity_name'],
		order_by='opportunity_name asc'
	)

	owner_name_list = frappe.db.get_list('Opportunity',
		filters = filters,
		fields=['distinct converted_by'],
		order_by='converted_by asc'
	)

	for owner in owner_name_list:
		if owner.converted_by:
			owner['owner_name'] = frappe.db.get_value('User', owner.converted_by, 'full_name')

	columns = get_columns(columns, owner_name_list)

	for opportunity_name in data:
		if opportunity_name.opportunity_name:
			total_count = 0
			for owner in owner_name_list:
				if owner.converted_by:
					filters['converted_by'] = owner.converted_by
					filters['opportunity_name'] = opportunity_name.opportunity_name

					count = frappe.db.count('Opportunity', filters)
					opportunity_name[owner.converted_by] = count or 0
					total_count += count
			opportunity_name["total"] = total_count
	
	chart = get_open_task_chart(data, owner_name_list)
	return columns, data, None, chart

def get_columns(columns, owner_name_list):
	columns.extend([
		{
			"label": _("Opportunity Name"),
			"fieldname": "opportunity_name",
			"fieldtype": "Data",
			"width": "400"
		}
	])
	for column in owner_name_list:
		if column.converted_by:
			columns.append(
				{
					"label": _(column.owner_name),
					"fieldname": column.converted_by,
					"fieldtype": "Int",
					"width": "180"
				}
			)
	columns.extend([
		{
			"label": _("<b>Total</b>"),
			"fieldname": "total",
			"fieldtype": "Int",
			"width": "180"
		}
	])
	return columns

def get_open_task_chart(data, owner_name_list):
	datasets = []
	labels = []
	total_count = {}

	for i in data:
		labels.append(i.opportunity_name)
		for owner in owner_name_list:
			if owner.converted_by:
				if owner.converted_by in total_count:
					total_count[owner.converted_by] += i.get(owner.converted_by, 0)
				else:
					total_count[owner.converted_by] = i.get(owner.converted_by, 0)
	labels.append('Total')

	for owner in owner_name_list:
		values = []
		if owner.converted_by:
			for i in data:
				values.append(i.get(owner.converted_by, 0))
			values.append(total_count.get(owner.converted_by, 0))
			datasets.append(
				{
					'name': owner.owner_name,
					'chartType': "bar",
					'values': values
				}
			)
	
	chart_data = {
		'labels' : labels,
		'datasets' : datasets
	}

	chart = {
		"title": "Count of Owner Name",
		"data": chart_data,
		"type": 'axis-mixed',
		"height": 500,
		"barOptions": {
			"stacked": True,
			"spaceRatio": 0.5
		},
	}
	return chart
