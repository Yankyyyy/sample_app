from __future__ import unicode_literals
import frappe
from num2words import num2words
from ummalqura.hijri_date import HijriDate

@frappe.whitelist()
def set_in_words_arabic(doc, method):
    number = doc.rounded_total
    date = doc.posting_date
    if number:
        doc.in_words_arabic = num2words(float(number), lang='ar', to='currency', currency="SAR") + " فقط"
    if date:
        doc.hijri_date = HijriDate.get_hijri_date(date)