# -*- coding: utf-8 -*-
# Copyright (c) 2020, Leader Investment Group
import frappe
import inspect

def createAPIErrorLog(error):
    """Create error log according the method from where createAPIErrorLog been called"""
    error_log =  frappe.new_doc("Error Log")
    error_log.method = inspect.stack()[1][3] #called method name will be fetched
    error_log.error = error
    error_log.save(ignore_permissions=True)

