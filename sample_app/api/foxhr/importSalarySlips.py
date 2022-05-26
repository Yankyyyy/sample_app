import frappe
from foxerp.utils import createAPIErrorLog

@frappe.whitelist()
def import_salary_slips(filename):
    try:
        #get the csv/excel file from 'File'
        import_file = frappe.get_doc('File', {'file_name': filename})
        data_import = get_importer("Salary Slip", import_file)
        #start the import and create the salary slips
        data_import.start_import()
        return "File Imported Successfully."
    except Exception:
        error = frappe.get_traceback()
        createAPIErrorLog(error)
        return error


def get_importer(doctype, import_file, update=False, submit_after_import=True):
    #set up the import parameters
    data_import = frappe.new_doc('Data Import')
    data_import.import_type = 'Insert New Records' if not update else 'Update Existing Records'
    data_import.submit_after_import = submit_after_import
    data_import.reference_doctype = doctype
    data_import.import_file = import_file.file_url
    data_import.insert()
    frappe.db.commit()

    return data_import