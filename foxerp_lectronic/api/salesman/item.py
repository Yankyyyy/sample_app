import frappe
import json
from foxerp_lectronic.utils import createAPIErrorLog
from erpnext.stock.get_item_details import get_item_details
from frappe.utils import flt, nowdate

@frappe.whitelist()
def getProductList():
    # Get Item List using API
    try:
        item_filters = []
        current_stock = 0
        price_list = ""
       
        #get item details api debug
        args = {
            'doctype': "Sales Order",
            'transaction_date':nowdate(),
            'company': frappe.db.get_single_value('Global Defaults', 'default_company'),
            'plc_conversion_rate': 1.0,
            'conversion_rate': 1.0,
            'ignore_pricing_rule':0
        }
        
        # Get Default Price list from selling settings page
        if frappe.db.get_single_value("Selling Settings", "selling_price_list"):
            price_list = frappe.db.get_single_value("Selling Settings", "selling_price_list")
        
        if frappe.request.data:
            data = json.loads(frappe.request.data)
            if data.get('item_code'):
                item_filters.append(['item_code', 'like', '%{}%'.format(data.get('item_code'))])

            if data.get('item_name'):
                item_filters.append(['item_name', 'like', '%{}%'.format(data.get('item_name'))])

            if data.get('item_group'):
                item_filters.append(['item_group', 'like', '%{}%'.format(data.get('item_group'))])

            if data.get('customer'):
                args['customer'] = data.get('customer')
                # Get Default Price List from Customer Master
                if frappe.db.get_value("Customer", data.get("customer"), ["default_price_list"]):
                    price_list = frappe.db.get_value("Customer", data.get("customer"), ["default_price_list"])
            else:
                return "Customer is Mandatory"

        args['selling_price_list'] = price_list
        args['price_list_currency'] = frappe.db.get_value("Price List", price_list, ["currency"])

        item_filters.append(['disabled', '=', 0])
        item_filters.append(['has_variants', '=', 0])

        # Get Item List as per filters
        items = frappe.db.get_list('Item',
            filters = item_filters,
            fields = ['item_code', 'item_name', 'item_group', 'image', 'stock_uom']
        )
        item_list = []
        for item in items:
            #args['uom'] = item.get('stock_uom')
            args['item_code'] = item.get('item_code')

            item_details = get_item_details(args)  #customer is mandatory filter
            price = item_details.get("price_list_rate")
            if not price:
                continue
            else:
                item["discount_percentage"] = item_details.get("discount_percentage")
                item["discount_amount"] = round(flt(item_details.get("price_list_rate")) *  (item["discount_percentage"]/100) ,2)
                item["price_after_discount"] =round( price - flt(item_details.get("price_list_rate")) *  (item["discount_percentage"]/100),2)#discount_amount,price_after_discount will only be returned if item has price_list_rate
            
                # Get Item Current available Stock
                current_stock = get_stock_qty(item.item_code)
                # If Current available stock is negative we consider as zero
                if current_stock < 0:
                    current_stock = 0
                
                if item.get('image'):
                    item["image"] = frappe.utils.get_url() + item["image"]
                
                item["current_stock"] = current_stock
                item["price"] = round( price,2 ) 
                item_list.append(item)
        
        return item_list
    except Exception:
        error = frappe.get_traceback()
        createAPIErrorLog(error)
        return error

@frappe.whitelist()
def getProductGroupList():
    # Get Item Group List using API
    try:
        item_group = frappe.db.get_list('Item Group',
            filters = {"is_group": 0},
            fields = ['name']
        )
        return item_group
    except Exception:
        error = frappe.get_traceback()
        createAPIErrorLog(error)
        return error

def get_stock_qty(item_code):
	"""
		Return actual qty of item from Stock Ledger
		flt from frappe.utils handles None value by changing it into float (0)
	"""
	cond = "item_code = '%s'"% item_code
	cond += " and docstatus = 1"
	return flt(frappe.db.sql("""
			select sum(actual_qty) from `tabStock Ledger Entry`
			where %s"""%(cond))[0][0])