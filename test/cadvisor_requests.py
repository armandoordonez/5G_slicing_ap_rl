import requests

cadvisor_url = "http://34.67.226.47:8080/api/v1.3/subcontainers/docker"

r = requests.get(cadvisor_url)
parsed_json = r.json()
for container in parsed_json:
    try:
        print(container["aliases"][0])
    except KeyError:
        print("key error: aliases")
    