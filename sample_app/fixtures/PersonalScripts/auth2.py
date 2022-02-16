# import sys
# import subprocess
import frappe
import requests
import json



@frappe.whitelist(allow_guest=True)
def callback(code):
    return code



@frappe.whitelist(allow_guest=True)
def get_new_token():

    auth_url = "http://devsite2.local:8000/api/method/frappe.integrations.oauth2.authorize"

    auth_payload='redirect_uri=http%3A%2F%2Fdevsite2.local%3A8000%2Fapi%2Fmethod%2Fsample_app.fixtures.PersonalScripts.trial.callback&client_id=dd82e222e0&response_type=code&client_secret=6a65517911'

    auth_headers = {
    'sid': 'f138971e3df02068a9c79a0b85b046c79e2b7c06b7602bd6ca949f6e',
    'Content-Type': 'application/x-www-form-urlencoded',
    'Cookie': 'full_name=Administrator%20gcghcjycfjyfcxjf; sid=f138971e3df02068a9c79a0b85b046c79e2b7c06b7602bd6ca949f6e; system_user=yes; user_id=Administrator; user_image='
    }

    auth_response = requests.request("POST", auth_url, headers=auth_headers, data=auth_payload)

    code = json.loads(auth_response.text)

    token_url = "http://devsite2.local:8000/api/method/frappe.integrations.oauth2.get_token"

    token_payload=f'grant_type=authorization_code&code={code["message"]}&client_id=dd82e222e0'

    token_headers = {
    'Content-Type': 'application/x-www-form-urlencoded',
    'Cookie': 'full_name=Administrator%20gcghcjycfjyfcxjf; sid=f138971e3df02068a9c79a0b85b046c79e2b7c06b7602bd6ca949f6e; system_user=yes; user_id=Administrator; user_image='
    }

    token_response = requests.request("POST", token_url, headers=token_headers, data=token_payload)
    
    access_token = json.loads(token_response.text)
    
    frappe.msgprint(access_token["access_token"])

    return access_token["access_token"]
