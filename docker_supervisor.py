import requests
import time
from ObserverPattern.vnf_observer_pattern import VnfCpuSubject  as CpuSubject
import collections
import asyncio, maya, math
DockerInstance = collections.namedtuple('DockerInstance', ('name','docker_id','vnf_id','ns_id','index', 'sampling_time', 'volume', 'flavor')) 
#TODO hacer refactor con las constantes en unas sola clase.
#TODO hacer una maquina de estado
class DockerSupervisor(CpuSubject):
    _observers = None
    _state = None

    def __init__(self, cadvisor_url, ns_id, vnf_id, index, sampling_time, volume, flavor):
        identifier =  "{}{}{}".format(flavor[0], volume[0], 0)
        docker_name = "mn._scale_.{}.{}.{}".format(ns_id[-4:], vnf_id[-4:],identifier)
        #docker_name = "py_serv"
        self.cadvisor_url = cadvisor_url 
        self.cadvisor_url_cpu = cadvisor_url.replace("v1.3/subcontainers/docker", "v1.0/containers/docker")
        self.nano_secs = math.pow(10, 9)
        self.cpu_load = None
        self.rx_usage = None
        self.tx_usage = None
        self.c_tx = None
        self.c_rx = None
        docker_id = self.get_docker_id(docker_name)
        print(docker_id)
        self.docker_instance = DockerInstance(docker_name, docker_id, vnf_id[-4:], ns_id[-4:], index, sampling_time, volume, flavor)

    def get_docker_id(self, docker_name):
        cadvisor_url = self.cadvisor_url
        r = requests.get(cadvisor_url)
        parsed_json = r.json()
        print(docker_name)
        for container in parsed_json:
            try:
                if container["aliases"][0] == docker_name:
                    print("docker id found!")
                    return container["aliases"][1]
            except KeyError:
                print("key error: aliases")
        return "docker id not found!"



    async def check_docker_loop(self):
        print("check cpu loop..{}".format(self.docker_instance.name))
        try:
            while True:
                if self.docker_instance.docker_id is not None:
                    await asyncio.sleep(self.docker_instance.sampling_time)
                    self.cpu, self.rx_usage, self.tx_usage = self.get_current_usage_stats()
                    print("cpu load:{}% tx_usage: {}, rx_usage: {} name:{}".format(self.cpu, self.tx_usage, self.rx_usage, self.docker_instance.name))
                    await self.notify()
        except asyncio.CancelledError as e:
            print("Task cancelled!")


    def get_current_usage_stats(self):
        #print(self.cadvisor_url_cpu+"/"+self.docker_instance.docker_id)

        r = requests.get(self.cadvisor_url_cpu+"/"+self.docker_instance.docker_id)
        #print(self.cadvisor_url_cpu+"/"+self.docker_instance.docker_id)
        parsed_json = r.json()
        cpu_percentage = 0
        count = 0
        final_cpu  = parsed_json["stats"][-1:][0]["cpu"]["usage"]["total"]
        initial_cpu = parsed_json["stats"][-2:-1][0]["cpu"]["usage"]["total"]
        final_rx =  parsed_json["stats"][-1:][0]["network"]["rx_bytes"]
        final_tx =  parsed_json["stats"][-1:][0]["network"]["tx_bytes"]
        print(parsed_json["stats"][-2:-1][0]["network"]["rx_bytes"])
        final_date = self.parse_datetime(parsed_json["stats"][-1:][0]["timestamp"])
        initial_date = self.parse_datetime(parsed_json["stats"][-2:-1][0]["timestamp"])
        if self.c_rx == None:
            self.c_rx = final_rx
        if self.c_tx == None:
            self.c_tx = final_rx    
        rx_usage = final_rx - self.c_rx
        tx_usage = final_tx - self.c_tx
        self.c_rx = final_rx
        self.c_tx = final_tx
        print("initial rx {} final rx {} ".format(self.c_rx, final_rx))
        cpu_percentage = self.calculate_cpu_percentage(initial_cpu = initial_cpu, final_cpu = final_cpu, initial_date =initial_date, final_date = final_date)    
        return cpu_percentage, rx_usage, tx_usage

    def calculate_cpu_percentage(self,initial_cpu, final_cpu, initial_date, final_date):
        date_delta = final_date - initial_date
        cpu_load = (final_cpu-initial_cpu)/(date_delta.total_seconds()* self.nano_secs)
        return cpu_load 

    def parse_datetime(self, date):
        return maya.parse(date).datetime()

    def attach(self, observer):
        print("{} subject: Attached to an observer".format(self.docker_instance.vnf_id[:5]))
        self._observers = observer
        
    
    def detach(self, detach):
        print("subject: Remove  an observer")
        self._observers = None
    
    async def notify(self):
        await self._observers.updateCpuUsageSubject(self)


#loop = asyncio.get_event_loop()
#loop.run_until_complete(insta.check_docker_loop())

#loop.close()
#print(insta.get_current_cpu_usage())
#insta.get_docker_names()