# Copyright (c) 2013, Yanky and contributors
# For license information, please see license.txt

# import frappe


import frappe

def execute(filters=None):
	columns, data = [], []
	columns = get_columns()
	yanky_data = get_yanky_data(filters)
	for person in yanky_data:
		temp_dict = {
		"first_name":person.get("first"),
		"last_name":person.get("last_name"),
		"gender":person.get("last_name"),
		"contact":person.get("gender"),
		"dob":person.get("dob"),
		"age":person.get("age")
		}
		data.append(temp_dict)
	return columns, data

def get_columns():
	columns = ["" for column in range(6)]
	columns[0] = {
		"label": ("First Name"),
		"fieldname": "first_name",
		"fieldtype": "Link",
		"options": "YankyDT"
	}
	columns[1] = {
		"label": ("Last Name"),
		"fieldname": "last_name",
		"width": 150
	}
	columns[2] = {
		"label": ("Gender"),
		"fieldname": "gender",
		"width": 100
	}
	columns[3] = {
		"label": ("Contact"),
		"fieldname": "contact",
		"width": 150
	}
	columns[4] = {
		"label": ("DoB"),
		"fieldname": "dob",
		"fieldtype": "Date"
	}
	columns[5] = {
		"label": ("Age"),
		"fieldname": "age",
		"width": 50
	}
	return columns

def get_yanky_data(filters) :
	if filters:
		query = "select first, last_name, gender, contact, dob, age from tabYankyDT where first = '" + str(filters.get("first_name_filter")) + "'"
		yanky_data  = frappe.db.sql(query, as_dict=1) 
	else:
		yanky_data  = frappe.db.sql("""select first, last_name, gender, contact, dob, age from tabYankyDT """, as_dict=1) 
	
	return yanky_data