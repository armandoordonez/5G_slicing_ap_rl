import requests
import time
from yaml import load, dump
import asyncio
from ObserverPattern.vnf_observer_pattern import VnfIpSubject  as IpSubject
class VnfIpSupervisor(IpSubject):
    _current_ips: [] = None
    _current_cpu_load = None 
    _observers = None
    def __init__(self, cadvisor_url, base_url,  auth_token, vnf_id, ns_name, ns_id):
        self.auth_token = auth_token
        self.vnf_id  = vnf_id
        self.ns_id = ns_id
        self.ns_name = ns_name
        self.base_url = base_url
        self.cadvisor_url = cadvisor_url
                
    def get_ip_request(self):
        url = self.base_url + "nslcm/v1/vnf_instances/"+self.vnf_id
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
        response_in_yaml = load(response.text)  # todo get ips from another source different of "vdur"         
        for element in response_in_yaml["vdur"]:
                current_ips.append(element["interfaces"][0]["ip-address"])
                     
        return current_ips

    async def check_ip_loop(self):
        #this loop inside and when the counter be divisible by 5 it shoot out to the manager....
        counter = 0
        print("ciploop..")
        while True:
            await asyncio.sleep(1)
            self._current_ips = self.get_current_ips()            
            counter += 1 
            if not (counter%5):
                self.notify()

    
    def attach (self, observer) -> None:
        print("{} subject: attached to an observer".format(self.vnf_id))
        self._observers = observer
    
    def detach(self, observer) -> None:
        print("subject: remove  an observer")
        self._observers = None
    
    
    def notify(self) -> None: 
        #print("total observers {}, notifying observers...".format(len(self._observers)))
        print("notifying....")
        self._observers.updateIpSubject(self)
