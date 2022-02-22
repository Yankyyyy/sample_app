from __future__ import unicode_literals
import frappe
import json

@frappe.whitelist()
def createDoctypeEntries():
    # function to create Any Doctype Entries
    if frappe.request.data:
        data = json.loads(frappe.request.data)
        if data.get("doctype"):
            doctype = data.get("doctype")
            if not frappe.db.exists("DocType", {"name": doctype}):
                return doctype+" DocType Does not Exist in FoxERP"
            else:
                doctype_entry = frappe.new_doc(doctype)
                for i in data:
                    if type(data.get(i)) is not list :
                        setattr(doctype_entry, i, data.get(i))
                    else:
                        for j in data.get(i):
                            doctype_entry.append(i, j)
                doctype_entry.insert(ignore_permissions=True)
                doctype_entry.submit()
                return doctype_entry.name +" Entry Created Successfully"