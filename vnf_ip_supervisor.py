import requests
import time
from yaml import load, dump

class VnfIpSupervisor:
    def __init__(self, auth_token, vnf_id, ns_id):
        self.auth_token = auth_token
        self.vnf_id  = vnf_id
        self.ns_id = ns_id
        self.check_ip_loop()
    def get_ip_request(self):
        url = "https://localhost:9999/osm/nslcm/v1/vnf_instances/"+self.vnf_id
        payload = ""
        headers = {
            'Content-Type': "application/",
            'Authorization': "Bearer "+self.auth_token,
            'cache-control': "no-cache",
            'Postman-Token': "13ff72dd-8fe4-44cf-905d-e158b09ddb08"
            }
        return requests.request("GET", url, data=payload, headers=headers, verify=False)
    def get_current_ips(self):
        current_ips = []
        response = self.get_ip_request()        
        response_in_yaml = load(response.text)
        for element in response_in_yaml["vdur"]:
                current_ips.append(element["interfaces"][0]["ip-address"])
        
        return current_ips

    def check_ip_loop(self):
        while True:
            time.sleep(1)
            print("ns: {}..., vnf: {}..., current_ips:".format(self.vnf_id[:10], self.ns_id[:10]))
            print(*self.get_current_ips(),sep=",")

    
"""
if __name__ == "__main__":
    url = "https://localhost:9999/osm/admin/v1/tokens"
    payload = "------WebKitFormBoundary7MA4YWxkTrZu0gW\r\nContent-Disposition: form-data; name=\"username\"\r\n\r\nadmin\r\n------WebKitFormBoundary7MA4YWxkTrZu0gW\r\nContent-Disposition: form-data; name=\"password\"\r\n\r\nadmin\r\n------WebKitFormBoundary7MA4YWxkTrZu0gW--"
    headers = {
        'content-type': "multipart/form-data; boundary=----WebKitFormBoundary7MA4YWxkTrZu0gW",
        'cache-control': "no-cache",
        'Postman-Token': "1f493fd0-4ae5-47f3-b03d-c08f9a106c4c"
        }

    response1 = requests.request("POST", url, data=payload, headers=headers, verify=False)

    response_parsed = response1.content.split()
    VnfSupervisor(auth_token = response_parsed[2].decode("utf-8"), vnf_id = "0c470c68-3465-4048-9b8d-b1a962973a8f")





url = "https://localhost:9999/osm/admin/v1/tokens"

payload = "------WebKitFormBoundary7MA4YWxkTrZu0gW\r\nContent-Disposition: form-data; name=\"username\"\r\n\r\nadmin\r\n------WebKitFormBoundary7MA4YWxkTrZu0gW\r\nContent-Disposition: form-data; name=\"password\"\r\n\r\nadmin\r\n------WebKitFormBoundary7MA4YWxkTrZu0gW--"
headers = {
    'content-type': "multipart/form-data; boundary=----WebKitFormBoundary7MA4YWxkTrZu0gW",
    'cache-control': "no-cache",
    'Postman-Token': "1f493fd0-4ae5-47f3-b03d-c08f9a106c4c"
    }

response1 = requests.request("POST", url, data=payload, headers=headers, verify=False)

response_parsed = response1.content.split()

# /vnf_id/
url = "https://localhost:9999/osm/nslcm/v1/vnf_instances/0c470c68-3465-4048-9b8d-b1a962973a8f"

payload = ""
headers = {
    'Content-Type': "application/",
    'Authorization': "Bearer "+response_parsed[2].decode("utf-8"),
    'cache-control': "no-cache",
    'Postman-Token': "13ff72dd-8fe4-44cf-905d-e158b09ddb08"
    }



response2 = requests.request("GET", url, data=payload, headers=headers, verify=False)
response_in_yaml = load(response2.text)
for element in response_in_yaml["vdur"]:
    print(element["interfaces"][0]["ip-address"])


"""
