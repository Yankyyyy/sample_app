import frappe

@frappe.whitelist()
def getBank():
    """Return a list of all Bank"""
    return frappe.db.get_list('Bank', pluck='name')

@frappe.whitelist()
def getCountry():
    """Return a list of all Country"""
    return frappe.db.get_list('Country', pluck='name')

@frappe.whitelist()
def getSalesTaxTemplate():
    """Return a list of Sales Tax Template"""
    sales_tax_template = """ select ST.account_head as 'title',
            ST.rate, ST.tax_amount as 'amount'
        from `tabSales Taxes and Charges` ST
        inner join `tabSales Taxes and Charges Template` STT
            on STT.name = ST.parent
        where STT.disabled = 0 ;"""
    return frappe.db.sql(sales_tax_template, as_dict=1)