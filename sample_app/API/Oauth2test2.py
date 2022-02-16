import sys
import frappe
import requests
import json


def get_new_token():
    authorize_url = "http://devsite2.local:8000/api/method/frappe.integrations.oauth2.authorize"
    token_url = "http://devsite2.local:8000/api/method/frappe.integrations.oauth2.get_token"
    callback_uri = "http://devsite2.local:8000/api/method/sample_app.API.Oauth2_test2.get_new_token"
    client_id = "dd82e222e0"
    client_secret = "6a65517911"
    
    
    authorization_redirect_url = authorize_url + '?response_type=code&client_id=' + client_id + '&redirect_uri=' + callback_uri + '&scope=openid'
    authorization_response = requests.post(authorization_redirect_url)    
    if authorization_response.status_code !=200:
        print("Failed to obtain token from the OAuth 2.0 server", file=sys.stderr)
        sys.exit(1)
    else:
        code = json.loads(authorization_response.text)
        authorization_code = code['authorization_code']
    

    data = {'grant_type': 'authorization_code', 'code': authorization_code, 'redirect_uri': callback_uri}
    
    
    token_response = requests.post(token_url, data=data, verify=False, allow_redirects=False, auth=(client_id, client_secret))           
    if token_response.status_code !=200:
        print("Failed to obtain token from the OAuth 2.0 server", file=sys.stderr)
        sys.exit(1)
    else:
        print("Successfuly obtained a new token")
        token = json.loads(token_response.text)
        return token['access_token']

@frappe.whitelist()
def oauth2_test(self, method):
    frappe.msgprint((f'API Called'));
    test_api_url = "http://devsite2.local:8000/api/method/frappe.auth.get_logged_user"
    access_token = get_new_token()


    while True:
        api_call_headers = {'Authorization': 'Bearer ' + access_token}
        api_call_response = requests.get(test_api_url, headers=api_call_headers, verify=False)
        if	api_call_response.status_code == 401:
                    access_token = get_new_token()
        else:
            print(api_call_response.text)
            break