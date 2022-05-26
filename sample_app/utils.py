# -*- coding: utf-8 -*-
# Copyright (c) 2020, Leader Investment Group

import json
import requests
import frappe
import inspect

def createAPIErrorLog(error):
    """Create error log according the method from where createAPIErrorLog been called"""
    error_log =  frappe.new_doc("Error Log")
    error_log.method = inspect.stack()[1][3] #called method name will be fetched
    error_log.error = error
    error_log.save(ignore_permissions=True)

def get_accounts(filters, vat_rate=None, account_name="VAT", exclude_account_name=[]):
    # Get VAT Account List as per tax rate/account name or List of All VAT Accounts
    sql_conditions = ""
    if filters.get("company"):
        sql_conditions += " and company = '" + filters.get("company") +"'"

    if account_name:
        sql_conditions += " and account_name like '%" + account_name +"%'"
    
    if vat_rate is not None:
        sql_conditions += " and tax_rate = " + str(vat_rate)

    if exclude_account_name:
        for account in exclude_account_name:
            sql_conditions += " and account_name not like '%" + str(account) +"%'"

    account_list = """select name, tax_rate
                from `tabAccount`
                where 
                    account_type = 'Tax'
                    {0};""".format(sql_conditions)
    account_list = frappe.db.sql(account_list, as_dict=1)
    return account_list


def get_tax_invoice_details(filters, invoice_name, account, is_return = None, additional_columns = ""):
    """To get taxes and charges applied invoice as per account name. 
    We can filter return invoice and non invoice also."""
    sql_conditions = ""
    invoice_doctype = ""
    tax_doctype = ""
    if invoice_name == "sales":
        invoice_doctype = "Sales Invoice"
        tax_doctype = "Sales Taxes and Charges"
    elif invoice_name == "purchase":
        invoice_doctype = "Purchase Invoice"
        tax_doctype = "Purchase Taxes and Charges"
    elif invoice_name == "journal":
        invoice_doctype = "Journal Entry"
        tax_doctype = "Journal Entry Account"

    if filters.get("company"):
        sql_conditions += " and I.company = '" + filters.get("company") +"'"

    if filters.get("from_date"):
        sql_conditions += " and I.posting_date >= '" + filters.get("from_date") +"'"
    
    if filters.get("to_date"):
        sql_conditions += " and I.posting_date <= '" + filters.get("to_date") +"'"

    if is_return is not None:
        if invoice_name == "journal":
            if is_return == 1:
                sql_conditions += " and TC.debit = 0"
            else:
                sql_conditions += " and TC.credit = 0"
        else:
            sql_conditions += " and I.is_return = " + str(is_return)

    if additional_columns:
        additional_columns += ", "

    if invoice_name == "journal":
        invoice_list = """select I.name, TC.account as 'account_head', {4} {5} as 'rate',
                    if(TC.debit != 0,TC.debit,TC.credit) as 'vat_amount',
                    if({5}!=0,(if(TC.debit != 0,TC.debit,TC.credit)*100)/{5},0) as 'taxable_amount',
                    if({5}!=0,(if(TC.debit != 0,TC.debit,TC.credit)*100)/{5},0) + if(TC.debit != 0,TC.debit,TC.credit) as 'base_total'
                from `tab{0}` TC
                inner join `tab{1}` I
                    on I.name = TC.parent and TC.parenttype = '{1}'
                where I.docstatus = 1 and TC.parenttype = '{1}' and TC.account = '{2}'
                    {3} order by I.posting_date desc ;""".format(tax_doctype, invoice_doctype, account.get("name"), sql_conditions, additional_columns, account.get("tax_rate"))
        invoice_list = frappe.db.sql(invoice_list, as_dict=1)
    else:
        invoice_list = """select I.name, TC.account_head, {4} TC.rate, TC.item_wise_tax_detail,
                    ABS(TC.base_tax_amount_after_discount_amount) as 'vat_amount'
                from `tab{0}` TC
                inner join `tab{1}` I
                    on I.name = TC.parent and TC.parenttype = '{1}'
                where I.docstatus = 1 and TC.parenttype = '{1}' and TC.account_head = '{2}'
                    {3} order by I.posting_date desc ;""".format(tax_doctype, invoice_doctype, account.get("name"), sql_conditions, additional_columns)
        invoice_list = frappe.db.sql(invoice_list, as_dict=1)

        for invoice in invoice_list:
            count = 0
            taxable_amount = 0
            zero_taxable_amount = 0
            
            item_tax_map = json.loads(invoice.get("item_wise_tax_detail")) if invoice.get("item_wise_tax_detail") else {}
            for item, tax in item_tax_map.items():
                if tax[0] !=0 :
                    invoice["rate"] = tax[0]
                invoice_item = """select ABS(base_net_amount) as 'base_net_amount'
                        from `tab{0} Item`
                        where item_code = '{1}' 
                            and parent = '{2}'""".format(invoice_doctype, item, invoice.get("name"))
                invoice_item = frappe.db.sql(invoice_item, as_dict=1)

                for item_value in invoice_item:
                    zero_taxable_amount += item_value.get("base_net_amount")
                    if tax[0] !=0 :
                        count += 1
                        taxable_amount += item_value.get("base_net_amount")
            if count == 0:
                invoice["taxable_amount"] = zero_taxable_amount
            else:
                invoice["taxable_amount"] = taxable_amount
            invoice["base_total"] = invoice["taxable_amount"] + invoice["vat_amount"]
    return invoice_list