import requests
import datetime
import time
import math
import maya
class CpuPercentage():
    def __init__(self):
        self.cadvisor_url_cpu = "http://35.237.110.251:8080/api/v1.0/containers/docker"
        self.docker_id = "94f747f6b7be592d051dd188d19a4b03fbc5acfbe2279fd0672a0d3788b4d6e6"
        self.nano_secs = math.pow(10, 9)
        self.make_cpu_request()
    
    def get_current_cpu_percentage(self,initial_cpu, final_cpu, initial_date, final_date):
        date_delta = final_date - initial_date
        cpu_load = (final_cpu-initial_cpu)/(date_delta.total_seconds()* self.nano_secs)
        print("{} %".format(cpu_load))
        return cpu_load
    def parse_datetime(self, date):
        return maya.parse(date).datetime()
    def make_cpu_request(self):
        r = requests.get(self.cadvisor_url_cpu+"/"+self.docker_id)
        #print(self.cadvisor_url_cpu+"/"+self.docker_id)
        parsed_json = r.json()
        cpu_percentage = 0
        count = 0
        final_cpu  = parsed_json["stats"][-1:][0]["cpu"]["usage"]["total"]
        initial_cpu = parsed_json["stats"][-2:-1][0]["cpu"]["usage"]["total"]
        final_date = self.parse_datetime(parsed_json["stats"][-1:][0]["timestamp"])
        initial_date = self.parse_datetime(parsed_json["stats"][-2:-1][0]["timestamp"])
        print(self.get_current_cpu_percentage(initial_cpu = initial_cpu, final_cpu = final_cpu, initial_date =initial_date, final_date = final_date))
        return cpu_percentage

if __name__ == "__main__":
    CpuPercentage()