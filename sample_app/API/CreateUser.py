import frappe
import json



@frappe.whitelist()
def createUser():
    data = json.loads(frappe.request.data)
    if frappe.db.exists('User', {'email': data.get('email')}):
        return "User already exists."
    else:
        user = frappe.new_doc('User')
    if data.get('first_name'):
        user.first_name = data.get('first_name')
    if data.get('last_name'):
        user.last_name = data.get('last_name')
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
    return "User-created Successfully."