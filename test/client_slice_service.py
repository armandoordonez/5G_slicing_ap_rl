import json, request, asyncio
class ClientService():
    def __init__(self, number_of_clients, request_per_client = 100):
        
        


export VIMEMU_HOSTNAME=$(sudo docker inspect -f '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' vim-emu)
osm vim-create --name emu-vim2 --user username --password password --auth_url http://$VIMEMU_HOSTNAME:6001/v2.0 --tenant tenantName --account_type openstack
