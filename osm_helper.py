import requests
import urllib3

class OsmHelper():
    def __init__(self, osm_url):
        self.base_url = osm_url
        self.auth_token = self.get_osm_authentication_token()
    
    def get_osm_authentication_token(self):
        '''
        OSM needs an auth token, you can modify the default user and password in the payload.

        Returns
        ----------
        auth token
            An array with the ips.

        '''
        url = self.base_url + "admin/v1/tokens"
        payload = "------WebKitFormBoundary7MA4YWxkTrZu0gW\r\nContent-Disposition: form-data; name=\"username\"\r\n\r\nadmin\r\n------WebKitFormBoundary7MA4YWxkTrZu0gW\r\nContent-Disposition: form-data; name=\"password\"\r\n\r\nadmin\r\n------WebKitFormBoundary7MA4YWxkTrZu0gW--"
        headers = {
            'content-type': "multipart/form-data; boundary=----WebKitFormBoundary7MA4YWxkTrZu0gW",
            'cache-control': "no-cache",
        }

        print("getting auth token: {}".format(url))
        response = requests.request("POST", url, data=payload, headers=headers, verify=False)
        response_parsed = response.content.split()
        return response_parsed[2].decode("utf-8")
    
    def get_vnf_current_ips(self, vnf_id):
        '''Get the current ip for a given vnf 
        Parameters
        ----------
        vnf_id: str
            The vnf id 

        Returns
        ----------
        vnfs ips
            An array with the ips. 
        '''
        url = self.base_url + "nslcm/v1/vnf_instances/"+vnf_id
        print("getting ips")
        payload = ""
        headers = {
            'Content-Type': "application/",
            'Authorization': "Bearer "+self.auth_token,
            'cache-control': "no-cache",
            }
        response = requests.request("GET", url, data=payload, headers=headers, verify=False)        
        current_ips = []           
        vnf_ips = {}
        response_in_yaml = load(response.text)       
        for element in response_in_yaml["vdur"]:
                current_ips.append(element["interfaces"][0]["ip-address"])                    
        vnf_ips[vnf_id] = current_ips
        print(vnf_ips)
        return vnf_ips 
"""
if __name__ == "__main__":
    url = "https://35.184.244.20:9999/osm/"
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

    OsmHelper(url)
"""