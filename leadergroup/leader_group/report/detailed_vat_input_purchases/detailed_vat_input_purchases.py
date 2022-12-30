# Copyright (c) 2022, Leader Group and contributors
# For license information, please see license.txt

import frappe
from leadergroup.utils import get_accounts, get_tax_invoice_details

def execute(filters=None):
    columns, data = [], []
    columns = get_columns(filters, columns)
    data = get_data(filters, data)
    return columns, data

def get_columns(filters, columns):
    columns.extend([
        {
            "label": ("Date"),
            "fieldname": "posting_date",
            "fieldtype": "Date",
            "width": "180"
        },
        {
            "label": ("Document"),
            "fieldname": "document",
            "fieldtype": "Data",
            "width": "180",
            "hidden": 1
        },
        {
            "label": ("Reference Document"),
            "fieldname": "name",
            "fieldtype": "Dynamic Link",
            "options": "document",
            "width": "180"
        }
    ])
    
    if filters.get("invoice_type") == "Purchase Adjustment":
        columns.extend([
            {
                "label": ("Return Against(Date)"),
                "fieldname": "return_against_date",
                "fieldtype": "Date",
                "width": "180"
            },
            {
                "label": ("Return Against"),
                "fieldname": "return_against",
                "fieldtype": "Dynamic Link",
                "options": "document",
                "width": "180"
            }
        ])
    
    columns.extend([
        {
            "label": ("Supplier Invoice No."),
            "fieldname": "bill_no",
            "width": "200"
        },
        {
            "label": ("Supplier Name"),
            "fieldname": "supplier",
            "fieldtype": "Data",
            "width": "200"
        },
        {
            "label": ("Vendor VAT No"),
            "fieldname": "tax_id",
            "width": "150"
        },
        {
            "label": ("VAT Type"),
            "fieldname": "account_head",
            "width": "200"
        },
        {
            "label": ("VAT Rate"),
            "fieldname": "rate",
            "fieldtype": "Float",
            "width": "200"
        },
        {
            "label": ("Taxable Amount"),
            "fieldname": "taxable_amount",
            "fieldtype": "Currency",
            "width": "200"
        },
        {
            "label": ("VAT Amount"),
            "fieldname": "vat_amount",
            "fieldtype": "Currency",
            "width": "200"
        },
        {
            "label": ("Total Amount"),
            "fieldname": "base_total",
            "fieldtype": "Currency",
            "width": "200"
        }
    ])
    return columns

def get_data(filters, data):
    account_list = []
    grand_taxable_amount = 0
    grand_vat_amount = 0
    grand_total_amount = 0

    if filters.get("account_list"):
        account_list = frappe.db.get_list('Account',
            filters = {'name': ['in', filters.get("account_list")]},
            fields = ['name', 'tax_rate']
        )

    if filters.get("invoice") is None or filters.get("invoice") == "Local Purchase":
        if not filters.get("account_list"):
            account_list =  get_accounts(filters, None, 'VAT', ['reverse charge mechanism', 'business expense', 'financial charge'])
        
        if account_list:
            for account in account_list:
                # get local purchase charges from purchase invoice and journal entry
                data, net_taxable_amount, net_vat_amount, net_total_amount = get_invoice_details(filters, account, data, "Local Purchase")
                grand_taxable_amount += net_taxable_amount
                grand_vat_amount += net_vat_amount
                grand_total_amount += net_total_amount

    if filters.get("invoice") is None or filters.get("invoice") == "Financial Charges":
        if not filters.get("account_list"):
            account_list =  get_accounts(filters, None, 'financial charge', ['reverse charge mechanism'])
        
        if account_list:
            for account in account_list:
                if 'financial charge' in account.get('name').lower():
                    # get financial charges entry from purchase invoice and journal entry
                    data, net_taxable_amount, net_vat_amount, net_total_amount = get_invoice_details(filters, account, data, "Financial Charges")
                    grand_taxable_amount += net_taxable_amount
                    grand_vat_amount += net_vat_amount
                    grand_total_amount += net_total_amount

    if filters.get("invoice") is None or filters.get("invoice") == "Business Expenses":
        if not filters.get("account_list"):
            account_list =  get_accounts(filters, None, 'business expense', ['reverse charge mechanism'])
        
        if account_list:
            for account in account_list:
                if 'business expense' in account.get('name').lower():
                    # get business expense charges from purchase invoice and journal entry
                    data, net_taxable_amount, net_vat_amount, net_total_amount = get_invoice_details(filters, account, data, "Business Expenses")
                    grand_taxable_amount += net_taxable_amount
                    grand_vat_amount += net_vat_amount
                    grand_total_amount += net_total_amount

    data.append(
        {
            "tax_id" : frappe.bold("GRAND TOTAL"),
            "taxable_amount" : grand_taxable_amount,
            "vat_amount" : grand_vat_amount,
            "base_total" : grand_total_amount
        }
    )
    return data

def get_invoice_details(filters, account, data, header_label):
    invoice_data = []
    net_taxable_amount = 0
    net_vat_amount = 0
    net_total_amount= 0
    is_return = 0
    if filters.get("invoice_type") == "Purchase Adjustment":
        is_return = 1

    # get purchase invoice which having vat charges as per account name in taxes and charges table
    additional_columns = "I.posting_date, I.return_against, I.bill_no, I.supplier, I.tax_id, 'Purchase Invoice' as 'document'"
    invoice_data.extend(get_tax_invoice_details(filters, "purchase", account, is_return, additional_columns))

    # get Journal Entry which having vat charges as per account name
    additional_columns = "I.posting_date, TC.against_account as 'supplier', 'Journal Entry' as 'document'"
    invoice_data.extend(get_tax_invoice_details(filters, "journal", account, is_return, additional_columns))
    if invoice_data:
        data.append(
            {
                "bill_no" : frappe.bold("VAT on " + header_label + " Standard Rate " + str(account.get("tax_rate"))+ "%"),
            }
        )
        for invoice in invoice_data:
            invoice['return_against_date'] = frappe.db.get_value("Purchase Invoice", invoice.get("return_against"), ["posting_date"])
            net_taxable_amount += invoice.get("taxable_amount")
            net_vat_amount += invoice.get("vat_amount")
            net_total_amount += invoice.get("base_total")
        data.extend(invoice_data)
        data.append(
            {
                "tax_id" : frappe.bold("TOTAL"),
                "taxable_amount" : net_taxable_amount,
                "vat_amount" : net_vat_amount,
                "base_total" : net_total_amount
            }
        )
    return data, net_taxable_amount, net_vat_amount, net_total_amount
