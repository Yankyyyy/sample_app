# Copyright (c) 2022, FoxERP and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class LicenseandUsageInfo(Document):
    def validate(self):
        # validate start date and end date
        if self.start_date and self.end_date:
            if self.end_date < self.start_date:
                frappe.throw("End Date Cannot be less than Start Date")

        if self.expiry_alert_before_in_days and self.expiry_alert_before_in_days < 0:
            frappe.throw("Expiry Alert Before in days cannot be in Negative")

        """
        On Save Active user will be updated according to the enabled user count in  the system and validated against allowed_user value
        """
        active_user = get_active_count()
        validate_user_count(self.allowed_user, active_user)
        self.active_user = active_user

def get_active_count():
    excluded_active_user =["Administrator","Guest"] 
    active_user = frappe.db.count('User', filters={"name":('not in',excluded_active_user),"enabled":["=",1]})
    return active_user

def validate_user_count(allowed_user, active_user):
    if allowed_user > 0:
        if allowed_user < active_user:
            frappe.throw("You have exceeded User Limit. Allowed Active User - "+ str(allowed_user) +". To increase number of users please contact FoxERP Team")