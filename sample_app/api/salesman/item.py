import frappe
import json
from foxerp_lectronic.utils import createAPIErrorLog
from erpnext.stock.dashboard.item_dashboard import get_data
from erpnext.stock.get_item_details import get_price_list_rate_for
from frappe.utils import nowdate

@frappe.whitelist()
def getProductList():
    # Get Item List using API
    try:
        item_filters = []
        current_stock = 0
        price_list = ""
        args = {
            "transaction_date": nowdate(),
            "qty": 1
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
                price_list = frappe.db.get_value("Customer", data.get("customer"), ["default_price_list"])

        args['price_list'] = price_list
        item_filters.append(['disabled', '=', 0])

        # Get Item List as per filters
        items = frappe.db.get_list('Item',
            filters = item_filters,
            fields = ['item_code', 'item_name', 'item_group', 'image', 'stock_uom']
        )

        for item in items:
            args['uom'] = item.get('stock_uom')
            # Get Item Selling Price
            price = get_price_list_rate_for(args, item.item_code)
            if not price:
                price = 0
            
            # Get Item Current available Stock
            avl_stock = get_data(item_code = item.item_code)
            for stock in avl_stock:
                current_stock += stock.get('actual_qty')
            # If Current available stock is negative we consider as zero
            if current_stock < 0:
                current_stock = 0
            
            if item.get('image'):
                item["image"] = frappe.utils.get_url() + item["image"]
            
            item["current_stock"] = current_stock
            item["price"] = price
        return items
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
