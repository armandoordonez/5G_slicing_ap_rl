import vnf_controller as vnf_controller
from vnf_ip_supervisor import VnfIpSupervisor
import vnf_monitor as vnf_monitor
import requests
from yaml import load
import argparse
import urllib3
from ObserverPattern.vnf_observer_pattern import VnfObserver as Observer
from ObserverPattern.vnf_observer_pattern import VnfIpSubject as IpSubject
import asyncio
class VnfManager(Observer): 
    def __init__(self, base_url):
        self.start(base_url)
        
    def start(self, base_url):
        auth_token = self.get_osm_authentication_token(base_url = base_url)
        ns_id_list = self.get_nsid_list(base_url = base_url, auth_token = auth_token)
        loop = asyncio.get_event_loop()
        
        
        vnf_per_ns = {}
        
        for ns_id in ns_id_list:
            vnf_per_ns[ns_id] =  self.get_vnf_list(base_url, ns_id, auth_token)
        
        print(auth_token)
        vnf_ip_supervisor: {string, VnfIpSupervisor} = {}
        vnf_ip_loop = []
        for ns, vnf_list in vnf_per_ns.items():
            for vnf_id in vnf_list:
                print("instantiation with ns: {} vnf: {}".format(ns, vnf_id))
                #Todo put this above in a thread
                subject = VnfIpSupervisor(base_url = base_url, auth_token = auth_token, vnf_id = vnf_id, ns_id = ns)
                subject.attach(self)
                vnf_ip_supervisor[vnf_id] = subject # two times bug.                
                vnf_ip_loop.append(subject.check_ip_loop())
                

        print("total vnf attached: {} ".format(len(vnf_ip_supervisor)))
        loop.run_until_complete(asyncio.gather(*vnf_ip_loop)) # possible bug two times
        print("brrrr")
            



    def get_osm_authentication_token(self, base_url):
        url = base_url + "admin/v1/tokens"
        payload = "------WebKitFormBoundary7MA4YWxkTrZu0gW\r\nContent-Disposition: form-data; name=\"username\"\r\n\r\nadmin\r\n------WebKitFormBoundary7MA4YWxkTrZu0gW\r\nContent-Disposition: form-data; name=\"password\"\r\n\r\nadmin\r\n------WebKitFormBoundary7MA4YWxkTrZu0gW--"
        headers = {
            'content-type': "multipart/form-data; boundary=----WebKitFormBoundary7MA4YWxkTrZu0gW",
            'cache-control': "no-cache",
            }

        response = requests.request("POST", url, data=payload, headers=headers, verify=False)

        response_parsed = response.content.split()
        return response_parsed[2].decode("utf-8")

    def get_nsid_list(self, base_url, auth_token):
        ns_list = []
        url = base_url + "nslcm/v1/ns_instances"
        payload = ""
        headers = {
            'Content-Type': "application/",
            'Authorization': "Bearer "+ auth_token,
            'cache-control': "no-cache",
            }
        response_in_yaml = load(requests.request("GET", url, data=payload, headers=headers, verify=False).text)
        for ns in response_in_yaml:
            ns_list.append(ns["id"])
        return ns_list

    def get_vnf_list(self, base_url, ns_id, auth_token):
        vnf_list = []
        url = base_url + "nslcm/v1/vnf_instances?nsr-id-ref="+ns_id
        payload = ""
        headers = {
            'Content-Type': "application/",
            'Authorization': "Bearer "+auth_token,
            'cache-control': "no-cache",
            }
        response_in_yaml =  load(requests.request("GET", url, data=payload, headers=headers, verify=False).text)
        for vnf in response_in_yaml:
            vnf_list.append(vnf["_id"])
        
        return vnf_list
    
            
    def updateIpSubject(self, subject: IpSubject) -> None:
        print("reacted from ip {}, number of vnfs: {}, ips: {}".format(subject._current_ips, len(subject._current_ips), subject.vnf_id))
        
if __name__ == "__main__":    
    parser = argparse.ArgumentParser(description="Arguments to work with")
    parser.add_argument('--dst_ip',default="localhost",help='destination ip')
    args = parser.parse_args()
    base_url = "https://"+args.dst_ip+":9999/osm/"
    print("base_url: {}".format(base_url))
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    VnfManager(base_url = base_url)