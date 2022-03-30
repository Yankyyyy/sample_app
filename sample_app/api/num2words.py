import frappe
from num2words import num2words

@frappe.whitelist()
def num_to_words(number, language):
    return num2words(float(number), lang=language, to='currency', currency="SAR")