import requests
import asyncio
import json 

class VnfScaleModule():
    volume_dic = {"small":1, "medium":2} #TODO  set default value.
    flavor_dic = {"single":" --cpu 1 --memory 256m ", "double":" --cpu 2 --memory 512m "}

    def scale_dockers(self, vnf_id, ns_id, volume, flavor):
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
        for instance in range(self.volume_dic[volume]):
            docker_sentence = "docker run --name mn._scale_.{}.{}.{} {} -t -d {}".format(ns_id[-4:],vnf_id[-4:],counter,self.flavor_dic[flavor], image)
            counter += 1
            print(docker_sentence)

        print(self.volume_dic["small"]) 

sl = VnfScaleModule()      
sl.scale_dockers("833306a5-411f-4d4a-bb80-d271cbdf71ff","833306a5-411f-4d4a-bb80-d271cbdf71ff","medium","double")

