# -*- coding: utf-8 -*-
# Copyright (c) 2020, Leader Investment Group
import frappe
import json
import requests
from foxerp.utils import createAPIErrorLog


@frappe.whitelist()
def createUser():
# function to update an existing user from foxhr
    try:
        data = json.loads(frappe.request.data)
        if frappe.db.exists('User', {'email': data.get('email')}):
            return "User already exists"
        else:
            user = frappe.new_doc('User')
            if data.get('first_name'):
                user.first_name = data.get('first_name')
            if data.get('last_name'):
                user.last_name = data.get('last_name')
            if data.get('email'):
                user.email = data.get('email')
            if data.get('gender'):
                user.gender = data.get('gender')
            if data.get('phone'):
                user.phone = data.get('phone')
            if data.get('birth_date'):
                user.birth_date = data.get('birth_date')
            if data.get('location'):
                user.location = data.get('location')
            user.username = frappe.scrub(data.get('first_name'))
            # strip space and @
            user.username = user.username.strip(" @")
            if user.username_exists():
                user.username = user.suggest_username()
            user.send_welcome_email = 0
            user.append('roles', {
                'role': 'Projects User'
            })
            user.save(ignore_permissions=True)
            frappe.db.commit()
            return {
                "user_id" : user.get("name"),
                "username" : user.get("username"),
                "message" : "User-Created Successfully"
            }
    except Exception:
        createAPIErrorLog(frappe.get_traceback())


@frappe.whitelist()
def updateUser():
# function to update an existing user from foxhr
    try:
        data = json.loads(frappe.request.data)
        if not frappe.db.exists("User", {"email": data.get("email")}):
            createUser()
        else:
            user_doc = frappe.get_doc("User", {"email": data.get("email")})

            if user_doc.first_name != data.get("first_name"):
                user_doc.first_name = data.get("first_name")

            if user_doc.last_name != data.get("last_name"):
                user_doc.last_name = data.get("last_name")

            if user_doc.gender != data.get("gender"):
                user_doc.gender = data.get("gender")

            if user_doc.phone != data.get("phone"):
                user_doc.phone = data.get("phone")

            if str(user_doc.birth_date) != str(data.get("birth_date")):
                user_doc.birth_date = data.get("birth_date")

            if user_doc.location != data.get("location"):
                user_doc.location = data.get("location")

            user_doc.save(ignore_permissions=True)
            frappe.db.commit()
            return "User data Updated !"
    except Exception:
        createAPIErrorLog(frappe.get_traceback())

@frappe.whitelist()
def disableUser():
    # Function to disable User using API from FoxHR
    try:
        if frappe.request.data:
            data = json.loads(frappe.request.data)
            if data.get("email"):
                update_status = update_user_status(data.get("email"), 0)
                return update_status
    except Exception:
        createAPIErrorLog(frappe.get_traceback())


def update_user_status(name, enabled = 1):
    # Function to enable or disable User
    user_status = "Enabled"
    if enabled != 1:
        user_status = "Disabled"

    if not frappe.db.exists("User", name):
        return {
            "user_id" : name,
            "message" : "User Does not Exist in FoxERP"
        }
    else:
        user_data = frappe.get_doc("User", name)
        if user_data.enabled == enabled:
            return {
                "user_id" : name,
                "message" : "User is Already "+ user_status
            }
        else:
            user_data.enabled = enabled
            user_data.save(ignore_permissions = True)
            frappe.db.commit()
            return {
                "user_id" : name,
                "message" : "User "+ user_status + " Successfully"
            }