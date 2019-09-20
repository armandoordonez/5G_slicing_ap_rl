import requests
import time
from yaml import load, dump
import asyncio, maya
import math
from ObserverPattern.vnf_observer_pattern import VnfCpuSubject  as CpuSubject
class VnfCpuSupervisor(CpuSubject):
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
        self.cadvisor_url_cpu = cadvisor_url + "v1.0/containers/docker"
        self.sampling_time_sec = 5 
        self.cadvisor_url = cadvisor_url + "v1.3/subcontainers/docker"
        self.nano_secs = math.pow(10, 9)
        self.docker_id, self.docker_name = self.get_docker_id()
        self.cpu_load = None
        
                
    #todo: sistema no funciona si no hay dockers containers corriendo 
    def get_docker_id(self):
        r = requests.get(self.cadvisor_url)
        print(self.cadvisor_url)
        parsed_json = r.json()
        #counter = 0 
        print("member index: {}".format(self.member_index))
        print()
        for container in parsed_json:
            try:            
                for alias in container["aliases"]:
                    if self.ns_name in alias :                       
                        if self.extract_vnf_number(container["aliases"][0]) is self.member_index and (container["aliases"][0][-1:] is "1"):
                            self.docker_id = container["aliases"][1]
                            self.docker_name  = container["aliases"][0]
                            print(container["aliases"])
                            print(container["aliases"][0][-1:])
                        #todo implement mapping between docker_id, docker_name, vnfd, ns
            except KeyError as e:
                
                pass
                print("catch error:{}".format(e))
        
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
        print("check cpu loop..{}".format(self.docker_id))
        while True:
            if  self.docker_id is not None: 
                await asyncio.sleep(self.sampling_time_sec)           
                self.cpu_load = self.get_current_cpu_usage()            
                print("current ip usage {}".format(self.cpu_load))
                if self.cpu_load > 0.3:
                    await self.notify()
           
    def get_current_cpu_usage(self):
        r = requests.get(self.cadvisor_url_cpu+"/"+self.docker_id)
        print("cpu_url = {}".format(self.cadvisor_url_cpu+"/"+self.docker_id))
        parsed_json = r.json()
        cpu_percentage = 0
        count = 0
        final_cpu  = parsed_json["stats"][-1:][0]["cpu"]["usage"]["total"]
        initial_cpu = parsed_json["stats"][-2:-1][0]["cpu"]["usage"]["total"]
        final_date = self.parse_datetime(parsed_json["stats"][-1:][0]["timestamp"])
        initial_date = self.parse_datetime(parsed_json["stats"][-2:-1][0]["timestamp"])
        cpu_percentage = self.get_current_cpu_percentage(initial_cpu = initial_cpu, final_cpu = final_cpu, initial_date =initial_date, final_date = final_date)    
        return cpu_percentage
    def get_current_cpu_percentage(self,initial_cpu, final_cpu, initial_date, final_date):
        date_delta = final_date - initial_date
        cpu_load = (final_cpu-initial_cpu)/(date_delta.total_seconds()* self.nano_secs)
        print("{} %".format(cpu_load))
        return cpu_load
   
    def parse_datetime(self, date):
        return maya.parse(date).datetime()
    
    def attach (self, observer) -> None:
        print("{} subject: attached to an observer".format(self.vnf_id))
        self._observers = observer
    
    def detach(self, observer) -> None:
        print("subject: remove  an observer")
        self._observers = None
    
    
    async def notify(self) -> None: 
        print("notifying....")
        await self._observers.updateCpuUsageSubject(self)
