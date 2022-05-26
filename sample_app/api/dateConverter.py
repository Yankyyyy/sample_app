import frappe
from ummalqura.hijri_date import HijriDate


@frappe.whitelist()
def gregorian_to_hijri(date):   #Gregorean date format : 2017-12-26
    return HijriDate.get_hijri_date(date)

@frappe.whitelist()
def hijri_to_gregorian(date):   #Hijri date format : 1439-04-08
    return HijriDate.get_georing_date(date)