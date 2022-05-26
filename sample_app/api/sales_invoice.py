from __future__ import unicode_literals
import frappe
from num2words import num2words

@frappe.whitelist()
def set_in_words_arabic(doc, method):
    doc.in_words_arabic = " فقط" +num2words(float(doc.grand_total), lang='ar', to='currency', currency="SAR")