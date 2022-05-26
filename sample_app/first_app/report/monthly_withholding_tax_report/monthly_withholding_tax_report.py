# Copyright (c) 2022, Leader Group and contributors
# For license information, please see license.txt

import frappe

def execute(filters=None):
	columns, data = [], []
	columns = set_columns()
	data = get_withholding_tax_data(filters)
	return columns,data

def get_withholding_tax_data(filters):
    # get list of Purchase Invoice with Withholding tax Amount which is submitted
	data =  frappe.db.get_list('Purchase Invoice',
		filters = {
			'apply_tds': 1,
			'posting_date': ['between',(filters.get("from_date"),filters.get("to_date"))],
			'company': filters.get("company"),
			'docstatus':1
		},
		fields = ['name', 'posting_date', 'supplier','tax_withholding_category','base_net_total'],
		order_by='posting_date desc'
	)

	# for loop of purchase invoice list
	for each_data in data:
		each_data["type_payment"] = frappe.db.get_value('Tax Withholding Category',each_data.get("tax_withholding_category"),'category_name')
		each_data["country"] = frappe.db.get_value('Supplier',each_data.get('supplier'),'country')
	
		# get Account list added in Tax Withholding Account Master
		account = frappe.db.get_list('Tax Withholding Account',
			filters ={
				'company': filters.get("company"),
				'parent' : each_data.get("tax_withholding_category"),
				'parenttype': 'Tax Withholding Category'
			},
			fields = ['account']
		)
		
		each_data["withhold"] = 0
		# for loop of Withholding tax account list
		for each_account in account:
			# get withholding tax Amount from purchase invoice tax table
			purchase_tax = frappe.db.get_list('Purchase Taxes and Charges',
				filters ={
					'account_head' : each_account.get("account"),
					'parent': each_data.get("name"),
					'parenttype':'Purchase Invoice'
				},
				fields = ['base_tax_amount_after_discount_amount']
			)
			for tax in purchase_tax:
				each_data["withhold"] = tax.get("base_tax_amount_after_discount_amount")
		
		each_data["tax_rate"] = (each_data["withhold"]*100)/each_data["base_net_total"]
		each_data["net_amount"] = each_data["base_net_total"] - each_data["withhold"]
	return data
    

def set_columns():
	the_columns = [
		{
			"label": ("Supplier"),
			"fieldname": "supplier",
			"fieldtype": "Link",
			"options":"Supplier",
			"width": "180"
		},
		{
			"label": ("Type of Payment"),
			"fieldname": "type_payment",
			"fieldtype": "Data",
			"width": "180"
		},
		{
			"label": ("Payment Date"),
			"fieldname": "posting_date",
			"fieldtype": "Date",
			"width": "200"
		},
		{
			"label": ("Country"),
			"fieldname": "country",
			"fieldtype": "Data",
			"width": "200"
		},
		{
			"label": ("Equivalent SAR"),
			"fieldname": "base_net_total",
			"fieldtype": "Currency",
			"width": "200"
		},
			{
			"label": ("Tax Rate"),
			"fieldname": "tax_rate",
			"fieldtype": "Float",
			"width": "150"
		},
		{
			"label": ("WHT Amount"),
			"fieldname": "withhold",
			"fieldtype": "Currency",
			"width": "200"
		},
		{
			"label": ("Net Transfer Amount"),
			"fieldname": "net_amount",
			"fieldtype": "Currency",
			"width": "200"
		},
		{
			"label": ("Voucher No"),
			"fieldname": "name",
			"fieldtype": "Link",
			"options": "Purchase Invoice",
			"width": "200"
		},
		{
			"label": ("Remarks "),
			"fieldname": "remarks",
			"fieldtype": "Data",
			"width": "200"
		}
	]
	return the_columns