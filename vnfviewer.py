import requests
  
url = "https://localhost:9999/osm/admin/v1/tokens"

payload = "------WebKitFormBoundary7MA4YWxkTrZu0gW\r\nContent-Disposition: form-data; name=\"username\"\r\n\r\nadmin\r\n------WebKitFormBoundary7MA4YWxkTrZu0gW\r\nContent-Disposition: form-data; name=\"password\"\r\n\r\nadmin\r\n------WebKitFormBoundary7MA4YWxkTrZu0gW--"
headers = {
    'content-type': "multipart/form-data; boundary=----WebKitFormBoundary7MA4YWxkTrZu0gW",
    'cache-control': "no-cache",
    'Postman-Token': "1f493fd0-4ae5-47f3-b03d-c08f9a106c4c"
    }

response1 = requests.request("POST", url, data=payload, headers=headers, verify=False)

response_parsed = response1.content.split()


url = "https://localhost:9999/osm/nslcm/v1/vnf_instances/0c470c68-3465-4048-9b8d-b1a962973a8f"

payload = ""
headers = {
    'Content-Type': "application/x-www-form-urlencoded",
    'Authorization': "Bearer "+response_parsed[2].decode("utf-8"),
    'cache-control': "no-cache",
    'Postman-Token': "13ff72dd-8fe4-44cf-905d-e158b09ddb08"
    }



response2 = requests.request("GET", url, data=payload, headers=headers, verify=False)

print(response2.json())