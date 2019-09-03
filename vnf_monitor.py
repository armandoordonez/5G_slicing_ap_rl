import requests
import time

class RealTimeCpuUsage:

    def __init__(self, vnf_container_id):
        self.url = "http://localhost:8080/api/v2.0/ps/docker/"+vnf_container_id
        self.time_loop()
        
    def time_loop(self):
        while True:
            time.sleep(1)
            print("total_cpu: {}".format(self.get_current_cpu_usage()))
        
    def get_current_cpu_usage(self):
        r = requests.get(self.url)
        parsed_json = r.json()
        cpu_percentage = 0
        for element in parsed_json:
            print(element['percent_cpu'])
            cpu_percentage = cpu_percentage + float(element['percent_cpu'])    
        return cpu_percentage

if __name__ == "__main__":
    #URL = "http://34.94.156.190:8080/api/v2.0/ps/docker/c2e78487797fd69395f9378915bc6c37066245f8aa29f07a10aa339108a7635c"
    RealTimeCpuUsage("c2e78487797fd69395f9378915bc6c37066245f8aa29f07a10aa339108a7635c")
