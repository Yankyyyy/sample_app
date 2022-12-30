import frappe
from frappe.utils import cint
from frappe import _, conf

ALLOWED_MIMETYPES = ('image/png', 'image/jpeg', 'application/pdf', 'application/msword',
			'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
			'application/vnd.ms-excel', 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
			'application/vnd.oasis.opendocument.text', 'application/vnd.oasis.opendocument.spreadsheet')

def upload_attachment(data,link_doctype):
	user = frappe.get_doc("User", frappe.session.user)
	is_private = link_doctype.get("is_private")
	doctype = link_doctype.get("doctype")
	docname = link_doctype.get("docname")
	fieldname = link_doctype.get("fieldname")
	file_url = link_doctype.get("file_url")
	folder = link_doctype.get("folder") or 'Home'
	content = None
	filename = None

	if data:
		content = data.stream.read()
		filename = data.filename

	if not file_url and (user and not user.has_desk_access()):
		import mimetypes
		filetype = mimetypes.guess_type(filename)[0]
		if filetype not in ALLOWED_MIMETYPES:
			frappe.throw(_("You can only upload JPG, PNG, PDF, or Microsoft documents."))

	ret = frappe.get_doc({
		"doctype": "File",
		"attached_to_doctype": doctype,
		"attached_to_name": docname,
		"attached_to_field": fieldname,
		"folder": folder,
		"file_name": filename,
		"file_url": file_url,
		"is_private": cint(is_private),
		"content": content
	})
	ret.save(ignore_permissions=True)
	return ret

@frappe.whitelist()
def validateUploadFileSize():
	lang = frappe.request.headers.get('Lang')
	file = frappe.request.files.to_dict()["file"]
	content = None
	max_file_size = get_max_file_size()
	if file:
		content = file.stream.read()
		file_size = len(content)

	if file_size > max_file_size:
		return {
		"msg" : (_("File size exceeded the maximum allowed size", lang = lang)),
		"is_valid_file_size" : 0
		}
	else:
		return {
		"msg" : (_("File size is valid", lang = lang)),
		"is_valid_file_size" : 1
		}

def get_max_file_size():
	return cint(conf.get('max_file_size')) or 10000000
