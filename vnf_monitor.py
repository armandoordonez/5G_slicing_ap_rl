import requests
import time
import argparse

class RealTimeCpuUsage:

    def __init__(self, BASE_URL):
        #self.url = "http://localhost:8080/api/v2.0/ps/docker/"+vnf_container_id
        self.base_url = BASE_URL
        self.get_docker_container_id_by_vnfid("id")
        #self.url = ""
        #self.time_loop()
    
    def get_docker_container_id_by_vnfid(self, vnf_id):
        r = requests.get(self.base_url+"v1.3/subcontainers/docker")
        parsed_json = r.json()
        print(len(parsed_json))
        
        counter = 0 
        for container in parsed_json:
            #print(container)           
            counter +=1 
            try:            
                for alias in container["aliases"]:
                    if "mn" in alias:
                        print(container["aliases"])
                        #todo implement mapping between docker_id, docker_name, vnfd, ns
            except KeyError as e:
                print("catch error: {}".format(e))
        
        del parsed_json

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
    parser = argparse.ArgumentParser(description='Arguments to work with')
    parser.add_argument('--dst_ip',default="localhost",help='destination ip')
    parser.add_argument('--docker_container', help='docker container')
    args = parser.parse_args()
    BASE_URL = "http://"+args.dst_ip+":8080/api/" # v2.0/ps/docker/"+args.docker_container
    RealTimeCpuUsage(BASE_URL)

#http://35.225.4.31:8080/api/v1.3/subcontainers get from here, get id by name and delete the json.