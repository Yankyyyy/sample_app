// Copyright (c) 2016, Leader Group and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Tracker Report"] = {
    "filters": [
                {
					"label" : __("Project"),
					"fieldname" : "project",
					"fieldtype" : "Link",
					"options" : "Project"
		
                },
                {
					"label" : __("Status"),
					"fieldname" : "status",
					"fieldtype" : "Select",
					"options" : "\nOpen\nWorking\nPending Review\nOverdue\Template\nCompleted\nCancelled"
                },
        		{
        			"fieldname": "date",
        			"label": __("Printed On"),
        			"fieldtype": "Data",
        			"default": moment(frappe.datetime.now_datetime()).format("MM-DD-YYYY HH:mm:ss"),
                    read_only: 1
        		}
            ]
        };



