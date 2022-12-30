# Copyright (c) 2013, Leader Group and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from leadergroup.utils import get_accounts, get_tax_invoice_details

def execute(filters=None):
    columns, data = [], []
    account_list = []
    gran_taxable_amount = 0
    gran_vat_amount = 0
    gran_total_amount = 0

    columns = get_columns(filters, columns)

    if filters.get("account_list"):
        account_list = frappe.db.get_list('Account',
            filters = {'name': ['in', filters.get("account_list")]},
            fields = ['name', 'tax_rate']
        )
    else:
        account_list = get_accounts(filters)

    if account_list:
        for account in account_list:
            tot_taxable_amount = 0
            tot_vat_amount = 0
            tot_total_amount= 0
            is_return = 0
            additional_columns = "I.posting_date, I.return_against, I.customer, I.tax_id"
            if filters.get("invoice_type") == "Sales Adjustment":
                is_return = 1
            
            tax_invoice_data = get_tax_invoice_details(filters, "sales", account, is_return, additional_columns)
            if tax_invoice_data:
                data.append({"account_head" : frappe.bold("Standard Rate " + str(account.get("tax_rate"))+ "%" )})

                for invoice_tax  in tax_invoice_data :
                    invoice_tax['return_against_date'] = frappe.db.get_value("Sales Invoice", invoice_tax.get("return_against"), ["posting_date"])
                    tot_taxable_amount += invoice_tax.get("taxable_amount")
                    tot_vat_amount += invoice_tax.get("vat_amount")
                    tot_total_amount += invoice_tax.get("base_total")
                data.extend(tax_invoice_data)

                #adding groupwise tax total
                data.append(
                    {
                    "tax_id" : frappe.bold("TOTAL"),
                    "vat_amount" : tot_vat_amount,
                    "taxable_amount" : tot_taxable_amount,
                    "base_total" : tot_total_amount
                    }
                )
                gran_taxable_amount += tot_taxable_amount
                gran_vat_amount += tot_vat_amount
                gran_total_amount += tot_total_amount

                #adding empty row
                data.append({"account_head" : ""})

        #total of all taxes data
        data.append(
            {
            "tax_id" : frappe.bold("GRAND TOTAL"),
            "taxable_amount" : gran_taxable_amount,
            "vat_amount" : gran_vat_amount, 
            "base_total" : gran_total_amount
            }
        )
    return columns, data
   
def get_columns(filters, columns):
    columns.extend([
        {
            "label": ("Date"),
            "fieldname": "posting_date",
            "fieldtype": "Date",
            "width": "100"
        },
        {
            "label": ("Reference Document"),
            "fieldname": "name",
            "fieldtype": "Link",
            "options": "Sales Invoice",
            "width": "180"
        }
    ])
    if filters.get("invoice_type") == "Sales Adjustment":
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
                "fieldtype": "Link",
                "options": "Sales Invoice",
                "width": "180"
            }
        ])
    
    columns.extend([
        {
            "fieldname": "customer",
            "label": _("Customer"),
            "fieldtype": "Link",
            "options": "Customer",
            "width": 120
        },
        {
            "fieldname": "tax_id",
            "label": _("VAT No"),
            "fieldtype": "Data",
            "width": 120
        },
        {
            "fieldname": "account_head",
            "label": _("VAT Type"),
            "fieldtype": "Data",
            "width": 200
        },
        {
            "fieldname": "rate",
            "label": _("VAT Rate"),
            "fieldtype": "Float",
            "width": 120
        },
        {
            "fieldname": "taxable_amount",
            "label": _("Taxable Amount"),
            "fieldtype": "Currency",
            "width": 120
        },
        {
            "fieldname": "vat_amount",
            "label": _("VAT Amount"),
            "fieldtype": "Currency",
            "width": 120
        },
        {
            "fieldname": "base_total",
            "label": _("Total Amount"),
            "fieldtype": "Currency",
            "width": 120
        }
    ])
    return columns