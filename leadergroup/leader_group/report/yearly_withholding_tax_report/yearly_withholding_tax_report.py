# Copyright (c) 2022, Leader Group and contributors
# For license information, please see license.txt
import frappe
from itertools import groupby
from leadergroup.leader_group.report.monthly_withholding_tax_report.monthly_withholding_tax_report import get_withholding_tax_data

def execute(filters=None):
	columns, data = [], []
	columns = set_columns()
	invoice_list = get_withholding_tax_data(filters)
	#grouping the supplier based on taxrate and withholdingtaxcategory
	for key, group in groupby(invoice_list, key=lambda x: (x['supplier'],x['type_payment'],x['tax_rate'] )):
		total_net = 0
		total_withhold = 0
		for grp in group:
			total_net += grp.net_amount
			total_withhold += grp.withhold
			supplier_grp = grp.supplier
			total_tax = grp.tax_rate
			category_grp = grp.type_payment
			country_grp = grp.country
		data.append(
			{
				'name':supplier_grp,
				'country':country_grp,
				'type_category':category_grp,
				'net_amount':total_net,
				'tax_rate': total_tax,
				'withhold_amt':total_withhold,
				'begin_amt': 0 ,
				'fine_amt': 0 ,
				'other_amt':0,
				'blnc_amt':0
			}
		)
	return columns,data
		
def set_columns():
    the_columns = [
		{
			"label": ("Company name"),
			"fieldname": "name",
			"fieldtype": "Link",
			"options":"Supplier",
			"width": "180"
		},
		{
			"label": ("Country"),
			"fieldname": "country",
			"fieldtype": "Data",
			"width": "180"
		},
		{
			"label": ("Type of Service"),
			"fieldname": "type_category",
			"fieldtype": "Data",
			"width": "200"
		},
		{
			"label": ("Beginning of period Balance"),
			"fieldname": "begin_amt",
			"fieldtype": "Currency",
			"width": "200"
		},
		{
			"label": ("Services Performed During the year"),
			"fieldname": "net_amount",
			"fieldtype": "Currency",
			"width": "200"
		},
			{
			"label": ("Paid during the year"),
			"fieldname": "net_amount",
			"fieldtype": "Currency",
			"width": "150"
		},
		{
			"label": ("Other Settlements"),
			"fieldname": "other_amt",
			"fieldtype": "Currency",
			"width": "200"
		},
		{
			"label": ("End of period balance"),
			"fieldname": "blnc_amt",
			"fieldtype": "Currency",
			"width": "200"
		},
		{
			"label": ("Payment Amount"),
			"fieldname": "net_amount",
			"fieldtype": "Currency",
			"width": "200"
		},
		{
			"label": ("Tax Rate"),
			"fieldname": "tax_rate",
			"fieldtype": "Float",
			"width": "200"
		},
		{
			"label": ("Withholding Tax Amount"),
			"fieldname": "withhold_amt",
			"fieldtype": "Currency",
			"width": "200"
			
		},
		{
			"label": ("Fine"),
			"fieldname": "fine_amt",
			"fieldtype": "Currency",
			"width": "200"
			
		}
	]
    return the_columns
