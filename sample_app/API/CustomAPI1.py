import frappe
import json

def create_address(
    ref_doc,
    ref_doc_name,
    ref_doc_title,
    country,
    city,
    town
    ):
    address = frappe.new_doc('Address')
    address.update({
        'address_title': ref_doc_name,
        'address_line1': town,
        'country': country,
        'city': city
        })
    address.insert()
    address.append('links', {'link_doctype': ref_doc,
                   'link_name': ref_doc_name,
                   'link_title': ref_doc_title})
    address.save()
    data = json.loads(frappe.request.data)
    yankyapi = frappe.get_doc('YankyAPI', {'email_id': data.get('email_id')})
    yankyapi.address_line1 = address.name
    yankyapi.save(ignore_permissions=True)
    frappe.db.commit()


@frappe.whitelist()
def updateYankyAPI():
    data = json.loads(frappe.request.data)
    if not frappe.db.exists('YankyAPI', {'email_id': data.get('email_id')}):
        yankyapi = frappe.new_doc('YankyAPI')
        yankyapi.email_id = data.get('email_id')
    else:
        yankyapi = frappe.get_doc('YankyAPI', {'email_id': data.get('email_id')})
    if data.get('full_name'):
        yankyapi.full_name = data.get('full_name')
    if data.get('gender'):
        yankyapi.gender = data.get('gender')
    if data.get('company'):
        yankyapi.company = data.get('company')
    if data.get('designation'):
        yankyapi.designation = data.get('designation')
    if data.get('contact_no'):
        yankyapi.contact_no = data.get('contact_no')
    if data.get('state'):
        yankyapi.state = data.get('state')
    if data.get('pincode'):
        yankyapi.pincode = data.get('pincode')
    yankyapi.save(ignore_permissions=True)
    frappe.db.commit()
    create_address(ref_doc='YankyAPI', ref_doc_name=yankyapi.name,
                   ref_doc_title=yankyapi.full_name,
                   country=data.get('country'), city=data.get('city'),
                   town=data.get('town'))