# Copyright (c) 2013, Leader Group and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from leadergroup.utils import get_accounts, get_tax_invoice_details
from erpnext import get_company_currency

def execute(filters=None):
    columns, data = [], []
    columns = get_columns(filters)

    # Sales Vat Details
    invoice_name = "sales"
    total_sales_gross = 0
    total_sales_adjustment = 0
    total_sales_vat_amount = 0

    data.append({
        "particulars": frappe.bold("VAT on Sales:")
    })

    # get 15% sales vat total
    account_list = get_accounts(filters, 15)
    total_row, return_total_row = get_account_wise_tax_invoice(filters, invoice_name, account_list)
    data.append({
        "sr_no":"1",
        "particulars": "Standard rated sales (15%)",
        "invoice_name": invoice_name,
        "account_list": account_list,
        "gross": total_row.get("total_taxable_amount"),
        "adjustment": return_total_row.get("total_taxable_amount"),
        "vat_amount": total_row.get("total_vat_amount") - return_total_row.get("total_vat_amount")
    })
    total_sales_gross += total_row.get("total_taxable_amount")
    total_sales_adjustment += return_total_row.get("total_taxable_amount")
    total_sales_vat_amount += total_row.get("total_vat_amount") - return_total_row.get("total_vat_amount")

    # get 5% sales vat total
    account_list = get_accounts(filters, 5)
    total_row, return_total_row = get_account_wise_tax_invoice(filters, invoice_name, account_list)
    data.append({
        "sr_no":"1.1",
        "particulars": "Sales Subject to VAT at (5%)",
        "invoice_name": invoice_name,
        "account_list": account_list,
        "gross": total_row.get("total_taxable_amount"),
        "adjustment": return_total_row.get("total_taxable_amount"),
        "vat_amount": total_row.get("total_vat_amount") - return_total_row.get("total_vat_amount")
    })
    total_sales_gross += total_row.get("total_taxable_amount")
    total_sales_adjustment += return_total_row.get("total_taxable_amount")
    total_sales_vat_amount += total_row.get("total_vat_amount") - return_total_row.get("total_vat_amount")

    data.append({
        "sr_no":"2",
        "particulars": "<p style='color:red'>Private health care / Private Education / First house sale to citizen</p>",
        "gross": 0,
        "adjustment": 0,
        "vat_amount": 0
    })
    
    # get 0% sales vat total
    account_list = get_accounts(filters, 0, "vat zero")
    total_row, return_total_row = get_account_wise_tax_invoice(filters, invoice_name, account_list)
    data.append({
        "sr_no":"3",
        "particulars": "Zero rated domestic sales",
        "invoice_name": invoice_name,
        "account_list": account_list,
        "gross": total_row.get("total_taxable_amount"),
        "adjustment": return_total_row.get("total_taxable_amount"),
        "vat_amount": total_row.get("total_vat_amount") - return_total_row.get("total_vat_amount")
    })
    total_sales_gross += total_row.get("total_taxable_amount")
    total_sales_adjustment += return_total_row.get("total_taxable_amount")
    total_sales_vat_amount += total_row.get("total_vat_amount") - return_total_row.get("total_vat_amount")

    # get sales export vat total
    account_list = get_accounts(filters, None, "vat export")
    total_row, return_total_row = get_account_wise_tax_invoice(filters, invoice_name, account_list)
    data.append({
        "sr_no":"4",
        "particulars": "Exports",
        "invoice_name": invoice_name,
        "account_list": account_list,
        "gross": total_row.get("total_taxable_amount"),
        "adjustment": return_total_row.get("total_taxable_amount"),
        "vat_amount": total_row.get("total_vat_amount") - return_total_row.get("total_vat_amount")
    })
    total_sales_gross += total_row.get("total_taxable_amount")
    total_sales_adjustment += return_total_row.get("total_taxable_amount")
    total_sales_vat_amount += total_row.get("total_vat_amount") - return_total_row.get("total_vat_amount")
    
    # get exempted vat sales total
    account_list = get_accounts(filters, None, "vat exempt")
    total_row, return_total_row = get_account_wise_tax_invoice(filters, invoice_name, account_list)
    data.append({
        "sr_no":"5",
        "particulars": "Exempt sales",
        "invoice_name": invoice_name,
        "account_list": account_list,
        "gross": total_row.get("total_taxable_amount"),
        "adjustment": return_total_row.get("total_taxable_amount"),
        "vat_amount": total_row.get("total_vat_amount") - return_total_row.get("total_vat_amount")
    })
    total_sales_gross += total_row.get("total_taxable_amount")
    total_sales_adjustment += return_total_row.get("total_taxable_amount")
    total_sales_vat_amount += total_row.get("total_vat_amount") - return_total_row.get("total_vat_amount")

    data.append({
        "sr_no":"6",
        "particulars": frappe.bold("Total Sales"),
        "gross": total_sales_gross,
        "adjustment": total_sales_adjustment,
        "vat_amount": total_sales_vat_amount
    })

    data.append({})
    data.append({})

    # Purchase Vat Details
    invoice_name = "purchase"
    total_purchase_gross = 0
    total_purchase_adjustment = 0
    total_purchase_vat_amount = 0
    
    data.append({
        "particulars": frappe.bold("VAT on Purchase:")
    })

    # get 15% purchase vat total
    account_list = get_accounts(filters, 15, 'VAT', ['reverse charge mechanism', 'business expense', 'financial charge'])
    total_row, return_total_row = get_account_wise_tax_invoice(filters, invoice_name, account_list)
    data.append({
        "sr_no":"7",
        "particulars": "Standard rated domestic purchases (15%)",
        "invoice_name": invoice_name,
        "account_list": account_list,
        "gross": total_row.get("total_taxable_amount"),
        "adjustment": return_total_row.get("total_taxable_amount"),
        "vat_amount": total_row.get("total_vat_amount") - return_total_row.get("total_vat_amount")
    })
    total_purchase_gross += total_row.get("total_taxable_amount")
    total_purchase_adjustment += return_total_row.get("total_taxable_amount")
    total_purchase_vat_amount += total_row.get("total_vat_amount") - return_total_row.get("total_vat_amount")

    # get 15% journal financial charges vat total
    account_list = get_accounts(filters, 15, "financial charge")
    total_row, return_total_row = get_account_wise_tax_invoice(filters, invoice_name, account_list)
    data.append({
        "particulars": "VAT on financial Charges (15%)",
        "invoice_name": "financial",
        "account_list": account_list,
        "gross": total_row.get("total_taxable_amount"),
        "adjustment": return_total_row.get("total_taxable_amount"),
        "vat_amount": total_row.get("total_vat_amount") - return_total_row.get("total_vat_amount")
    })
    total_purchase_gross += total_row.get("total_taxable_amount")
    total_purchase_adjustment += return_total_row.get("total_taxable_amount")
    total_purchase_vat_amount += total_row.get("total_vat_amount") - return_total_row.get("total_vat_amount")

    # get 15% journal business expense vat total
    account_list = get_accounts(filters, 15, "business expense")
    total_row, return_total_row = get_account_wise_tax_invoice(filters, invoice_name, account_list)
    data.append({
        "particulars": "VAT on Business Expenses (15%)",
        "invoice_name": "business",
        "account_list": account_list,
        "gross": total_row.get("total_taxable_amount"),
        "adjustment": return_total_row.get("total_taxable_amount"),
        "vat_amount": total_row.get("total_vat_amount") - return_total_row.get("total_vat_amount")
    })
    total_purchase_gross += total_row.get("total_taxable_amount")
    total_purchase_adjustment += return_total_row.get("total_taxable_amount")
    total_purchase_vat_amount += total_row.get("total_vat_amount") - return_total_row.get("total_vat_amount")

    data.append({
        "particulars": "",
        "gross": total_purchase_gross,
        "adjustment": total_purchase_adjustment,
        "vat_amount": total_purchase_vat_amount
    })

    data.append({})

    net_gross = 0
    net_adjustment = 0
    net_vat_amount = 0
    # get 5% purchase vat total
    account_list = get_accounts(filters, 5, 'VAT', ['reverse charge mechanism', 'business expense', 'financial charge'])
    total_row, return_total_row = get_account_wise_tax_invoice(filters, invoice_name, account_list)
    data.append({
        "sr_no":"7.1",
        "particulars": "Purchases subject to VAT at (5%)",
        "invoice_name": invoice_name,
        "account_list": account_list,
        "gross": total_row.get("total_taxable_amount"),
        "adjustment": return_total_row.get("total_taxable_amount"),
        "vat_amount": total_row.get("total_vat_amount") - return_total_row.get("total_vat_amount")
    })
    total_purchase_gross += total_row.get("total_taxable_amount")
    total_purchase_adjustment += return_total_row.get("total_taxable_amount")
    total_purchase_vat_amount += total_row.get("total_vat_amount") - return_total_row.get("total_vat_amount")

    net_gross += total_row.get("total_taxable_amount")
    net_adjustment += return_total_row.get("total_taxable_amount")
    net_vat_amount += total_row.get("total_vat_amount") - return_total_row.get("total_vat_amount")

    # get 5% journal financial charges vat total
    account_list = get_accounts(filters, 5, "financial charge")
    total_row, return_total_row = get_account_wise_tax_invoice(filters, invoice_name, account_list)
    data.append({
        "particulars": "VAT on financial Charges (5%)",
        "invoice_name": "financial",
        "account_list": account_list,
        "gross": total_row.get("total_taxable_amount"),
        "adjustment": return_total_row.get("total_taxable_amount"),
        "vat_amount": total_row.get("total_vat_amount") - return_total_row.get("total_vat_amount")
    })
    total_purchase_gross += total_row.get("total_taxable_amount")
    total_purchase_adjustment += return_total_row.get("total_taxable_amount")
    total_purchase_vat_amount += total_row.get("total_vat_amount") - return_total_row.get("total_vat_amount")

    net_gross += total_row.get("total_taxable_amount")
    net_adjustment += return_total_row.get("total_taxable_amount")
    net_vat_amount += total_row.get("total_vat_amount") - return_total_row.get("total_vat_amount")

    # get 5% journal business expense vat total
    account_list = get_accounts(filters, 5, "business expense")
    total_row, return_total_row = get_account_wise_tax_invoice(filters, invoice_name, account_list)
    data.append({
        "particulars": "VAT on Business Expenses (5%)",
        "invoice_name": "business",
        "account_list": account_list,
        "gross": total_row.get("total_taxable_amount"),
        "adjustment": return_total_row.get("total_taxable_amount"),
        "vat_amount": total_row.get("total_vat_amount") - return_total_row.get("total_vat_amount")
    })
    total_purchase_gross += total_row.get("total_taxable_amount")
    total_purchase_adjustment += return_total_row.get("total_taxable_amount")
    total_purchase_vat_amount += total_row.get("total_vat_amount") - return_total_row.get("total_vat_amount")

    net_gross += total_row.get("total_taxable_amount")
    net_adjustment += return_total_row.get("total_taxable_amount")
    net_vat_amount += total_row.get("total_vat_amount") - return_total_row.get("total_vat_amount")

    data.append({
        "particulars": "",
        "gross": net_gross,
        "adjustment": net_adjustment,
        "vat_amount": net_vat_amount
    })

    data.append({})

    data.append({
        "sr_no":"8",
        "particulars": "<p style='color:red'>Imports subject to VAT paid at customs (15%)</p>",
        "gross": 0,
        "adjustment": 0,
        "vat_amount": 0
    })

    data.append({
        "sr_no":"8.1",
        "particulars": "<p style='color:red'>Imports subject to VAT paid at customs (5%)</p>",
        "gross": 0,
        "adjustment": 0,
        "vat_amount": 0
    })

    # get 15% purchase rcm vat total
    account_list = get_accounts(filters, 15, "Vat Input Tax 15% On Reverse Charge Mechanism")
    total_row, return_total_row = get_account_wise_tax_invoice(filters, invoice_name, account_list)
    data.append({
        "sr_no":"9",
        "particulars": "Imports subject to VAT accounted for through the reverse charge mechanism (15%)",
        "invoice_name": "input rcm",
        "account_list": account_list,
        "gross": total_row.get("total_taxable_amount"),
        "adjustment": return_total_row.get("total_taxable_amount"),
        "vat_amount": 0
    })
    total_purchase_gross += total_row.get("total_taxable_amount")
    total_purchase_adjustment += return_total_row.get("total_taxable_amount")
    # total_purchase_vat_amount += total_row.get("total_vat_amount") + return_total_row.get("total_vat_amount")

    # get 5% purchase rcm vat total
    account_list = get_accounts(filters, 5, "Vat Input Tax 5% On Reverse Charge Mechanism")
    total_row, return_total_row = get_account_wise_tax_invoice(filters, invoice_name, account_list)
    data.append({
        "sr_no":"9.1",
        "particulars": "Imports subject to VAT accounted for through the reverse charge mechanism (5%)",
        "invoice_name": "input rcm",
        "account_list": account_list,
        "gross": total_row.get("total_taxable_amount"),
        "adjustment": return_total_row.get("total_taxable_amount"),
        "vat_amount": 0
    })
    total_purchase_gross += total_row.get("total_taxable_amount")
    total_purchase_adjustment += return_total_row.get("total_taxable_amount")
    # total_purchase_vat_amount += total_row.get("total_vat_amount") + return_total_row.get("total_vat_amount")

    # get 0% purchase vat total
    account_list = get_accounts(filters, 0, "vat", ['vat exempt'])
    total_row, return_total_row = get_account_wise_tax_invoice(filters, invoice_name, account_list)
    data.append({
        "sr_no":"10",
        "particulars": "Zero rated purchases",
        "invoice_name": invoice_name,
        "account_list": account_list,
        "gross": total_row.get("total_taxable_amount"),
        "adjustment": return_total_row.get("total_taxable_amount"),
        "vat_amount": total_row.get("total_vat_amount") - return_total_row.get("total_vat_amount")
    })
    total_purchase_gross += total_row.get("total_taxable_amount")
    total_purchase_adjustment += return_total_row.get("total_taxable_amount")
    total_purchase_vat_amount += total_row.get("total_vat_amount") - return_total_row.get("total_vat_amount")

    # get exempted vat purchase total
    account_list = get_accounts(filters, None, "vat exempt")
    total_row, return_total_row = get_account_wise_tax_invoice(filters, invoice_name, account_list)
    data.append({
        "sr_no":"11",
        "particulars": "Exempt purchases",
        "invoice_name": invoice_name,
        "account_list": account_list,
        "gross": total_row.get("total_taxable_amount"),
        "adjustment": return_total_row.get("total_taxable_amount"),
        "vat_amount": total_row.get("total_vat_amount") - return_total_row.get("total_vat_amount")
    })
    total_purchase_gross += total_row.get("total_taxable_amount")
    total_purchase_adjustment += return_total_row.get("total_taxable_amount")
    total_purchase_vat_amount += total_row.get("total_vat_amount") - return_total_row.get("total_vat_amount")

    data.append({
        "sr_no":"12",
        "particulars": frappe.bold("Total Purchase"),
        "gross": total_purchase_gross,
        "adjustment": total_purchase_adjustment,
        "vat_amount": total_purchase_vat_amount
    })

    data.append({})

    data.append({
        "sr_no":"13",
        "particulars": frappe.bold("Total VAT due for current period"),
        "vat_amount": total_sales_vat_amount - total_purchase_vat_amount
    })
    currency = ""
    if filters.get("company"):
        currency = get_company_currency(filters["company"])

    data.append({
        "sr_no":"14",
        "particulars": "<p style='color:red'>Corrections from previous period ( between {0} ± 5000.00 )</p>".format(currency),
        "vat_amount": 0
    })

    data.append({
        "sr_no":"15",
        "particulars": "<p style='color:red'>VAT credit carried forward from previous period(s)</p>",
        "vat_amount": 0
    })

    data.append({
        "sr_no":"16",
        "particulars": frappe.bold("Net VAT due (or reclaimed)"),
        "vat_amount": total_sales_vat_amount - total_purchase_vat_amount
    })
    return columns, data

