import frappe
import json

@frappe.whitelist()
def createUser():
    data = json.loads(frappe.request.data)
    if frappe.db.exists('User', {'email': data.get('email')}):
        frappe.msgprint("User already exist.")
    else:
        user = frappe.new_doc('User')
        user.first_name = data.get('first_name')
        user.last_name = data.get('last_name')
        user.username = data.get('username')
        user.email = data.get('email')
        user.gender = data.get('gender')
        user.phone = data.get('phone')
        user.birth_date = data.get('birth_date')
        user.location = data.get('location')
    user.save(ignore_permissions=True)
    frappe.db.commit()
    frappe.msgprint("User-created Successfully.")

@frappe.whitelist()
def updateUser():
    data = json.loads(frappe.request.data)
    if not frappe.db.exists('User', {'email': data.get('email')}):
        user = createUser()
    else:
        user = frappe.get_doc('User', {'email': data.get('email')})
    if data.get('first_name'):
        user.first_name = data.get('first_name')
    if data.get('last_name'):
        user.last_name = data.get('last_name')
    if data.get('time_zone'):
        user.time_zone = data.get('time_zone')
    if data.get('username'):
        user.username = data.get('username')
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
    user.save(ignore_permissions=True)
    frappe.db.commit()
    frappe.msgprint("User Updated Successfully")