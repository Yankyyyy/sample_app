import frappe
import json
from frappe.model.naming import append_number_if_name_exists
from foxerp.utils import createAPIErrorLog


@frappe.whitelist()
def validate_salary_component():
# function to check if a salary component exist and if not create one.
    try:
        data = json.loads(frappe.request.data)
        if not frappe.db.exists('Salary Component', {'salary_component': data.get('name'), 'type': data.get('type')}):
            salary_component = frappe.new_doc('Salary Component')
            if data.get('name'):
                salary_component.salary_component = data.get('name')
            if data.get('type'):
                salary_component.type = data.get('type')
            #create and validate salary component abbreviation
            salary_component.salary_component_abbr = ''.join([c[0] for c in
			    salary_component.salary_component.split()]).upper()
            salary_component.salary_component_abbr = salary_component.salary_component_abbr.strip()
            #alter the abbreviation by appending a number if a similar abbreviation already exist
            salary_component.salary_component_abbr = append_number_if_name_exists('Salary Component', salary_component.salary_component_abbr,
			    'salary_component_abbr', separator='_', filters={"name": ["!=", salary_component.name]})
            #create a row in accounts table with the default company
            salary_component.append("accounts",{
                        "company": frappe.defaults.get_user_default("Company") or frappe.defaults.get_global_default("Company")
                    })
            salary_component.save(ignore_permissions=True)
            frappe.db.commit()
        return "Done"
    except Exception:
        createAPIErrorLog(frappe.get_traceback())