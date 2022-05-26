import frappe
from frappe.utils import cint

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