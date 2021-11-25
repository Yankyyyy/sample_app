# Copyright (c) 2013, Yanky and contributors
# For license information, please see license.txt

# import frappe

import frappe

def execute(filters=None):
	columns, data = [], []
	columns = get_columns()
	employee_data = get_employee_data(filters)

#	data = [{"employee_id":"A001","first_name":"Yanky","second_name":"Potter","full_name":"Yanky Potter","phone_number":"6379573186","email":"tamocha44@gmail.com"}] //"This is for static data"
	
	for employee in employee_data:
		temp_dict = {
		"employee_id":employee.get("name"),
		"first_name":employee.get("first_name"),
		"second_name":employee.get("last_name"),
		"full_name":employee.get("employee_name"),
		"phone_number":employee.get("cell_number"),
		"email":employee.get("personal_email")
		}
		data.append(temp_dict)
	return columns, data

def get_columns():
	columns = ["" for column in range(6)]
	columns[0] = {
		"label": ("Employee ID"),
		"fieldname": "employee_id",
		"fieldtype": "Link",
		"options": "Employee"
	}
	columns[1] = {
		"label": ("First Name"),
		"fieldname": "first_name",
		"width": 160
	}
	columns[2] = {
		"label": ("Second Name"),
		"fieldname": "second_name",
		"width": 160
	}
	columns[3] = {
		"label": ("Full Name"),
		"fieldname": "full_name",
		"width": 250
	}
	columns[4] = {
		"label": ("Phone Number"),
		"fieldname": "phone_number",
		"width": 160
	}
	columns[5] = {
		"label": ("Email"),
		"fieldname": "email",
		"fetch from": "employee_id.personal_email"
	}
	return columns

def get_employee_data(filters) :
	if filters:
		query = "select name, first_name, last_name, employee_name, cell_number, personal_email from tabEmployee where name = '" + str(filters.get("employee_id_filter")) + "'"
		employee_data  = frappe.db.sql(query, as_dict=1) 

	# if filters:
	# 	query = "select name, first_name, last_name, employee_name, cell_number, personal_email from tabEmployee where name = '" + str(filters.get("first_name_filter")) + "'"
	# 	employee_data  = frappe.db.sql(query, as_dict=1) 

	# if filters:
	# 	query = "select name, first_name, last_name, employee_name, cell_number, personal_email from tabEmployee where name = '" + str(filters.get("last_name_filter")) + "'"
	# 	employee_data  = frappe.db.sql(query, as_dict=1) 

	# if filters:
	# 	query = "select name, first_name, last_name, employee_name, cell_number, personal_email from tabEmployee where name = '" + str(filters.get("employee_name_filter")) + "'"
	# 	employee_data  = frappe.db.sql(query, as_dict=1) 

	# if filters:
	# 	query = "select name, first_name, last_name, employee_name, cell_number, personal_email from tabEmployee where name = '" + str(filters.get("cell_number_filter")) + "'"
	# 	employee_data  = frappe.db.sql(query, as_dict=1) 

	# if filters:
	# 	query = "select name, first_name, last_name, employee_name, cell_number, personal_email from tabEmployee where name = '" + str(filters.get("personal_email_filter")) + "'"
	# 	employee_data  = frappe.db.sql(query, as_dict=1) 
	
	else:
		employee_data  = frappe.db.sql("""select name,first_name,last_name,employee_name,cell_number,personal_email from tabEmployee """, as_dict=1) 
	
	return employee_data
# #My code :
# def get_columns():
# 	columns = ["" for column in range(4)]
# 	columns[0] = {
# 		"label": ("First Name"),
# 		"fieldname": "first_name",
# 		"fieldtype": "Link",
# 		"options": "YankyDT",
# 		"width": 150
# 	}
# 	columns[1] = {
# 		"label": ("Last Name"),
# 		"fieldname": "last_name",
# 		"fieldtype": "Data"
# 		"fetch from": "first_name.last_name",
# 		"width": 150
# 	}
# 	columns[2] = {
# 		"label": ("Gender"),
# 		"fieldname": "gender",
# 		"fieldtype": "Select",
# 		"options": "Male\nFemale\nOthers",
#      	"default": "Male",
# 		"width": 100
# 	}
# 	columns[3] = {
# 		"label": ("DoB"),
# 		"fieldname": "dob",
# 		"fieldtype": "Date",
# 		"width": 100
# 	}
# 	return columns
#to be continue....



	# data =[{"employee_name":"Suresh","employee_phone":"907899"},
	# {"employee_name":"Yanky","employee_phone": "9804569"},
	# {"employee_name":"Amal","employee_phone": "9345809"},
	# {"employee_name":"Pradeep","employee_phone": "97654809"}
	# ]
	
# 	employee_data  = get_employee_data()
# 	for employee in  employee_data :
# 		temp_dic ={"employee_name":employee.get("name"),"employee_phone":"907899","first_name":employee.get("first_name")}
# 		data.append(temp_dic)	
	# return columns, data

# def get_employee_data() :
# 	employee_data  = frappe.db.sql("""select name,first_name from `tabEmployee` """, as_dict=1) 
# 	return employee_data