def get_account_wise_tax_invoice(filters, invoice_name, account_list):
    # total_row = return_total_row = {"total_taxable_amount": 0, "total_vat_amount": 0}
    invoice_list = []
    return_invoice_list = []

    # get invoice list for gross value
    for account in account_list:
        invoice_list.extend(get_tax_invoice_details(filters, invoice_name, account, 0))
        # get Journal Entry list for gross value if it is Purchase VAT
        if invoice_name == "purchase":
            invoice_list.extend(get_tax_invoice_details(filters, "journal", account, 0))
    total_row = calc_total_amount(invoice_list)

    # get return invoice list for adjustment value
    for account in account_list:
        return_invoice_list.extend(get_tax_invoice_details(filters, invoice_name, account, 1))
        # get return Journal Entry list for adjustment value if it is Purchase VAT
        if invoice_name == "purchase":
            return_invoice_list.extend(get_tax_invoice_details(filters, "journal", account, 1))
    return_total_row = calc_total_amount(return_invoice_list)
    
    return total_row, return_total_row

def calc_total_amount(invoice_list):
    # total invoice list and return total value as per VAT account
    total_taxable_amount = total_vat_amount = 0
    for invoice in invoice_list:
        total_taxable_amount += invoice.get("taxable_amount")
        total_vat_amount += invoice.get("vat_amount")
    return {"total_taxable_amount": total_taxable_amount, "total_vat_amount": total_vat_amount}


def get_columns(filters):
    currency = ""
    if filters.get("company"):
        currency = get_company_currency(filters["company"])
    return [
        {
            "fieldname": "sr_no",
            "label": _("Sr No"),
            "fieldtype": "Data",
            "width": 70
        },
        {
            "fieldname": "particulars",
            "label": _("Particulars"),
            "fieldtype": "Link",
            "options": "Report",
            "width": 450
        },
        {
            "fieldname": "gross",
            "label": _("GROSS Amount ({0})").format(currency),
            "fieldtype": "Currency",
            "width": 200
        },
        {
            "fieldname": "adjustment",
            "label": _("ADJUSTMENT Amount ({0})").format(currency),
            "fieldtype": "Currency",
            "width": 250
        },
        {
            "fieldname": "vat_amount",
            "label": _("VAT Amount ({0})").format(currency),
            "fieldtype": "Currency",
            "width": 200
        }
    ]
