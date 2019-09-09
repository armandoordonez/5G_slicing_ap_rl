import requests
def get_ip_request():
    url = "http://34.67.98.227:9999/osm/nslcm/v1/vnf_instances/4528fd0f-b0a7-4474-a6c0-03a94b4057d9"
    payload = ""
    headers = {
        'Content-Type': "application/",
        'Authorization': "Bearer sxLGjl9FfYccbWmFtrqr7XmZlu2qhdP9",
        'cache-control': "no-cache",
        'Postman-Token': "13ff72dd-8fe4-44cf-905d-e158b09ddb08"
        }
    return requests.request("GET", url, data=payload, headers=headers, verify=False)

print(get_ip_request().text)