import requests
import urllib3
from yaml import load


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
        vnfs ips: array
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


    def get_nsid_list(self):
        ''' Get all the Network Slices and their associates vnfs
        Returns
        ----------
        ns_list: array

        
        ns_vnf_dict: dict
        {'network_slice_id'-> {'name'  -> : 'ns_name', 'vnf' -> {index: -> 'vnf_id_at_index_0'}}}
        '''
        ns_list = []
        ns_vnf_dict = {}
        url = self.base_url + "nslcm/v1/ns_instances"
        payload = ""
        print(url)
        headers = {
            'Content-Type': "application/",
            'Authorization': "Bearer " + self.auth_token,
            'cache-control': "no-cache",
        }
        response_in_yaml = load(requests.request(
            "GET", url, data=payload, headers=headers, verify=False).text)
        for ns in response_in_yaml:
            ns_list.append(ns["id"])
            internal_dict = {}
            internal_dict["name"] = ns["name"]
            vnf_data = {}
            for index, vnf_list in enumerate(ns["constituent-vnfr-ref"]):
                vnf_data[index] = vnf_list
            internal_dict["vnf"] = vnf_data
            ns_vnf_dict[ns["id"]] = internal_dict
        # {'network_slice_id': {'name': 'ns_name', 'vnf':{index: 'vnf_id_at_index_0'}}}
        #{'a4833c61-bc96-4b9a-b392-7e05800a7499': {'name': 'ns_name', 'vnf': {0: 'ea37c34f-6e85-46e4-a424-4cb69c0a8735', 1: '64bb6800-d23b-432f-a0c7-16a990e36492'}}}
        return ns_list, ns_vnf_dict
"""
if __name__ == "__main__":
    url = "https://35.184.244.20:9999/osm/"
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

    OsmHelper(url)
"""