# Copyright (c) 2013, Leader Group and contributors
# For license information, please see license.txt

import frappe
from frappe import _

def execute(filters=None):
	filters.pop('date', None)
	columns, data = [], []
	columns = get_columns(filters)
	solutions_data = frappe.db.get_all("Solution Offerings",
            filters=filters,
            fields=["parent",
                    'code',
                    "maturity_level",
                    "description"
                ],
            order_by="creation")
	solution_wise_offerings_dict = {}

	for solution in  solutions_data:
		if solution_wise_offerings_dict.get(solution.get("parent")):
			solution_wise_offerings_dict[solution.get("parent")].append(solution)
		else:
			solution_wise_offerings_dict[solution.get("parent")] = [solution]
	
	for solution,solution_data in  solution_wise_offerings_dict.items():
		row_dict ={
			"solution":solution
		}
		for row in solution_data:
			row_dict.update({
			row.get("description"): row.get("code") +"."+row.get("maturity_level")
			})
		data.append(row_dict)
	return columns, data

def get_columns(filters):
	columns = []
	descriptions = frappe.db.sql("""select distinct(description) from `tabSolution Offerings`""" ,as_dict =1)
	columns.append( {
		"fieldname": "solution",
		"label": _("Solution"),
		"fieldtype": "Link",
		"options": "Solution",
		"width": 200
	} )
	for data in descriptions:
		columns.append(
			{
			"label": _(data.get("description")),
			"fieldname": data.get("description"),
			"width": 120
			}
		)
	return columns