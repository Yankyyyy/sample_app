import frappe
from frappe.core.doctype.file.file import create_new_folder
from foxerp.utils import createAPIErrorLog
from frappe.utils import cint


ALLOWED_MIMETYPES = ('text/csv', 'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
			'application/vnd.ms-excel', 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
            'application/vnd.oasis.opendocument.spreadsheet')


@frappe.whitelist()
def upload_salary_slip_files():
    """ checking whether the Payroll folder exists,if not creating a folder named Payroll """
    try:
        for file in frappe.request.files.to_dict():
            file_url = None
            if frappe.request.files[file]:
                user = frappe.get_doc("User", frappe.session.user)
                if frappe.db.exists({
                        "doctype": "File",
                        "file_name": "Payroll",
                        "is_folder": 1,
                        "folder": "Home"
                    }):
                    folder = "Home/Payroll"
                else:
                    create_new_folder('Payroll', 'Home')
                    folder = "Home/Payroll"
                is_private = 1
                doctype = "Salary Slip"
                content = None
                filename = None
                data = frappe.request.files[file]
                content = data.stream.read()
                filename = data.filename
                if not file_url and (user and not user.has_desk_access()):
                    import mimetypes
                    """checking the type of file uploaded"""
                    filetype = mimetypes.guess_type(filename)[0]
                    if filetype not in ALLOWED_MIMETYPES:
                        frappe.throw("You can only upload Microsoft documents.")

                file_details = frappe.get_doc({
                    "doctype": "File",
                    "attached_to_doctype": doctype,
                    "folder": folder,
                    "file_name": filename,
                    "file_url": file_url,
                    "is_private": cint(is_private),
                    "content": content
                })
                file_details.save(ignore_permissions=True)
        return {
            "filename": filename,
            "message" : "File Successfully Uploaded."
        }
    except Exception:
        error = frappe.get_traceback()
        createAPIErrorLog(error)
        return error