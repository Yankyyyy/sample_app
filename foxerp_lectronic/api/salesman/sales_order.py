from locale import currency
import frappe
import json
from foxerp_lectronic.utils import createAPIErrorLog
from frappe.contacts.doctype.address.address import get_address_display
from erpnext.controllers.accounts_controller import get_taxes_and_charges
from frappe.utils import cint, flt, round_based_on_smallest_currency_fraction


@frappe.whitelist()
def createSalesOrder(data):
    """To create new Sales Order.User should be sales person"""
    try:
        if get_sales_person_by_user():
            so = frappe.new_doc("Sales Order")
            so.customer = data.get("customer")
            so.delivery_date = data.get("delivery_date") #delievry date
            so.territory = data.get("territory")
            so.company =  frappe.db.get_single_value('Global Defaults', 'default_company')
            so.customer_address = data.get("billing_address") 
            so.shipping_address_name = data.get("shipping_address")
            
            so.order_type = "Sales" 
            so.currency= frappe.db.get_single_value('Global Defaults', 'default_currency')
            so.selling_price_list= frappe.db.get_single_value('Selling Settings', 'selling_price_list')
            so.set('sales_team', [])
            so_sales_team = so.append('sales_team', {})
            so_sales_team.sales_person = get_sales_person_by_user()
            so_sales_team.allocated_percentage = 100

            so.set('items', [])
            for item in data.get('items'):
                soi = so.append('items', {})
                soi.item_code = item.get("item_code")
                soi.qty = item.get("qty")
                soi.price_list_rate = flt(item.get("price_list_rate")) #Rate before discount
                soi.discount_percentage = item.get("discount_percentage")
          
            so.taxes_and_charges = data.get("taxes_and_charges")
            so.set_taxes()
            so.save(ignore_permissions=True)
            frappe.db.commit()
            return so.name
        else:
            return "Logged In User must be a Sales Person"
  
    except Exception:
        error = frappe.get_traceback()
        createAPIErrorLog(error)
        return error

@frappe.whitelist()
def updateSalesOrder(data,sales_order_id):
    """Update Item Details in Sales Order"""
    try:
        so = frappe.get_doc("Sales Order",sales_order_id)
        if so.docstatus == 0 : #only draft mode orders will be updated
            so.set('items', [])
            for item in data.get('items'):
                soi = so.append('items', {})
                soi.item_code = item.get("item_code")
                soi.qty = item.get("qty")
                soi.price_list_rate = flt(item.get("price_list_rate")) #Rate before discount
                soi.discount_percentage = item.get("discount_percentage")
            so.save(ignore_permissions=True)
            frappe.db.commit()
            return so.name
        else :
            raise Exception("Only Draft mode Orders will be updated")
            
    except Exception:
        error = frappe.get_traceback()
        createAPIErrorLog(error)
        return error

@frappe.whitelist()
def getTaxesAndTotals(data):
    """Get the calculated Taxes and Totals"""
    try:
        so = frappe.new_doc("Sales Order")
        so.ignore_pricing_rule = 0
        so.customer = data.get("customer")
        company = frappe.db.get_single_value('Global Defaults', 'default_company')
        so.company = company
        so.order_type = "Sales"
        so.currency= frappe.db.get_single_value('Global Defaults', 'default_currency')
        so.selling_price_list= frappe.db.get_single_value('Selling Settings', 'selling_price_list')
        so.set('items', [])
        for item in data.get('items'):
            soi = so.append('items', {})
            soi.item_code = item.get("item_code")
            soi.qty = item.get("qty")
            soi.price_list_rate = flt(item.get("price_list_rate")) #Rate before discount
            soi.discount_percentage = item.get("discount_percentage")
        
        default_tax = frappe.db.get_value('Sales Taxes and Charges Template', {"is_default": 1, "company": company})
        tax_percentage = ""
        if default_tax: 
            so.taxes_and_charges = default_tax
            taxes = get_taxes_and_charges('Sales Taxes and Charges Template', default_tax)
            if round(taxes[0]["rate"],0) == taxes[0]["rate"] :
                tax_percentage = str( round(taxes[0]["rate"]) ) + "%"
            else:
                tax_percentage = str(taxes[0]["rate"]) + "%"
            for tax in taxes:
                so.append('taxes', tax)
       
        so.set_taxes() 
        so.calculate_taxes_and_totals()
        
        items_total_discount = 0
        items_total_price_list_rate = 0
        #Items total Discount
        for item in so.get('items'):
            items_total_discount += item.get("discount_amount") * item.get("qty")
            items_total_price_list_rate += item.get("base_price_list_rate") * item.get("qty")

        #Items totals
        total_details_dic ={}
        total_details_dic["discount"] =  round(items_total_discount,2) 
        total_details_dic["total_base_amount"] = round(items_total_price_list_rate,2)  
        total_details_dic["tax_amount"] =round( so.get("total_taxes_and_charges"),2 )  
        total_details_dic["taxable_amount"] = round( so.get("net_total") ,2)  
        total_details_dic["grand_total"] = round( so.get("grand_total") ,2)  
        total_details_dic["total_qty"] = so.get("total_qty")  
        total_details_dic["taxes_and_charges"] = so.get("taxes_and_charges") if default_tax else ""
        total_details_dic["tax_percentage"] = tax_percentage 
        total_details_dic["rounding_adjustment"] = so.get("rounding_adjustment") 
        total_details_dic["rounded_total"] = round( so.get("rounded_total"),2 )  
        return total_details_dic
    except Exception:
        error = frappe.get_traceback()
        createAPIErrorLog(error)
        return error

