import frappe
import json
from foxerp.utils import createAPIErrorLog


@frappe.whitelist()
def createHolidayList():
    # function to create holiday list in foxerp
    try:
        data = json.loads(frappe.request.data)
        if frappe.db.exists('Holiday List', {'name': data.get('name')}):
            return "Holiday list already exists"
        else:
            holiday_list = frappe.new_doc('Holiday List')
            if data.get('name'):
                holiday_list.holiday_list_name = data.get('name')
            if data.get('from_date'):
                holiday_list.from_date = data.get('from_date')
            if data.get('to_date'):
                holiday_list.to_date = data.get('to_date')
            if data.get('date') and data.get('description'):
                date = data.get('date')
                description = data.get('description')
                for i in range(0, len(date)):
                    holiday_list.append("holidays",{
                        "holiday_date": date[i],
                        "description": description[i]
                    })
            holiday_list.save(ignore_permissions=True)
            frappe.db.commit()
            return "Holiday list created successfully"
    except Exception:
        createAPIErrorLog(frappe.get_traceback())
        

@frappe.whitelist()
def updateHolidayList():
    # function to update holiday list in foxerp
    try:
        data = json.loads(frappe.request.data)
        if not frappe.db.exists('Holiday List', {'name': data.get('name')}):
            createHolidayList()
        else:
            holiday_list = frappe.get_doc("Holiday List", {"name": data.get("name")})
            if holiday_list.name != data.get('name'):
                holiday_list.holiday_list_name = data.get('name')
            if str(holiday_list.from_date) != str(data.get('from_date')):
                holiday_list.from_date = data.get('from_date')
            if str(holiday_list.to_date) != data.get('to_date'):
                holiday_list.to_date = data.get('to_date')
            if data.get('date') and data.get('description'):
                date = data.get('date')
                description = data.get('description')
                for i in range(0, len(date)):
                    holiday_list.append("holidays",{
                        "holiday_date": date[i],
                        "description": description[i]
                    })
            holiday_list.save(ignore_permissions=True)
            frappe.db.commit()
            return "Holiday list updated successfully"
    except Exception:
        createAPIErrorLog(frappe.get_traceback())
