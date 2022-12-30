# -*- coding: utf-8 -*-
# Copyright (c) 2022, FoxERP and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.utils import now, date_diff, format_datetime
from foxerp.foxerp.doctype.license_and_usage_info.license_and_usage_info import get_active_count, validate_user_count

def validate_active_user(doc, method):
    """
    Validating active user count against allowed  user count when a new user is created or when  enabling an existing user
    Active user count will be increased  when  a new user is created or when  enabling an existing user 
    Active user count will be decreased when  disabling an existing user
    """
    active_user = get_active_count()
    
    if doc.is_new():
        #only new user entry will be validated
        active_user += doc.get("enabled")
    else:
        #Validting if enabled is modified on save
        if not doc.get("enabled") == frappe.db.get_value("User", doc.get("name"), "enabled"):
            if doc.get("enabled") != 1:
                active_user -= 1
            else:
                active_user += 1

    allowed_user = frappe.db.get_single_value("License and Usage Info", "allowed_user")
    validate_user_count(allowed_user, active_user)
    frappe.db.set_value("License and Usage Info", "License and Usage Info", "active_user", active_user)

def validate_license_info(login_manager):
    # To check whether Fox erp license valid or not
    if login_manager.user != "Administrator":
        license_and_usage_info = frappe.get_single('License and Usage Info')
        license_start_date = license_and_usage_info.get("start_date")
        license_end_date = license_and_usage_info.get("end_date")
        current_datetime = now()

        if license_start_date and license_start_date > current_datetime:
            frappe.throw("Your Fox ERP License will start on <b>"+ str(format_datetime(license_start_date)) +".</b> Please Contact Fox ERP Team")

        if license_end_date:
            if license_end_date < current_datetime:
                frappe.throw("Your Fox ERP License has expired on <b>"+ str(format_datetime(license_end_date)) +".</b> Please Contact Fox ERP Team")
            else:
                expiry_alert_before_in_days = license_and_usage_info.get("expiry_alert_before_in_days")
                if expiry_alert_before_in_days > 0:
                    license_days = date_diff(license_end_date, current_datetime)
                    if license_days <= expiry_alert_before_in_days:
                        frappe.msgprint("Your Fox ERP License is about to expire in <b>"+ str(license_days) +" days. </b>")
