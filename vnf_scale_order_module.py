import requests
import asyncio
import json 
import os
from utils.colors import bcolors 

class VnfScaleModule():
    ''' VNF Scale Docker module
    With this module you can scale up and down VNFs. The container names has the format: \n
    
    Identifier is composed by the first letter of vnf_id + ns_id and the number of the container \n
    mn._ scale _.{ns_id[-4:]}.{vnf_id[-4:]}.{identifier} \n


    '''
    
    volume_dic = {"small":1, "medium":2} #TODO  set default value.
    flavor_dic = {"single":" --cpus 1 --memory 256m ", "double":" --cpus 2 --memory 512m "}

    def scale_up_dockers(self, vnf_id, ns_id, volume, flavor):
        '''Scale dockers for a given vnf(and ns) with a custom flavor and number

        Parameters
        ----------
        vnf_id: str
            Vnf id given by osm
        ns_id: str
            Network slice id given by osm.
        flavor: str single, double
            The docker flavor you can choose between: single and double.
            with single you obtain a container with 1 cpu and 1gb of ram,
            with double you will get a container with 2 cpu and 2gb of ram.
        volume: str small, medium
            Number of dockers to deploy, small and medium are the choise \n
            choose small if you want to get 1 container \n
            choose medium if you want to get 2 containers \n
        CATCH
        ----------
        e
        '''
        counter = 0 
        image = "py_serv"
        try:
            for instance in range(self.volume_dic[volume]):
                identifier = "{}{}{}".format(flavor[0], volume[0], counter)
                docker_sentence = "docker run --name mn._scale_.{}.{}.{} {} -t -d {}".format(ns_id[-4:],vnf_id[-4:],identifier, self.flavor_dic[flavor], image)
                counter += 1
                self.exec_in_os(docker_sentence)
        except KeyError:
            self.custom_print("Key error, creating lowest scale  docker..") 
            identifier = "ss0"
            docker_sentence = "docker run --name mn._scale_.{}.{}.{} {} -t -d {}".format(ns_id[-4:],vnf_id[-4:],identifier,self.flavor_dic["single"], image)
            self.exec_in_os(docker_sentence)
    
    def scale_down_dockers(self,cadvisor_url , vnf_id, ns_id):
        docker_names = self.get_docker_names(cadvisor_url, ns_id, vnf_id)
        for docker in docker_names:
            docker_sentence = "docker container stop  {}".format(docker)
            self.exec_in_os(docker_sentence)
            docker_sentence = "docker container rm  {} ".format(docker)
            self.exec_in_os(docker_sentence)


    def get_docker_names(self, cadvisor_url, ns_id, vnf_id):
        #TODO working on this 
        r = requests.get(cadvisor_url)
        parsed_json = r.json()
        docker_names = []
        docker_name = "mn._scale_.{}.{}".format(ns_id[-4:], vnf_id[-4:])
        self.custom_print("searching for docker names like{}...".format(docker_name))

        for container in parsed_json:
            try:
                if docker_name in container["aliases"][0]:
                    self.custom_print("name found!")
                    self.custom_print(container["aliases"][0])
                    docker_names.append(container["aliases"][0])
            except KeyError:
                self.custom_print("key error: aliases")
        return docker_names
        
    def get_docker_scale_ips(self, cadvisor_url):
        print("getting docker scale ips")
        docker_ids = self.get_docker_ids(cadvisor_url)
        self.custom_print(docker_ids)
        docker_ips = []
        for docker in docker_ids:
            docker_ips.append(self.get_docker_ip(docker))
        return docker_ips
    
    def get_docker_ids(self, cadvisor_url):
        docker_name = "mn._scale_"
        r = requests.get(cadvisor_url)
        parsed_json = r.json()
        self.custom_print(docker_name)
        docker_ids = []
        for container in parsed_json:
            try:
                if docker_name in container["aliases"][0]:
                    self.custom_print("docker id found!")
                    docker_ids.append(container["aliases"][1])
            except KeyError:
                self.custom_print("key error: aliases")
        return docker_ids
    def get_docker_ip(self, id):
        result = os.popen("docker inspect -f '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' mn._scale_.b24f.fd25.ss0").read()
        return result.replace("\n","")


    def exec_in_os(self, command):
        '''Execute command in OS bash
        Parameters
        ----------
        command: str
            Command to execute.

        '''
        self.custom_print(command)
        os.system(command)           
        os.system("\n")

    def custom_print(self, message):
        print("{} ScaleModule:    {} {}".format( bcolors.WARNING, message, bcolors.ENDC))
        
#sl = VnfScaleModule()      
#sl.get_docker_scale_ips("http://34.67.105.37:8080/api/v1.3/subcontainers/docker")
#sl.scale_up_dockers("c630036f-174a-4892-afd7-0be46a637f05","d1bc4b47-eb56-4fb5-838a-ea0e5d137e68", "medium", "double") #,"medisum","double")
#sl.scale_down_dockers("http://34.69.148.248:8080/api/v1.3/subcontainers/docker","c630036f-174a-4892-afd7-0be46a637f05","d1bc4b47-eb56-4fb5-838a-ea0e5d137e68") #, "medium", "double") #,"medisum","double")

