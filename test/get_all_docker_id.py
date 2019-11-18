import requests

class GetAll():
    def __init__(self):
        self.cadvisor_url = "http://35.239.70.153:8080/api/v1.3/subcontainers/docker"
        self.get_all_docker_id()


    def get_all_docker_id(self):
        r = requests.get(self.cadvisor_url)
        print(self.cadvisor_url)
        parsed_json = r.json()
        #counter = 0 
        for container in parsed_json:
            try:            
                for alias in container["aliases"]:
                    """
                    if self.ns_name in alias :                       
                        if self.extract_vnf_number(container["aliases"][0]) is self.member_index and (container["aliases"][0][-1:] is "1"):
                            self.docker_id = container["aliases"][1]
                            self.docker_name  = container["aliases"][0]
                            print(container["aliases"])
                            print(container["aliases"][0][-1:])
                        #todo implement mapping between docker_id, docker_name, vnfd, ns
                    """
                    print(alias)
            except KeyError as e:
                pass
                print("catch error:{}".format(e))
        
        del parsed_json
        

if __name__ == "__main__":
    GetAll()