@frappe.whitelist()
def getSalesOrderList(data):
    # Get sales order list as per Account manager/Owner and applied filters
    try:
        tab = ""
        sql_conditions = "1=1"
        sql_data_order_id = []
        under_execution_data = []
        
        #set filters
        if data.get("territory"):
            sql_conditions += " and so.territory like '" + f'%{data.get("territory")}%' +"'"
        if data.get("city"):
            sql_conditions += " and c.city like '" + f'%{data.get("city")}%' +"'"
            tab += "join `tabCustomer` c on so.customer = c.name "
            if data.get("shop_name"):
                sql_conditions += " and c.shop_name like '" + f'%{data.get("shop_name")}%' +"'"
        if not data.get("city"):
            if data.get("shop_name"):
                sql_conditions += " and c.shop_name like '" + f'%{data.get("shop_name")}%' +"'"
                tab += "join `tabCustomer` c on so.customer = c.name "
        if data.get("transaction_date"):
            sql_conditions += " and so.transaction_date = '" + data.get("transaction_date") +"'"
        if data.get("sales_person"):
            sql_conditions += " and st.sales_person like '" + f'%{data.get("sales_person")}%' +"'"
            tab += "join `tabSales Team` st on so.name = st.parent "
        if not "Sales Manager" in frappe.get_roles(frappe.session.user):
            sql_conditions += " and so.owner = '" +frappe.session.user+"'"
            
        #get sales order list according to the filters applied    
        sql_data = frappe.db.sql("""SELECT 
                                so.customer as customer_id, so.customer_name,COALESCE(so.customer_name_in_arabic,'') as customer_name_in_arabic, so.name as order_id,
                                so.transaction_date as order_date, 
                                so.status as order_status, so.grand_total as order_amount
                                FROM 
                                `tabSales Order` so {0}
                                WHERE
                                {2};
                                """.format(tab, frappe.session.user, sql_conditions), as_dict=1)
        
        #under execution list the sales orders that has been filtered out
        if data.get("under_execution") == 1:
            cond = "1=1"
            if not "Sales Manager" in frappe.get_roles(frappe.session.user):
                cond += " and so.owner = '" +frappe.session.user+"'"
            complete_data = frappe.db.sql("""SELECT 
                                so.customer as customer_id,so.customer_name,COALESCE(so.customer_name_in_arabic,'') as customer_name_in_arabic ,so.name as order_id,
                                so.transaction_date as order_date, 
                                so.status as order_status, so.grand_total as order_amount
                                FROM 
                                `tabSales Order` so
                                WHERE {2};
                                """.format(cond), as_dict=1)

            for j in range(0,len(sql_data)):
                #create a list of order id included in the sql_data
                sql_data_order_id.append(sql_data[j].get("order_id"))
            for k in range(0,len(complete_data)):
                if complete_data[k].get("order_id") not in sql_data_order_id:
                    #the sales orders which is not in the sql_data are added in a new variable
                    under_execution_data.append(complete_data[k])
            return under_execution_data
        else:
            return sql_data
    except Exception:
        error = frappe.get_traceback()
        createAPIErrorLog(error)
        return error

