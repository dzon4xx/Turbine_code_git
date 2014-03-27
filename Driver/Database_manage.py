import datetime
import time

from Settings import *

class Database_manager():

    time = None
    date = None

    def __init__(self):
       
        self.points_list = [] 
        self.names_dict = {}

    def create_tree(self):

        def get_timestamp():
            """if option = 1 return time, else return date """                       
            now = datetime.datetime.now()
            now = str(now)
            date, time = now.split(' ')
            time = time.split('.')[0]
            return date, time
        
        def all_points_tree():

            def point_tree(point_number):

                def attr_value():
                    value_dict = {}
                    value_dict["value"] = 0.  # SPENT 1 HOUR ON MISTAKE HERE. VALUE MUST BE DOUBLE!!!!
                    return value_dict

                point_attr = {}
                for value_name in self.names_dict[point_number]:
                    point_attr[value_name] = attr_value()
                return point_attr

            points_dict = {}
            for point_number in self.points_list:
                points_dict['P'+str(point_number)] = point_tree(point_number)

            return points_dict

        main_interface_dir       = client.reset_subdir(client.get_dir(DB_PRESENT_DIR[:-1]), DB_PRESENT_DIR[-1])   
        history_interface_dir   =   client.get_dir(DB_HISTORY_DIR)

        points_dict = all_points_tree()
        client.create_tree(main_interface_dir, points_dict)
        Database_manager.date, Database_manager.time = get_timestamp()
        history_points_dict = {self.date: {self.time: points_dict}}
        client.create_tree(history_interface_dir, history_points_dict)
        pass

    def add_record(self, operating_devices):
        ### atrybut powinien byc dodawany tylko jesli nie ma juz takiego atrybutu. zrob jakies sprawdzanie 
        for device in operating_devices:         
            client.add_attr_and_set_value(device.history_dir, str(device.record_id), device.value  )
            device.record_id = device.record_id + 1

    def set_devices_history_dir(self, operating_devices):
        for device in operating_devices:
            device.history_dir  =   client.get_dir(DB_HISTORY_DIR + [Database_manager.date, Database_manager.time, device.point, device.name])

    def set_devices_present_dir(self, operating_devices):
        for device in operating_devices:
            device.dir   = client.get_dir(DB_PRESENT_DIR + [device.point, device.name])
            device.value = client.get_attr( device.dir, 'value' ) 

    def record(self, operating_devices):
        start = time.time()       
        while True:            
            if time.time()-start > sleep_time:                      
                self.add_record(operating_devices)
                start = time.time()








     
            
     