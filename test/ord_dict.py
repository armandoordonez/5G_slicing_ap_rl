from collections import OrderedDict
class OrdDict():
    volume_dic = OrderedDict()
    volume_dic = {"small":1, "medium":2, "extra":3} #TODO  set default value.
    flavor_dic = OrderedDict()
    flavor_dic = {"single":" --cpus 1 --memory 256m ", "double":" --cpus 2 --memory 512m "}

    def print_next_volume_dict(self, current_volume):
        print(self.get_next_value(current_volume))
    
    def print_previous_volume_dict(self, current_volume):
        print(self.get_previous_value(current_volume))


    def get_next_value(self, current_val):
        keys = self.volume_dic.keys()
        key_len = len(keys) - 1 
        counter = 0
        next_val = False
        
        for key in keys:
            if next_val is True:
                return key
            if key is current_val:
                next_val = True
                if counter is key_len:
                    return key
            counter += 1

    def get_previous_value(self, current_val):
        keys = self.volume_dic.keys()
        for key in keys:
            if key is current_val:
                return key


    def get_neighbors_values(self, current_val):
        '''
        return previous value and next value.
        '''
        keys = list(self.volume_dic.keys())
        index = list(self.volume_dic).index(current_val)
        if index < len(keys) and index != 0:
            return keys[index-1], keys[index+1]
        else:
            return keys[index], keys[index]
    
    def _get_next_value(self, current_val):
        keys = list(self.volume_dic.keys())
        index = list(self.volume_dic).index(current_val)
        if index < (len(keys)-1):
            return keys[index+1]
        else:
            return keys[index]

    def _get_previous_value(self, current_val):
        keys = list(self.volume_dic.keys())
        index = list(self.volume_dic).index(current_val)
        if index != 0:
            return keys[index-1]
        else:
            return keys[index]

if __name__ == "__main__":
    odict = OrdDict()
    current_volume = ["extra","small", "small", "medium", "extra", "extra"]
    expected_output = ["medium", "medium", "medium", "extra", "extra", "extra"]
    
    for current in current_volume:
        #previous_index, next_value = odict.get_neighbors_values(current)
        #print(previous_index, next_value)
        previous_val = odict._get_previous_value(current)
        print(previous_val)