@frappe.whitelist()
def getSalesOrderDetails(sales_order_id):
    # Get sales order details of a particular sales order
    try:
        details = {}
        discount = 0
        amount = 0
        items = []
        
        #get all the sales order details
        sql_data = frappe.db.sql("""SELECT DISTINCT 
                                so.owner, so.customer_name,COALESCE(so.customer_name_in_arabic,'') as customer_name_in_arabic , so.name, so.transaction_date, 
                                so.customer_address, so.shipping_address_name, 
                                so.total,so.net_total, so.discount_amount, so.total_taxes_and_charges, st.rate,
                                so.rounded_total, so.per_delivered,soi.item_code, soi.item_name, soi.qty,soi.image,
                                soi.base_price_list_rate, soi.discount_percentage,
                                soi.discount_amount, soi.amount, soi.delivered_qty,
                                c.territory, c.city, so.company, c.commercial_record_number,
                                c.payment_method, c.mobile_no, si.name as invoice_name, si.status
                                FROM 
                                `tabSales Order` so 
                                join `tabCustomer` c on so.customer = c.name 
                                join `tabSales Order Item` soi on so.name = soi.parent
                                join `tabSales Invoice Item` sii on so.name = sii.sales_order
                                join `tabSales Invoice` si on sii.parent = si.name 
                                join `tabSales Taxes and Charges` st on so.name = st.parent
                                WHERE
                                so.name = "{0}" ;""".format(sales_order_id), as_dict=1)
        
        if sql_data:
            #assign the values to their corresponding keys in a new dictionary variable
            details["full_name"] = frappe.db.get_value("User", sql_data[0].get("owner"), "full_name")
            details["customer_name"] =sql_data[0].get("customer_name")
            details["customer_name_in_arabic"] =sql_data[0].get("customer_name_in_arabic")
            details["territory"] = sql_data[0].get("territory")
            details["city"] = sql_data[0].get("city")
            details["company"] = sql_data[0].get("company")
            details["commercial_record_number"] = sql_data[0].get("commercial_record_number")
            details["mobile_no"] = sql_data[0].get("mobile_no")
            details["payment_method"] = sql_data[0].get("payment_method")
            details["sales_invoice"] = sql_data[0].get("invoice_name")
            details["order_id"] = sql_data[0].get("name")
            details["order_date"] = sql_data[0].get("transaction_date")
            details["payment_status"] = sql_data[0].get("status")
            details["billing_address"] = get_address_display(sql_data[0].get("customer_address"))
            details["shipping_address"] = get_address_display(sql_data[0].get("shipping_address_name"))
            details["billing_address_in_arabic"] = frappe.get_value("Address", sql_data[0].get("customer_address"), 'address_in_arabic')  or ""
            details["shipping_address_in_arabic"] = frappe.get_value("Address", sql_data[0].get("shipping_address_name"), 'address_in_arabic')  or ""


            #item details are made into a dictionary and put it into a list
            for item in sql_data:
                item_dict = {}
                item_dict["item_name"] = item.get("item_name")
                item_dict["item_code"] = item.get("item_code")
                item_dict["qty"] = item.get("qty")
                item_dict["price_list_rate"] = round(item.get("base_price_list_rate"),2)  
                item_dict["discount_percentage"] = item.get("discount_percentage")
                item_dict["discount_amount"] = round(item.get("discount_amount") * item.get("qty"),2)  
                discount += item.get("discount_amount") * item.get("qty")
                item_dict["amount_before_discount"] = round(item.get("base_price_list_rate") * item.get("qty"),2)  
                amount += item.get("base_price_list_rate") * item.get("qty")
                item_dict["total_amount"] = round(item.get("amount"),2)  
                item_dict["delivered_qty"] = item.get("delivered_qty")
                item_dict["image"] = frappe.utils.get_url() + item.get('image') if item.get('image') else ""
                items.append(item_dict)
            details["items"] = items
            details["total_base_price"] = round(amount,2)  
            details["discount"] = round(discount,2)  
            details["total_price"] = round(amount - discount,2)  
            details["tax_percentage"] = sql_data[0].get("rate")
            details["tax"] = round(sql_data[0].get("total_taxes_and_charges"),2)  
            details["taxable_amount"] = round(sql_data[0].get("net_total"),2)  
            details["net_bill"] = round(amount - discount + sql_data[0].get("total_taxes_and_charges"),2)  
            return details
        else:
            sql_data = frappe.db.sql("""SELECT DISTINCT 
                                so.owner, so.customer_name,COALESCE(so.customer_name_in_arabic,'') as customer_name_in_arabic , so.name, so.transaction_date, 
                                so.customer_address, so.shipping_address_name, 
                                so.total,so.net_total ,so.total_taxes_and_charges, st.rate,
                                so.per_delivered, soi.item_name,soi.item_code, soi.qty,soi.image,
                                soi.base_price_list_rate, soi.discount_percentage,
                                soi.discount_amount, soi.amount, soi.delivered_qty,
                                c.territory, c.city, so.company, c.commercial_record_number,
                                c.payment_method, c.mobile_no
                                FROM 
                                `tabSales Order` so 
                                join `tabCustomer` c on so.customer = c.name 
                                join `tabSales Order Item` soi on so.name = soi.parent
                                join `tabSales Taxes and Charges` st on so.name = st.parent
                                WHERE
                                so.name = "{0}" ;""".format(sales_order_id), as_dict=1)
            if sql_data:
                #assign the values to their corresponding keys in a new dictionary variable
                details["full_name"] = frappe.db.get_value("User", sql_data[0].get("owner"), "full_name")
                details["customer_name"] =sql_data[0].get("customer_name")
                details["customer_name_in_arabic"] =sql_data[0].get("customer_name_in_arabic") or ""
                details["territory"] = sql_data[0].get("territory")
                details["city"] = sql_data[0].get("city")
                details["company"] = sql_data[0].get("company")
                details["commercial_record_number"] = sql_data[0].get("commercial_record_number")
                details["mobile_no"] = sql_data[0].get("mobile_no")
                details["payment_method"] = sql_data[0].get("payment_method")
                details["sales_invoice"] = ""
                details["order_id"] = sql_data[0].get("name")
                details["order_date"] = sql_data[0].get("transaction_date")
                details["billing_address"] = get_address_display(sql_data[0].get("customer_address"))
                details["shipping_address"] = get_address_display(sql_data[0].get("shipping_address_name"))
                details["billing_address_in_arabic"] = frappe.get_value("Address", sql_data[0].get("customer_address"), 'address_in_arabic')  or ""
                details["shipping_address_in_arabic"] = frappe.get_value("Address", sql_data[0].get("shipping_address_name"), 'address_in_arabic')  or ""
                #item details are made into a dictionary and put it into a list
                for item in sql_data:
                    item_dict = {}
                    item_dict["item_name"] = item.get("item_name")
                    item_dict["item_code"] = item.get("item_code")
                    item_dict["qty"] = item.get("qty")
                    item_dict["price_list_rate"] = round(item.get("base_price_list_rate"),2)  
                    item_dict["discount_percentage"] = item.get("discount_percentage")
                    item_dict["discount_amount"] = round(item.get("discount_amount") * item.get("qty"),2)  
                    discount += item.get("discount_amount") * item.get("qty")
                    item_dict["amount_before_discount"] = round(item.get("base_price_list_rate") * item.get("qty"),2)  
                    amount += item.get("base_price_list_rate") * item.get("qty")
                    item_dict["total_amount"] = round(item.get("amount"),2)  
                    item_dict["delivered_qty"] = item.get("delivered_qty")
                    item_dict["image"] = frappe.utils.get_url() + item.get('image') if item.get('image') else ""
                    items.append(item_dict)
                details["items"] = items
                details["total_base_price"] = round(amount,2)  
                details["discount"] = round(discount,2)  
                details["total_price"] = round(amount - discount,2)  
                details["tax_percentage"] = sql_data[0].get("rate")
                details["tax"] = round(sql_data[0].get("total_taxes_and_charges"),2)  
                details["taxable_amount"] = round(sql_data[0].get("net_total"),2)  
                details["net_bill"] = round(amount - discount + sql_data[0].get("total_taxes_and_charges"),2)  
                return details
            else:
                return "Sales Order not available"
    except Exception:
        error = frappe.get_traceback()
        createAPIErrorLog(error)
        return error
    
