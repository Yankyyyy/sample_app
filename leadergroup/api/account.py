# Copyright (c) 2021, Leader Group and contributors
# For license information, please see license.txt

import frappe
from stripe import Account

def autoname(doc, method):
    set_account_number(doc, method)
    from erpnext.accounts.utils import get_autoname_with_number
    doc.name = get_autoname_with_number(doc.get('account_number'), doc.get('account_name'), None, doc.get('company'))

def set_account_number(doc, method):
    # set account number auto increment of Parent Account
    if not doc.get('account_number'):
        if doc.get('parent_account'):
            if frappe.db.exists("Account", doc.get('parent_account')):
                account_number = frappe.db.get_value('Account', doc.get('parent_account'), 'account_number')
                if account_number:
                    account_number = int(account_number) + 1

                    number_exists = True
                    while number_exists == True:
                        verify_number = frappe.db.sql("""select name, account_number
                            from `tabAccount`
                            where account_number = '{0}'
                            """.format(account_number), as_dict=1)
                        if verify_number:
                            account_number = int(account_number) + 1
                        else:
                            number_exists = False
                    
                    doc.account_number =  account_number
