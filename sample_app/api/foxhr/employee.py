# -*- coding: utf-8 -*-
# Copyright (c) 2022, FoxERP and contributors
# For license information, please see license.txt

import frappe
import json
from sample_app.utils import createAPIErrorLog
from sample_app.api.foxhr.user import update_user_status, createUser

@frappe.whitelist()
def createEmployee():
    # function to create a employee from foxhr
    user = {}
    try:
        if frappe.request.data:
            data = json.loads(frappe.request.data)
            employee = frappe.new_doc('Employee')
            employee = map_employee_field(data, employee)
            if data.get("is_foxerp_user") == 1:
                user = createUser()
                employee.user_id = user.get("user_id")
            employee.save(ignore_permissions=True)
            frappe.db.commit()
            return {
                "emp_id" : employee.get("name"),
                "user_id" : employee.get("user_id"),
                "username" : user.get("username"),
                "message" : "Employee Created"
            }
    except Exception:
        createAPIErrorLog(frappe.get_traceback())

@frappe.whitelist()
def updateEmployee():
    # function to update an existing employee from foxhr
    user = {}
    try:
        if frappe.request.data:
            data = json.loads(frappe.request.data)
            emp_id = data.get("emp_id")
            if emp_id:
                employee = frappe.get_doc("Employee", emp_id)
                employee = map_employee_field(data, employee)

                if employee.get("is_foxerp_user") != data.get("is_foxerp_user"):
                    if employee.get("user_id"):
                        update_status = update_user_status(employee.get("user_id"), data.get("is_foxerp_user"))
                    else:
                        if data.get("is_foxerp_user") == 1:
                            user = createUser()
                            employee.user_id = user.get("user_id")
                
                employee.save(ignore_permissions=True)
                frappe.db.commit()
                return {
                    "emp_id" : employee.get("name"),
                    "user_id" : employee.get("user_id"),
                    "username" : user.get("username"),
                    "message" : "Employee Data Updated !"
                }
    except Exception:
        createAPIErrorLog(frappe.get_traceback())

@frappe.whitelist()
def disableEmployee(emp_id):
    # Function to disable Employee using API from FoxHR
    try:
        if emp_id:
            if not frappe.db.exists("Employee", emp_id):
                return {
                    "emp_id" : emp_id,
                    "message" : "Employee Does not Exist in FoxERP"
                }
            else:
                emp_data = frappe.get_doc("Employee", emp_id)
                if emp_data.get("user_id"):
                    update_status = update_user_status(emp_data.get("user_id"), 0)
                return {
                    "emp_id" : emp_id,
                    "message" : "Employee Disabled Successfully"
                }
    except Exception:
        createAPIErrorLog(frappe.get_traceback())

def map_employee_field(data, employee):
    if employee.get("company") != data.get("company"):
        employee.company = data.get("company")
    if employee.get("first_name") != data.get("first_name"):
        employee.first_name = data.get("first_name")
    if employee.get("middle_name") != data.get("middle_name"):
        employee.middle_name = data.get("middle_name")
    if employee.get("last_name") != data.get("last_name"):
        employee.last_name = data.get("last_name")
    if employee.get("employment_type") != data.get("employment_type"):
        employee.employment_type = data.get("employment_type")
    if employee.get("status") != data.get("status"):
        employee.status = data.get("status")
    if employee.get("gender") != data.get("gender"):
        employee.gender = data.get("gender")
    if employee.get("date_of_birth") != data.get("birth_date"):
        employee.date_of_birth = data.get("birth_date")
    if employee.get("date_of_joining") != data.get("date_of_joining"):
        employee.date_of_joining = data.get("date_of_joining")
    if employee.get("employee_number") != data.get("employee_id"):
        employee.employee_number = data.get("employee_id")
    if employee.get("scheduled_confirmation_date") != data.get("date_of_joining"):
        employee.scheduled_confirmation_date = data.get("date_of_joining")
    if employee.get("final_confirmation_date") != data.get("date_of_joining"):
        employee.final_confirmation_date = data.get("date_of_joining")
    if employee.get("department") != data.get("department"):
        employee.department = data.get("department")
    if employee.get("designation") != data.get("job_title"):
        employee.designation = data.get("job_title")
    if employee.get("reports_to") != data.get("line_manager"):
        employee.reports_to = data.get("line_manager")

    if employee.get("grade") != data.get("grade"):
        employee.grade = data.get("grade")
    if employee.get("cell_number") != data.get("phone"):
        employee.cell_number = data.get("phone")
    if employee.get("permanent_address") != data.get("address"):
        employee.permanent_address = data.get("address")
    if employee.get("current_address") != data.get("address"):
        employee.current_address = data.get("address")

    employee.prefered_contact_email = "Company Email"
    if employee.get("company_email") != data.get("email"):
        employee.company_email = data.get("email")
    if employee.get("passport_number") != data.get("passport_number"):
        employee.passport_number = data.get("passport_number")
    if employee.get("valid_upto") != data.get("passport_expiry_date"):
        employee.valid_upto = data.get("passport_expiry_date")
    if employee.get("marital_status") != data.get("marital_status"):
        employee.marital_status = data.get("marital_status")
    if data.get("education") is not None:
        employee.education = None
        for education in data.get("education"):
            employee.append("education", {
                "school_univ": education.get("institution_name"),
                "qualification": education.get("degree"),
                "level": education.get("major"),
                "year_of_passing": education.get("graduation_date")
            })
    if data.get("internal_work_history") is not None:
        employee.internal_work_history = None
        for internal_work_history in data.get("internal_work_history"):
            employee.append("internal_work_history", {
                "designation": internal_work_history.get("job_title"),
                "from_date": internal_work_history.get("effective_date")
            })
    return employee
