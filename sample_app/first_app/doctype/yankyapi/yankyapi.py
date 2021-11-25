# # Copyright (c) 2021, Yanky and contributors
# # For license information, please see license.txt


# # import frappe

from frappe.model.document import Document

class YankyAPI(Document):
	pass


# from __future__ import unicode_literals

# import frappe
# from erpnext.accounts.party import set_taxes
# from erpnext.controllers.selling_controller import SellingController
# from frappe import _
# from frappe.contacts.address_and_contact import load_address_and_contact
# from frappe.email.inbox import link_communication_to_document
# from frappe.model.mapper import get_mapped_doc
# from frappe.utils import cint, comma_and, cstr, getdate, has_gravatar, nowdate, validate_email_address

# class YankyAPI(SellingController):

# 	def before_insert(self):
# 		if self.address_title and self.address_type:
# 			self.address_doc = self.create_address()
# 		self.contact_doc = self.create_contact()

# 	def after_insert(self):
# 		self.update_links()


# 	def create_address(self):
# 		address_fields = ["address_type", "address_title", "address_line1",
# 			"city", "county", "state", "country", "pincode"]
# 		info_fields = ["email_id"]

# 		# do not create an address if no fields are available,
# 		# skipping country since the system auto-sets it from system defaults
# 		address = frappe.new_doc("Address")

# 		address.update({addr_field: self.get(addr_field) for addr_field in address_fields})
# 		address.update({info_field: self.get(info_field) for info_field in info_fields})
# 		address.insert()

# 		return address

# 	def create_contact(self):
# 		contact = frappe.new_doc("Contact")
# 		contact.update({
# 			"first_name": full_name,
# 			"last_name": full_name,
# 			"gender": self.gender,
# 			"designation": self.designation,
# 		})

# 		if self.email_id:
# 			contact.append("email_ids", {
# 				"email_id": self.email_id,
# 				"is_primary": 1
# 			})

# 		if self.phone:
# 			contact.append("phone_nos", {
# 				"phone": self.phone,
# 				"is_primary_phone": 1
# 			})

# 		if self.mobile_no:
# 			contact.append("phone_nos", {
# 				"phone": self.mobile_no,
# 				"is_primary_mobile_no":1
# 			})

# 		contact.insert(ignore_permissions=True)

# 		return contact

# 	def update_links(self):
# 		# update address links
# 		if hasattr(self, 'address_doc'):
# 			self.address_doc.append("links", {
# 				"link_doctype": "YankyAPI",
# 				"link_name": self.full_name,
# 				"link_title": self.full_name
# 			})
# 			self.address_doc.save()

# 		# update contact links
# 		if self.contact_doc:
# 			self.contact_doc.append("links", {
# 				"link_doctype": "YankyAPI",
# 				"link_name": self.full_name,
# 				"link_title": self.full_name
# 			})
# 			self.contact_doc.save()



# def _set_missing_values(source, target):
# 	address = frappe.get_all('Dynamic Link', {
# 			'link_doctype': source.doctype,
# 			'link_name': source.name,
# 			'parenttype': 'Address',
# 		}, ['parent'], limit=1)

# 	contact = frappe.get_all('Dynamic Link', {
# 			'link_doctype': source.doctype,
# 			'link_name': source.name,
# 			'parenttype': 'Contact',
# 		}, ['parent'], limit=1)

# 	if address:
# 		target.customer_address = address[0].parent

# 	if contact:
# 		target.contact_person = contact[0].parent


# # from __future__ import unicode_literals

# # import frappe

# # def get_context(context):
# # 	# do your magic here
# # 	context.show_sidebar = True


# # from __future__ import unicode_literals

# # import frappe
# # from frappe.model.document import Document
# # from frappe import _
# # from andesit_karang_anyar.utilities.driverlist import load_drivers

# # class Vehicle(Document):

# # 	def onload(self):

# # 		dlist = load_drivers(self.wb_vehicle_registration)

		
# # 		self.get("__onload").driver_list = dlist

# 	# def fetch_driver_info(self, driverdocname):

# 	# 	frappe.msgprint(driverdocname)

# 	# 	dr = frappe.get_doc("Driver", driverdocname)

# 	# 	return dr