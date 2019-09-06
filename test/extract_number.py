
def extract_vnf_number(self, docker_container_name):
    number = ""
    for indx, value in enumerate(docker_container_name):
        if value.isdigit() and len(docker_container_name)>indx+2:
            if "-" in docker_container_name[indx-2:indx+2]:
                number = number + docker_container_name[indx]

    return int(number)

if __name__ == "__main__":
    docker_container_name = "mn.dc1_ozuna-1-slice_hackfest_vnfd-VM-1"
    print(extract_vnf_number("", docker_container_name))