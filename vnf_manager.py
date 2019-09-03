import vnf_controller as vnf_controller
from vnf_ip_supervisor import VnfIpSupervisor
import vnf_monitor as vnf_monitor
import requests

def get_osm_authentication_token():
    url = "https://localhost:9999/osm/admin/v1/tokens"
    payload = "------WebKitFormBoundary7MA4YWxkTrZu0gW\r\nContent-Disposition: form-data; name=\"username\"\r\n\r\nadmin\r\n------WebKitFormBoundary7MA4YWxkTrZu0gW\r\nContent-Disposition: form-data; name=\"password\"\r\n\r\nadmin\r\n------WebKitFormBoundary7MA4YWxkTrZu0gW--"
    headers = {
        'content-type': "multipart/form-data; boundary=----WebKitFormBoundary7MA4YWxkTrZu0gW",
        'cache-control': "no-cache",
        }

    response = requests.request("POST", url, data=payload, headers=headers, verify=False)

    response_parsed = response.content.split()
    return response_parsed[2].decode("utf-8")

def get_ns_list(auth_token):
    url = "https://localhost:9999/osm/nslcm/v1/ns_instances"
    payload = ""
    headers = {
        'Content-Type': "application/",
        'Authorization': "Bearer "+ auth_token,
        'cache-control': "no-cache",
        }
    return requests.request("GET", url, data=payload, headers=headers, verify=False)

def get_vnf_list(ns_id, auth_token):
    url = "https://localhost:9999/osm/nslcm/v1/vnf_instances?nsr-id-ref="+ns_id
    payload = ""
    headers = {
        'Content-Type': "application/",
        'Authorization': "Bearer "+auth_token,
        'cache-control': "no-cache",
        }
    return requests.request("GET", url, data=payload, headers=headers, verify=False)


if __name__ == "__main__":
    auth_token = get_osm_authentication_token()
    print(get_ns_list(auth_token).text)

    """
    osm_auth_token = get_osm_authentication_token()
    VnfIpSupervisor(osm_auth_token, )
    """