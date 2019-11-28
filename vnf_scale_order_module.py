import requests
import asyncio
import json 
import os
class VnfScaleModule():
    
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
        image = "vlc_server"
        try:
            for instance in range(self.volume_dic[volume]):
                identifier = "{}{}{}".format(flavor, volume, counter)
                docker_sentence = "docker run --name mn._scale_.{}.{}.{} {} -t -d {}".format(ns_id[-4:],vnf_id[-4:],identifier, self.flavor_dic[flavor], image)
                counter += 1
                #print(docker_sentence)
                self.exec_in_os(docker_sentence)
            print(self.volume_dic["small"]) 
        except KeyError:
            print("Key error, creating lowest scale  docker..") 
            identifier = "ss0"
            docker_sentence = "docker run --name mn._scale_.{}.{}.{} {} -t -d {}".format(ns_id[-4:],vnf_id[-4:],identifier,self.flavor_dic["single"], image)
            self.exec_in_os(docker_sentence)
    
    def scale_down_dockers(self, vnf_id, ns_id):
        for docker in range(self.volume_dic["medium"]):
            docker_sentence = "docker stop container mn._scale_.{}.{}.{} ".format(ns_id[-4:],vnf_id[-4:], docker)
            self.exec_in_os(docker_sentence)
            docker_sentence = "docker rm container mn._scale_.{}.{}.{} ".format(ns_id[-4:],vnf_id[-4:], docker)
            self.exec_in_os(docker_sentence)




    def exec_in_os(self, command):
        '''Execute command in OS bash
        Parameters
        ----------
        command: str
            Command to execute.

        '''
        print(command)
        os.system(command)           
        os.system("\n")


        
sl = VnfScaleModule()      
sl.scale_down_dockers("833306a5-411f-4d4a-bb80-d271cbdf71ff","833306a5-411f-4d4a-bb80-d271cbdf71ff") #,"medisum","double")

