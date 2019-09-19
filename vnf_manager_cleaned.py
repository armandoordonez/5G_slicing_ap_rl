from vnf_ip_supervisor import VnfCpuSupervisor
import vnf_monitor as vnf_monitor
import requests
from yaml import load
import argparse
import urllib3
from ObserverPattern.vnf_observer_pattern import VnfObserver as Observer
from ObserverPattern.vnf_observer_pattern import VnfCpuSubject as CpuSubject
import asyncio
import websockets
import json
from vnf_scale_order_module import VnfScaleModule
import os


class VnfManager(Observer):
    def __init__(self, base_url, sdm_ip):
        self.TAG = "VnfManager"
        self.load_balancer_docker_id = "haproxy"
        self.haproxy_cfg_name = "haproxy.cfg"
        print(self.TAG,"init")
        print(self.TAG, "load balancer docker id: {}, cfg name: {}".format(self.load_balancer_docker_id, self.haproxy_cfg_name))
        self.start(base_url, sdm_ip)
    def print(self, TAG, string):
        print("class: {}, {}".format(TAG, string))
        
    def start(self, base_url, sdm_ip):
        cadvisor_url = base_url.replace("https", "http") + ":8080/api/"
        self.base_url = base_url+":9999/osm/"  # osm nbi api.
        auth_token = self.get_osm_authentication_token(base_url=self.base_url)
        self.print(self.TAG,auth_token)
        self.auth_token = auth_token

        self.vnf_scale_module_instance = VnfScaleModule(base_url = self.base_url, auth_token=auth_token)
        ns_id_list, ns_vnf_list = self.get_nsid_list(base_url=self.base_url, auth_token=auth_token)
        loop = asyncio.get_event_loop()
        asyncio.ensure_future(websockets.serve(
            self.server_function, "localhost", 8765))

        vnf_supervisor_instances = {}
        for key, ns in ns_vnf_list.items():
            for vnf in ns["vnf"]:
                self.print(self.TAG,"ns name:{}".format(ns["name"]))
                self.print(self.TAG,"vnf:{}".format(ns["vnf"][vnf]))
                self.update_ips(vnf_id = ns["vnf"][vnf])
                vnf_supervisor_instance = VnfCpuSupervisor(
                    cadvisor_url=cadvisor_url, base_url=self.base_url, auth_token=auth_token, vnf_id=ns["vnf"][vnf], ns_id=key, ns_name=ns["name"], member_index=vnf)
                vnf_supervisor_instance.attach(self)
                asyncio.ensure_future(vnf_supervisor_instance.check_ip_loop())
                vnf_supervisor_instances[ns["vnf"]
                                         [vnf]] = vnf_supervisor_instance

        pending = asyncio.Task.all_tasks()  # allow end the last task!
        loop.run_until_complete(asyncio.gather(*pending))
        for indx, instance in vnf_supervisor_instances.items():
            self.print(self.TAG,"docker_id: {} vnf_id: {} docker_name:{}".format(
                instance.docker_id, instance.vnf_id, instance.docker_name))
        loop.run_forever()

    async def server_function(self, websocket, path):
        scale_decision = await websocket.recv()
        
        scale_decision = json.loads(scale_decision)
        self.print(self.TAG,"scale decision: {} ".format(scale_decision["scale_decision"]))
        #self.vnf_scale_module_instance.scale_instance(
        #        scale_decision["vnf_id"], scale_decision["scale_decision"], scale_decision["member_index"])
        self.print(self.TAG,type(scale_decision["scale_decision"]))
            
        if scale_decision["scale_decision"] is 1:
            self.print(self.TAG,"scale up")
            self.vnf_scale_module_instance.scale_instance(
                    ns_id = scale_decision["ns_id"], scale_decision =  "SCALE_OUT", member_index = scale_decision["member_index"])   
            await asyncio.sleep(5)
            
            self.update_ips(scale_decision["vnf_id"])              
        elif scale_decision["scale_decision"] is 0:
            self.print(self.TAG,"scale down ")
            self.vnf_scale_module_instance.scale_instance(
                    ns_id = scale_decision["ns_id"], scale_decision =  "SCALE_IN", member_index = scale_decision["member_index"])                 
            await asyncio.sleep(5)
            self.update_ips(scale_decision["vnf_id"])     
    
    async def send_alert_to_sdm(self, message):
        async with websockets.connect("ws://localhost:8544") as websocket:
            await websocket.send(message)

    def get_osm_authentication_token(self, base_url):
        url = base_url + "admin/v1/tokens"
        payload = "------WebKitFormBoundary7MA4YWxkTrZu0gW\r\nContent-Disposition: form-data; name=\"username\"\r\n\r\nadmin\r\n------WebKitFormBoundary7MA4YWxkTrZu0gW\r\nContent-Disposition: form-data; name=\"password\"\r\n\r\nadmin\r\n------WebKitFormBoundary7MA4YWxkTrZu0gW--"
        headers = {
            'content-type': "multipart/form-data; boundary=----WebKitFormBoundary7MA4YWxkTrZu0gW",
            'cache-control': "no-cache",
        }

        print("getting auth token: {}".format(url))
        response = requests.request("POST", url, data=payload, headers=headers, verify=False)
        response_parsed = response.content.split()
        return response_parsed[2].decode("utf-8")
    
    #todo function to send to the client to update the ips of the vnfs
    # vnf_1 : [0:ip1,1:ip2....,(n-1):ipn]
    def update_ips(self, vnf_id):
        vnf_ips = self.get_current_ips(vnf_id)
        print(vnf_ips)
        only_vnf_ips = []
        for ips in vnf_ips.values():
            only_vnf_ips = ips
        self.update_loadbalancer_cfg(vnf_id, only_vnf_ips)
        self.copy_cfg_to_loadbalancer()
        self.restart_loadbalancer()
        return vnf_ips
    
    def restart_loadbalancer(self):
        restart_command = "docker restart {}".format(self.load_balancer_docker_id)
        print(restart_command)
        os.system(restart_command)

    def copy_cfg_to_loadbalancer(self):
        copy_command = "docker cp haproxy.cfg {}:/usr/local/etc/haproxy/haproxy.cfg".format(self.load_balancer_docker_id)
        print(copy_command)
        os.system(copy_command)

    def update_loadbalancer_cfg(self, vnf_id, vnf_ips):
        with open( self.haproxy_cfg_name, "a") as myfile:
            count = 0 
            # todo extract ips from array.
            print(vnf_ips)
            for ip in vnf_ips:
                print(ip)
                server_name = "my_server_" + str(vnf_id[:4])
                parsed_ips = "    server {} {}:{} \n".format(server_name, ip, "7079")
                print(parsed_ips)
                myfile.write(parsed_ips)
                count += 1
    def get_current_ips(self, vnf_id):
        url = self.base_url + "nslcm/v1/vnf_instances/"+vnf_id
        print("getting ips")
        payload = ""
        headers = {
            'Content-Type': "application/",
            'Authorization': "Bearer "+self.auth_token,
            'cache-control': "no-cache",
            }
        print(url)
        response = requests.request("GET", url, data=payload, headers=headers, verify=False)        
        current_ips = []           
        vnf_ips = {}
        response_in_yaml = load(response.text)       
        for element in response_in_yaml["vdur"]:
                current_ips.append(element["interfaces"][0]["ip-address"])                    
        vnf_ips[vnf_id] = current_ips
        print(vnf_ips)
        return vnf_ips

    def get_nsid_list(self, base_url, auth_token):
        ns_list = []
        ns_vnf_dict = {}
        url = base_url + "nslcm/v1/ns_instances"
        payload = ""
        self.print(self.TAG,url)
        headers = {
            'Content-Type': "application/",
            'Authorization': "Bearer " + auth_token,
            'cache-control': "no-cache",
        }
        response_in_yaml = load(requests.request(
            "GET", url, data=payload, headers=headers, verify=False).text)
        for ns in response_in_yaml:
            # self.print(self.TAG,ns["name"])
            ns_list.append(ns["id"])
            internal_dict = {}
            internal_dict["name"] = ns["name"]
            vnf_data = {}
            for index, vnf_list in enumerate(ns["constituent-vnfr-ref"]):
                # self.print(self.TAG,vnf_list)
                vnf_data[index] = vnf_list
            internal_dict["vnf"] = vnf_data
            ns_vnf_dict[ns["id"]] = internal_dict
        return ns_list, ns_vnf_dict

    
    async def updateCpuUsageSubject(self, subject: CpuSubject) -> None:
        message = {
            "cpu": subject.cpu_load,
            "docker_id": subject.docker_id,
            "vnf_id": subject.vnf_id,
            "member_index": subject.member_index,
            "ns_id": subject.ns_id
        }
        await self.send_alert_to_sdm(json.dumps(message))
        self.print(self.TAG,"reacted from docker_name: {}, cpu load: {}, ns_name: {}".format(
            subject.docker_name, subject.cpu_load, subject.ns_name))

    


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Arguments to work with")
    parser.add_argument('--dst_ip', default="localhost", help='destination ip')
    parser.add_argument('--sdm_ip', default="localhost",
                        help="scale decision module ip")
    args = parser.parse_args()
    main_url = "https://"+args.dst_ip
    print("base_url: {}".format(main_url))
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    VnfManager(base_url=main_url, sdm_ip="ws://localhost:8544")
