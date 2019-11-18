import requests
import asyncio
import json 

class VnfScaleModule():
    def __init__(self, auth_token, base_url):
        self.auth_token = auth_token
        self.base_url = base_url
    
    def scale_instance(self, ns_id, scale_decision, member_index):
        url = self.base_url + "nslcm/v1/ns_instances/"+ns_id+"/scale"
        payload_str = {"scaleType": "SCALE_VNF","scaleVnfData":{"scaleVnfType": scale_decision,"scaleByStepData":{"scaling-group-descriptor": "scale_cirros","member-vnf-index": str(member_index)}}}
        payload =json.dumps(payload_str)
        print(payload)
        headers = {
            'Content-Type': "application/",
            'Authorization': "Bearer "+self.auth_token,
            'cache-control': "no-cache",
        }        
        response =  requests.request("POST", url, data=payload, headers=headers, verify=False)
        print(response.text)

    def init_all_docker_services(self):
        pass
    
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