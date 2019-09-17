import requests
from yaml import load, dump
# vnf2 
def get_ip_request():
    vnf_id = "016879a0-4323-446f-a50a-6d63ae704a19"
    url = "https://34.94.156.190:9999/osm/nslcm/v1/vnf_instances/016879a0-4323-446f-a50a-6d63ae704a19"
    payload = ""
    headers = {
        'Content-Type': "application/",
        'Authorization': "Bearer oXiFYAVD3SRppzw8i5P2DXbaHyfruL8E",
        'cache-control': "no-cache",
        'Postman-Token': "13ff72dd-8fe4-44cf-905d-e158b09ddb08"
        }
    response = requests.request("GET", url, data=payload, headers=headers, verify=False)
    print(get_current_ips(response,vnf_id)  )
def get_current_ips(response, vnf_id):    
    current_ips = []           
    vnf_ips = {}
    response_in_yaml = load(response.text)       
    for element in response_in_yaml["vdur"]:
            current_ips.append(element["interfaces"][0]["ip-address"])                    
    vnf_ips[vnf_id] = current_ips
    return vnf_ips

get_ip_request()

"""

curl -X POST   https://localhost:9999/osm/nslcm/v1/ns_instances/1d616ba3-eefc-469c-a394-102609dab162/scale   -H 'Authorization: Bearer Z6ixpuSvo35kh7Cx7sC9htIxqj0wnTKA'   -H 'Content-Type: application/json'   -H 'Postman-Token: 7057c832-ab3a-4853-8d0c-b59332fd9ac6'   -H 'cache-control: no-cache'   -d '{"scaleType": "SCALE_VNF","scaleVnfData":{"scaleVnfType": "SCALE_OUT","scaleByStepData":{"scaling-group-descriptor": "apache_vdu_manualscale","member-vnf-index": "1"}}}' -k
curl -X POST https://localhost:9999/osm/admin/v1/tokens -H 'Postman-Token: 70cf1d12-da0e-440f-9c0a-35f9f7f66ddc' -H 'cache-control: no-cache' -H 'content-type: multipart/form-data; boundary=----WebKitFormBoundary7MA4YWxkTrZu0gW' -F username=admin -F password=admin -k

"""