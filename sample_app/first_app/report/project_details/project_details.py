# Copyright (c) 2013, Leader Group and contributors
# For license information, please see license.txt

import frappe
from frappe import _

def execute(filters=None):
    columns, data = [], []
    columns = get_columns()
    del filters["printed_on"]
    project_filters = filters.copy()
    if filters.get("from_date"):
        del project_filters["from_date"]
    if filters.get("to_date"):
        del project_filters["to_date"]

    # Get List of Project as per filters
    project_list = frappe.db.get_all("Project",
        filters=project_filters,
        fields=["name", "project_name", 
                "customer"
            ])
    
    for project in project_list:
        sql_conditions = ""
        total_delivery_amount = 0
        total_invoice_amount = 0
        total_collection_amount = 0
        total_collected_vat = 0
        total_collected_amount = 0
        total_vat_amount = 0
        total_invoice_amount_with_vat = 0
        filters_data = []
        filters_data.append(["project", "=", project.get("name")])
        if filters.get("from_date"):
            filters_data.append(["posting_date", ">=", filters.get("from_date")])
            sql_conditions += " and posting_date >= '" + filters.get("from_date") +"'"
        if filters.get("to_date"):
            filters_data.append(["posting_date", "<=", filters.get("to_date")])
            sql_conditions += " and posting_date <= '" + filters.get("to_date") +"'"
        
        # Get List of Delivery Note as per Project and filters
        delivery_note = frappe.db.get_all("Delivery Note",
            filters=filters_data,
            fields=["name",
                    "customer",
                    "project",
                    "grand_total"
                ],
            order_by="modified")
        
        for delivery in delivery_note:
            sales_inv = ""
            inv_amt = 0
            payment_rec = ""
            collect_amt = 0
            collect_vat = 0
            total_collect_amt = 0
            vat_amt = 0
            inv_amt_with_vat = 0
            
            # Get List of Sales Invoice as per Delivery Note and Sales Invoice and filters
            sales_invoice = """SELECT DISTINCT si.name, 
                                si.total, si.grand_total, si.total_taxes_and_charges
                            FROM `tabSales Invoice Item` sii
                            inner join `tabSales Invoice` si 
                                on si.name = sii.parent 
                            where (sii.delivery_note = "{0}" 
                                or si.name in (select DISTINCT against_sales_invoice
                                    from `tabDelivery Note Item` 
                                    WHERE against_sales_invoice is not null
                                        and parent = "{0}"))
                            {1} ; """.format(delivery.get("name"),sql_conditions)
            sales_invoice = frappe.db.sql(sales_invoice, as_dict=1)
            if sales_invoice:
                for sales in sales_invoice:
                    sales_inv += sales.get("name")
                    inv_amt += sales.get("total")
                    vat_amt += sales.get("total_taxes_and_charges")
                    inv_amt_with_vat += sales.get("grand_total")
                    
                    # Get List of Payment Receipt as per Sales Invoice and filters
                    payment_receipt = """select pe.name, per.allocated_amount, pe.total_taxes_and_charges
                                        FROM `tabPayment Entry Reference` per
                                    inner join `tabPayment Entry` pe
                                        on pe.name = per.parent
                                    where per.reference_doctype ='Sales Invoice'
                                        and per.reference_name = "{0}" {1}; """.format(sales.get("name"),sql_conditions)
                    payment_receipt = frappe.db.sql(payment_receipt, as_dict=1)
                    if payment_receipt:
                        for payment in payment_receipt:
                            payment_rec += payment.get("name")
                            collect_amt += payment.get("allocated_amount")
                            collect_vat += payment.get("total_taxes_and_charges")
                            total_collect_amt += payment.get("allocated_amount") + payment.get("total_taxes_and_charges")
            delivery["project_name"] = project.get("project_name")                
            delivery["sales_invoice"] = sales_inv
            delivery["invoice_amount"] = inv_amt
            delivery["payment_receipt"] = payment_rec
            delivery["vat_amount"] = vat_amt
            delivery["invoice_amt_with_vat"] = inv_amt_with_vat
            # delivery["payment_receipt"] = payment_rec
            # delivery["collection_amount"] = collect_amt
            # delivery["collected_vat"] = collect_vat
            delivery["total_collected_amount"] = total_collect_amt
            delivery["remaining_amount"] = inv_amt_with_vat - total_collect_amt

            #sub-Total
            total_delivery_amount += delivery.get("grand_total")
            total_invoice_amount += inv_amt
            total_vat_amount += vat_amt
            total_invoice_amount_with_vat += inv_amt_with_vat
            total_collection_amount += collect_amt
            total_collected_vat += collect_vat
            total_collected_amount += total_collect_amt
        data.extend(delivery_note)
        if delivery_note:
            data.append({"project":"<b>Sub Total for "+project.get("project_name")+"</b>",
                "grand_total": total_delivery_amount,
                "invoice_amount": total_invoice_amount,
                "collection_amount": total_collection_amount,
                "collected_vat": total_collected_vat,
                "total_collected_amount": total_collected_amount,
                "vat_amount": total_vat_amount,
                "invoice_amt_with_vat": total_invoice_amount_with_vat,
                "remaining_amount": total_invoice_amount_with_vat - total_collection_amount
                })
    return columns, data

def get_columns():
    return [
        {
            "fieldname": "customer",
            "label": _("Customer Name"),
            "fieldtype": "Link",
            "options": "Customer",
            "width": 200
        },
        {
            "fieldname": "project",
            "label": _("Project"),
            "fieldtype": "Link",
            "options": "Project",
            "width": 200
        },
        {
            "fieldname": "name",
            "label": _("Delivery Note #"),
            "fieldtype": "Link",
            "options": "Delivery Note",
            "width": 200
        },
        {
            "fieldname": "sales_invoice",
            "label": _("Sales Invoice #"),
            "fieldtype": "Link",
            "options": "Sales Invoice",
            "width": 200
        },
        {
            "fieldname": "payment_receipt",
            "label": _("Payment Receipt #"),
            "fieldtype": "Link",
            "options": "Payment Entry",
            "width": 200
        },
        # {
        #     "fieldname": "grand_total",
        #     "label": _("Delivered Amount"),
        #     "fieldtype": "Float",
        #     "width": 200
        # },
        {
            "fieldname": "invoice_amount",
            "label": _("Invoice Amount"),
            "fieldtype": "Float",
            "width": 200
        },
        {
            "fieldname": "vat_amount",
            "label": _("VAT Amount"),
            "fieldtype": "Float",
            "width": 200
        },
        {
            "fieldname": "invoice_amt_with_vat",
            "label": _("Invoice Amount with VAT"),
            "fieldtype": "Float",
            "width": 200
        },
        #{
        #     "fieldname": "collection_amount",
        #     "label": _("Collection Amount (w/o VAT)"),
        #     "fieldtype": "Float",
        #     "width": 200
        # },
        # {
        #     "fieldname": "collected_vat",
        #     "label": _("Collected VAT"),
        #     "fieldtype": "Float",
        #     "width": 200
        # },
        {
            "fieldname": "total_collected_amount",
            "label": _("Total Collected Amount"),
            "fieldtype": "Float",
            "width": 200
        },
        {
            "fieldname": "remaining_amount",
            "label": _("Remaining Amount"),
            "fieldtype": "Float",
            "width": 200
        }
    ]