from __future__ import unicode_literals
import frappe

@frappe.whitelist()
def get_managers(doctype, txt, searchfield, start, page_len, filters):

	return frappe.db.sql("""
		select distinct user.name, user.first_name, user.last_name
		from `tabUser` user
		join `tabHas Role` user_role ON user.name = user_role.parent
		where user_role.role IN (%(role)s)
		and user.name like %(txt)s
		and user.enabled = 1
		and user.name != 'Administrator'
		order by
			if(locate(%(_txt)s, user.name), locate(%(_txt)s, user.name), 99999),
			user.name
		limit %(start)s, %(page_len)s""".format(**{
			'key': searchfield,
		}), {
			'txt': "%%%s%%" % txt,
			'_txt': txt.replace("%", ""),
			'start': start,
			'page_len': page_len,
			'role': filters.get("role")
		})