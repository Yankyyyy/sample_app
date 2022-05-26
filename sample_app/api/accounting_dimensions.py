from __future__ import unicode_literals
import frappe

def after_save(doc,method):
    if doc.get("__islocal") == 1:
        for row in doc.items:
            if row.get("update_flag") != 1 :
                row.employee = None