{{ frappe.format_date(due_date} }}

or

{{ doc.get_formatted(due_date) }}

or

{{frappe.utils.formatdate(due_date, “dd-MM-yyyy”)}}

or

{{frappe.utils.formatdate(doc.due_date, "dd-MM-yyyy")}}

or

{{frappe.utils.formatdate(doc.due_date, "dd-MM-yyyy")}}