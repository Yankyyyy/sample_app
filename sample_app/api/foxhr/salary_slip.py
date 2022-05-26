import frappe
import json
from foxerp.utils import createAPIErrorLog
 
@frappe.whitelist()
def create_salary_slips():
    """Creates Salary slips"""
    data =json.loads(frappe.request.data)
    sl_response ={}
    salary_slip_details = []
    error_salary_slip_details =[]

    for salary_slip_data in data.get("data"):
        sl =create_salary_slip(salary_slip_data)
        if sl.get("has_created") == 0:
            error_salary_slip_details.append(sl)
        else:
            salary_slip_details.append(sl)
        
    sl_response["salary_slip_details"] = salary_slip_details
    sl_response["error_salary_slip_details"] = error_salary_slip_details
    return sl_response

@frappe.whitelist()
def create_salary_slip(data): 
    sl={} 
    try:
        salary_slip = frappe.new_doc('Salary Slip')
        salary_slip.posting_date =  data.get("posting_date")
        salary_slip.employee =  data.get("employee")
        salary_slip.company =  data.get("company")
        salary_slip.start_date =  data.get("start_date") 
        salary_slip.end_date =  data.get("end_date")
        salary_slip.total_working_days =  data.get("total_working_days") 
        salary_slip.payment_days =  data.get("payment_days")
        salary_slip.currency =  data.get("currency")
        salary_slip.unmarked_days =  data.get("unmarked_days")
        salary_slip.leave_without_pay =  data.get("leave_without_pay")
        salary_slip.absent_days =  data.get("absent_days")

        salary_slip.set('earnings', [])
        for earning in data.get("earnings_list"):
            salary_slip_earning = salary_slip.append('earnings', {}) 
            salary_slip_earning.salary_component = earning.get("salary_component")
            salary_slip_earning.amount = earning.get("amount")
            
        salary_slip.set('deductions', [])
        for deduction in data.get("deductions_list"):
            salary_slip_earning = salary_slip.append('deductions', {}) 
            salary_slip_earning.salary_component = deduction.get("salary_component")
            salary_slip_earning.amount = deduction.get("amount")
        
        salary_slip.save(ignore_permissions=True)
        salary_slip.submit()
        sl["emp_id"] = data.get("employee")
        sl["sl_erpnext_id"] = salary_slip.name
        sl["has_created"] = 1
    except Exception as e:
        sl["has_created"] = 0
        sl["emp_id"] = data.get("employee")
        sl["error"] = e
        createAPIErrorLog(frappe.get_traceback())
    return sl