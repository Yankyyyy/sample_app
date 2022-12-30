import frappe
import json
from foxerp.utils import createAPIErrorLog
from math import *

def validated_user_current_location(doc,method):
    """Validates Employee Current location against employee   geolocations defined on Employee master"""
    #lat and lon are coordinates of employee current location
    employee = frappe.get_doc("Employee",doc.employee)
    isValidLocation = 0
    valid_locations=[]
    if employee.enable_geofencing == 1:
        for employee_geolocation in employee.employee_geolocation:
            #distnace in meter
            distance = haversine(float(doc.latitude),float(doc.longitude),float(employee_geolocation.latitude),float(employee_geolocation.longitude)) 
            if distance < employee_geolocation.work_radius:
                isValidLocation = 1
                break;
        
        if isValidLocation == 1:
            pass
        else:
            location_status_message = "Employee: "+ employee.employee_name+ " is not allowed to login from the current location.Contact your HR to disable geolocation for you."
            frappe.throw(location_status_message)

def haversine(lat1, lon1, lat2, lon2):
    """
    Calculate the great circle distance in meter between two points 
    on the earth (specified in decimal degrees)
    """
    # convert decimal degrees to radians 
    lat1, lon1, lat2, lon2 = map(radians, [ lat1, lon1, lat2, lon2 ])
    #lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])
    # haversine formula 
    dlon = lon2 - lon1 
    dlat = lat2 - lat1 
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a)) 
    r = 6371000 # Radius of earth in meters.
    return c * r