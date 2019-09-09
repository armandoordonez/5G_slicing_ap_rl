import requests
import asyncio
import json 

class VnfScaleModule():
    def __init__(self, auth_token, base_url):
        self.auth_token = auth_token
        self.base_url = base_url
    
    #SCALE_OUT: adds.
    #SCALE_IN: scale down.
    def scale_instance(self, ns_id, scale_decision, member_index):
        url = self.base_url + "nslcm/v1/ns_instances/"+ns_id+"/scale"
        payload_str = {"scaleType": "SCALE_VNF","scaleVnfData":{"scaleVnfType": scale_decision,"scaleByStepData":{"scaling-group-descriptor": "scale_cirros","member-vnf-index": str(member_index)}}}
        payload =json.dumps(payload_str)
        print(payload)
        headers = {
            'Content-Type': "application/",
            'Authorization': "Bearer "+self.auth_token,
            'cache-control': "no-cache",
        }        
        response =  requests.request("POST", url, data=payload, headers=headers, verify=False)
        print(response.text)



        



"""
url =  "https://34.67.193.200/admin/v1/tokens"
payload = "------WebKitFormBoundary7MA4YWxkTrZu0gW\r\nContent-Disposition: form-data; name=\"username\"\r\n\r\nadmin\r\n------WebKitFormBoundary7MA4YWxkTrZu0gW\r\nContent-Disposition: form-data; name=\"password\"\r\n\r\nadmin\r\n------WebKitFormBoundary7MA4YWxkTrZu0gW--"
headers = {
    'content-type': "multipart/form-data; boundary=----WebKitFormBoundary7MA4YWxkTrZu0gW",
    'cache-control': "no-cache",
}
response = requests.request("POST", url, data=payload, headers=headers, verify=False)
response_parsed = response.content.split()
print(response_parsed)
"""