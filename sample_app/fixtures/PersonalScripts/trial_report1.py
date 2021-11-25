import frappe

def execute(filters=None):
	columns, data = [], []
	columns = get_columns()
	employee_data = get_employee_data()

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
		"fieldtype": "Data",
		"width": 150
	}
	columns[1] = {
		"label": ("First Name"),
		"fieldname": "first_name",
		"width": 150
	}
	columns[2] = {
		"label": ("Second Name"),
		"fieldname": "second_name",
		"width": 150
	}
	columns[3] = {
		"label": ("Full Name"),
		"fieldname": "full_name",
		"width": 200
	}
	columns[4] = {
		"label": ("Phone Number"),
		"fieldname": "phone_number",
		"fieldtype": "int",
		"width": 150
	}
	columns[5] = {
		"label": ("Email"),
		"fieldname": "email",
		"width": 200
	}
	return columns

def get_employee_data() :
	employee_data  = frappe.db.sql("""select name,first_name,last_name,employee_name,cell_number,personal_email from `tabEmployee` """, as_dict=1) 
	return employee_data