import requests
import time
from yaml import load, dump
import asyncio
from ObserverPattern.vnf_observer_pattern import VnfIpSubject  as IpSubject
class VnfIpSupervisor(IpSubject):
    _current_ips: [] = None
    _current_cpu_load = None 

    _observers = None
    def __init__(self, cadvisor_url, base_url,  auth_token, vnf_id, ns_name, ns_id, member_index):
        self.auth_token = auth_token
        self.vnf_id  = vnf_id
        self.ns_id = ns_id
        self.ns_name = ns_name
        self.base_url = base_url        
        self.member_index = member_index + 1 
        self.cadvisor_url_cpu = cadvisor_url + "v2.0/ps/docker"

        self.cadvisor_url = cadvisor_url +"v1.3/subcontainers/docker"
        self.docker_id, self.docker_name = self.get_docker_id()
        self.cpu_load = None
        
                

    def get_docker_id(self):
        r = requests.get(self.cadvisor_url)
        
        parsed_json = r.json()
        for container in parsed_json:
            try:            
                for alias in container["aliases"]:
                    if self.ns_name in alias :
                       
                        if self.extract_vnf_number(container["aliases"][0]) is self.member_index:
                            self.docker_id = container["aliases"][1]
                            self.docker_name  = container["aliases"][0]
                            #print(self.docker_id)
                        #todo implement mapping between docker_id, docker_name, vnfd, ns
            except KeyError as e:
                pass
                #print("catch error:{}".format(e))
        
        del parsed_json
        return self.docker_id, self.docker_name
    def extract_data_from_docker_name(self, docker_container_name):    
        pass

    def extract_vnf_number(self, docker_container_name):
        number = ""
        for indx, value in enumerate(docker_container_name):
            if value.isdigit() and len(docker_container_name)>indx+2:
                if "-" in docker_container_name[indx-2:indx+2]:
                    number = number + docker_container_name[indx]
        return int(number)
    async def check_ip_loop(self):
        #this loop inside and when the counter be divisible by 5 it shoot out to the manager....
        counter = 0
        print("ciploop..")
        while True:
            if  self.docker_id is not None: 
                await asyncio.sleep(1)
            
                #self._current_ips = self.get_current_ips()            
                self.cpu_load = self.get_current_cpu_usage()            
                counter += 1 
                if self.cpu_load > 50:
                    self.notify()
           
    def get_current_cpu_usage(self):
        r = requests.get(self.cadvisor_url_cpu+"/"+self.docker_id)
        #print(self.cadvisor_url_cpu+"/"+self.docker_id)
        parsed_json = r.json()
        cpu_percentage = 0
        for element in parsed_json:
            #print(element['percent_cpu'])
            cpu_percentage = cpu_percentage + float(element['percent_cpu'])    
        return cpu_percentage
    
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
