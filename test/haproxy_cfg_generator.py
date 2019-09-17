"""
class my_class():
    def __init__(self, parameter_list):

"""
def appendIpsCFG(self, new_ips):
    with open("example.cfg", "a") as myfile:
        count = 0 
        for ip in new_ips:
            server_name = "my_server_" + str(count)
            parsed_ips = "    server {} {}:{} \n".format(server_name, ip, self["video_stream_port"])
            print(parsed_ips)
            myfile.write(parsed_ips)
            count += 1


if __name__ == "__main__":
    self = {
        "video_stream_port" : "7079"
    }
    print("hi")
    my_ips = ["231.12","342.32","32.32.12"]
    appendIpsCFG(self, my_ips)