import datetime
import time
import File_read
from Settings import *

class Database_manager():

    time = None
    date = None

    def __init__(self):
       
        self.points_list = [] 
        self.names_dict = {}


    def create_tree(self):



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

        Database_manager.date, Database_manager.time = self.timestamp()
        history_points_dict = {self.date: {self.time: points_dict}}
        client.create_tree(history_interface_dir, history_points_dict)

        file_handler = File_read.File_handler()
        file_handler.save_launch_time((Database_manager.date, Database_manager.time))
        pass

    def timestamp(self):                   
        now = datetime.datetime.now()
        now = str(now)
        date, time = now.split(' ')
        time = time.split('.')[0]
        return date, time

    def add_record(self, operating_devices):
        ### atrybut powinien byc dodawany tylko jesli nie ma juz takiego atrybutu. zrob jakies sprawdzanie 
        for device in operating_devices:      
            client.set_value(device.history_dir, 'value', device.value )   
            #client.add_attr_and_set_value(device.history_dir, str(device.record_id), device.value  )
         
    def set_devices_history_dir(self, operating_devices):
        for device in operating_devices:
            device.history_dir  =   client.get_dir(DB_HISTORY_DIR + [Database_manager.date, Database_manager.time, device.point, device.name])

    def set_devices_initial_value(self, output_devices):

        file_handler = File_read.File_handler()
        date, time  =   file_handler.read_last_launch_time()
                
        for device in output_devices:
            last_launch_dir =   client.get_dir(DB_HISTORY_DIR + [date, time, device.point, device.name])
            attr = last_launch_dir.attrs()
            value = client.get_dir_values(last_launch_dir)                         
            device.value    =   value[0]
            client.set_value(device.dir, 'value', device.value )

    def set_devices_present_dir(self, operating_devices):
        for device in operating_devices:
            device.dir   = client.get_dir(DB_PRESENT_DIR + [device.point, device.name])

    def record(self, operating_devices):
        start = time.time()       
        while True:            
            if time.time()-start > sleep_time:                      
                self.add_record(operating_devices)
                start = time.time()








     
            
     