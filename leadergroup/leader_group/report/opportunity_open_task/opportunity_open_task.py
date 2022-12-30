# Copyright (c) 2022, Leader Group and contributors
# For license information, please see license.txt

import frappe
from frappe import _

def execute(filters=None):
    columns = get_columns()
    data = []
    row_data = []

    row_data = frappe.db.get_all("Opportunity",
            filters=filters,
            fields=["name","converted_by","status"],
            group_by = "converted_by", order_by = 'converted_by asc')
    for key in row_data :
        if key["converted_by"] != None and key["converted_by"] != "":
            data.append(key)    
    for owner in data :
        if filters == {} :
            number = frappe.db.count('Opportunity', {'converted_by': owner.converted_by})
            user = frappe.db.get_value('User',owner.converted_by, 'full_name')
            owner ["converted_by"] = user
            owner["count"]= number

        elif filters != {} and "status" in filters.keys() : 
            number = frappe.db.count('Opportunity', {'converted_by': owner.converted_by,"status": filters['status']})
            user = frappe.db.get_value('User',owner.converted_by, 'full_name')
            owner ["converted_by"] = user
            owner["count"]= number

        elif filters != {} and "converted_by" in filters.keys() : 
            number = frappe.db.count('Opportunity', {'converted_by': filters['converted_by']})
            user = frappe.db.get_value('User',owner.converted_by, 'full_name')
            owner ["converted_by"] = user
            owner["count"]= number

    chart = get_open_task_chart(data)
    return columns, data, None, chart

def get_columns():
  columns = [
        {
          "label": _("Owner Name"),
          "fieldname": "converted_by",
          "fieldtype": "Data",
          "width": "180"
        },
        {
          "label": _("No of Opportunities"),
          "fieldname": "count",
          "fieldtype": "Int",
          "width": "180"
        } 
      ]
  return columns

def get_open_task_chart(data):
    converted_by = []
    count = []
    for owner in data:
        converted_by.append(owner.get('converted_by'))
        count.append(owner.get('count'))
    chart_data = {
    'labels':converted_by,
        'datasets': [
        {
        'name':_('Count of Opportunities'),
        'values': count
        }
        ]
    }
    chart = {
        "title": "Total",
        "data": chart_data,
        "type": 'bar',
                'height': 100
        }
    return chart