@frappe.whitelist()
def getDeliveryData(sales_order_id):
    # Get delivery details of a particular sales order
    try:
        details = {}
        items = []
        
        #get all the delivery details
        sql_data = frappe.db.sql("""SELECT DISTINCT 
                                so.name, so.transaction_date, c.mobile_no, 
                                so.per_delivered, soi.item_name, soi.base_price_list_rate, 
                                soi.qty, soi.delivered_qty, c.payment_method,
                                si.name as invoice_name, si.status
                                FROM 
                                `tabSales Order` so 
                                join `tabCustomer` c on so.customer = c.name 
                                join `tabSales Order Item` soi on so.name = soi.parent
                                join `tabSales Invoice Item` sii on so.name = sii.sales_order
                                join `tabSales Invoice` si on sii.parent = si.name 
                                WHERE
                                so.name = "{0}" ;""".format(sales_order_id), as_dict=1)
        
        #check if delivery information is available or not
        if sql_data[0].get("per_delivered") > 0:
            #assign the values to their corresponding keys in a new dictionary variable
            details["order_id"] = sql_data[0].get("name")
            details["order_date"] = sql_data[0].get("transaction_date")
            details["payment_method"] = sql_data[0].get("payment_method")
            details["sales_invoice"] = sql_data[0].get("invoice_name")
            details["payment_status"] = sql_data[0].get("status")
            details["mobile_no"] = sql_data[0].get("mobile_no")
            #item details are made into a list
            for item in sql_data:
                item_dict = {}
                item_dict["item_name"] = item.get("item_name")
                item_dict["qty"] = item.get("qty")
                item_dict["price_list_rate"] = round(item.get("base_price_list_rate"),2)  
                item_dict["delivered_qty"] = item.get("delivered_qty")
                items.append(item_dict)
            details["items"] = items
            return details
        else:
            return "No delivery information available"
    except Exception:
        error = frappe.get_traceback()
        createAPIErrorLog(error)
        return error

def get_sales_person_by_user():
    return frappe.db.get_value("Sales Person", {"employee":frappe.db.get_value("Employee", {"user_id":frappe.session.user})})