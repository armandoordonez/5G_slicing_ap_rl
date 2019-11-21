import requests

class GetAll():
    def __init__(self):
        self.cadvisor_url = "http://35.239.70.153:8080/api/v1.3/subcontainers/docker"
        self.get_all_docker_id()


    def init_server_in_all_instances(self):
        r = requests.get(self.cadvisor_url)
        print(self.cadvisor_url)
        parsed_json = r.json()
        for container in parsed_json:
            try:            
                for alias in container["aliases"]:
                    if "mn"  in alias:
                        print(alias)
                        command = "docker exec -i "+alias+" nohup python3 /home/server.py > /home/server.log 2>&1&"
                        print(command)
                        os.system(command)           
                        os.system("\n")
            except KeyError as e:
                pass
                print("catch error:{}".format(e))
        
        del parsed_json
        

if __name__ == "__main__":
    GetAll()