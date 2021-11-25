import frappe

@frappe.whitelist()
def example_func(b_year, p_year):
	age = p_year - b_year
	return age
