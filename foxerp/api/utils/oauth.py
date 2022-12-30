import frappe
import requests
import json
from leadergroup.utils import createAPIErrorLog
from frappe.utils.password import update_password, check_password

@frappe.whitelist()
def callback(code):
    return code

@frappe.whitelist(allow_guest=True)
def login():
    if frappe.request.data:
        try:
            data = json.loads(frappe.request.data)
            app_name = data.get("app_name")
            usr = data.get("usr")
            pwd = data.get("pwd")

            # To get sid and other details from cookies
            cookies = frappe_login(usr,pwd)

            if cookies:
                cookie_string = "; ".join([str(x)+"="+str(y) for x,y in cookies.items()])
                if app_name:
                    if not frappe.db.exists("OAuth Client",{"app_name": app_name }):
                        frappe.throw(app_name+ " OAuth Client Not Found")
                    else:
                        oauth_client = frappe.db.get_value("OAuth Client",{"app_name": app_name },["client_id","default_redirect_uri","grant_type"],as_dict=1)
                        client_id = oauth_client.client_id
                        redirect_uri = oauth_client.default_redirect_uri
                        grant_type = oauth_client.grant_type

                        if grant_type == "Authorization Code":
                            hostname = frappe.utils.get_url()
                            auth_url = hostname + "/api/method/frappe.integrations.oauth2.authorize"
                            token_url = hostname + "/api/method/frappe.integrations.oauth2.get_token"
                            headers = {
                                'Content-Type': 'application/x-www-form-urlencoded',
                                'Cookie': cookie_string
                            }

                            # To get authorize code from OAuth2 login
                            payload= f'redirect_uri={redirect_uri}&client_id={client_id}&response_type=code'
                            response = requests.request("POST", auth_url, headers=headers, data=payload)
                            response_text = json.loads(response.text)
                            if response.status_code != 200:
                                frappe.throw(response_text.get("_server_messages"))
                            else:
                                # To get access token using authorize code
                                if response_text.get("message"):
                                    payload= f'grant_type=authorization_code&code={response_text.get("message")}&client_id={client_id}'
                                    token_resp = requests.request("POST", token_url, headers=headers, data=payload)
                                    token_resp_text = json.loads(token_resp.text)
                                    if token_resp.status_code != 200:
                                        frappe.throw(token_resp_text.get("_server_messages"))
                                    else:
                                        return token_resp_text
                        else:
                            frappe.throw("Grant Type in Oauth Client is not Authorization Code")
                else:
                    frappe.throw("Please Provide OAuth Client App Name")
        except Exception:
            error = frappe.get_traceback()
            createAPIErrorLog(error)
            return error

def frappe_login(usr,pwd):
    login_url = frappe.utils.get_url() + "/api/method/login"
    payload = json.dumps({"usr": usr, "pwd": pwd })
    headers = {
        'Content-Type': 'application/json'
    }
    session = requests.Session()
    login_resp = session.request("POST", login_url, headers=headers, data=payload)
    if login_resp.status_code == 200:
        return session.cookies.get_dict()
    else:
        login_resp_text = json.loads(login_resp.text)
        frappe.throw(login_resp_text.get("message"))

@frappe.whitelist()
def get_access_token_from_refresh_token(refresh_token):
    try:
        #getting access token from valid refresh token
        token_url =  frappe.utils.get_url() + "/api/method/frappe.integrations.oauth2.get_token"
        token_payload= f'grant_type=refresh_token&refresh_token={refresh_token}'
        token_headers = {
            'Content-Type': 'application/x-www-form-urlencoded'
        }
        token_response = requests.request("POST", token_url, headers=token_headers, data=token_payload)
        token_response_text = json.loads(token_response.text)
        if token_response.status_code != 200:
            frappe.throw(token_response_text.get("_server_messages"))
        else:
            return token_response_text
    except Exception:
        error = frappe.get_traceback()
        createAPIErrorLog(error)
        return error

@frappe.whitelist()
def revoke_access_token(access_token):
    try:
        #access token  and refresh token which created along will be revoked
        url = frappe.utils.get_url() + "/api/method/frappe.integrations.oauth2.revoke_token"
        payload= f'token={access_token}'
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded'
        }
        response = requests.request("POST", url, headers=headers, data=payload)
        response_text = json.loads(response.text)
        if response.status_code != 200:
            frappe.throw(response_text.get("_server_messages"))
        else:
            return response_text
    except Exception:
        error = frappe.get_traceback()
        createAPIErrorLog(error)
        return error     