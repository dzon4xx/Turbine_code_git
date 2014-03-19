import datetime
import time
import os
from copy import deepcopy

from __init__ import *

class Record():
    """Class used to export historical data to Nikitta database"""

    def __init__(self):
        pass 
                      
    def add_record(self, operating_devices):
        ### atrybut powinien byc dodawany tylko jesli nie ma juz takiego atrybutu. zrob jakies sprawdzanie 
        for device in operating_devices:         
            client.add_attr_and_set_value(device.history_dir, str(device.record_id), device.value  )
            device.record_id = device.record_id + 1

    def record(self, operating_devices):
        start = time.time()       
        while True:            
            if time.time()-start > sleep_time:                      
                self.add_record(operating_devices)
                start = time.time()

class History():
    """ Creates device history dir in Nikitta Database """

    def __init__(self, start_dir_list, operating_devices):
        
        self.history_dir, self.history_dir_list  = self.__get_datetime_dir(start_dir_list)
        #self.create_devices_history_dir(operating_devices)  

    def create_devices_history_dir(self, operating_devices):
        """Creates device.history_dir atribute which is path to device's history catalog """

        for device in operating_devices:
            point_dir   = client.add_get_subdir(self.history_dir, str(device.point) )
            device_dir  = client.add_get_subdir(point_dir, device.device_type )
            device.history_dir = device_dir

    def create_folder( self ):
        """Creates a folder where history data will be stored """

        History_folder_path = os.path.abspath('History')
        folder_date = self.history_dir_list[2]
        folder_time = self.history_dir_list[3].replace(":", "-")
        
        if not os.path.isdir( "\\".join( (History_folder_path, folder_date) ) ):
            os.makedirs("\\".join( (History_folder_path, folder_date) ) )
        if not os.path.isdir( "\\".join( (History_folder_path, folder_date, folder_time) ) ):
            os.makedirs( "\\".join( (History_folder_path, folder_date, folder_time) ) )
        
        folder_dir =  "\\".join( (History_folder_path, folder_date, folder_time) ) 
        return folder_dir

    def __get_datetime_dir(self, start_dir_list):

        start_dir       = client.get_dir(start_dir_list)

        today = self.current_datetime(time_option=False)
        now   = self.current_datetime(time_option=True)

        start_dir_list.append( today )
        today_dir_list  = deepcopy(start_dir_list)
        today_dir_list.append(now)
        now_dir_list    = deepcopy(today_dir_list)

        today_dir       = client.get_dir(today_dir_list)

        if today_dir is None:
            today_dir = client.add_get_subdir(start_dir, self.current_datetime(time_option=False))           
            #start_dir = start_dir_list.append(self.current_datetime(time_option=false))
            now_dir   = client.add_get_subdir(today_dir, self.current_datetime(time_option=True))
            client.add_attr_and_set_value(now_dir, "_sleep_time", sleep_time)

        else:
            now_dir         = client.get_dir(now_dir_list)
            
            if now_dir is None:
                now_dir   = client.add_get_subdir(today_dir, self.current_datetime(time_option=True))
                client.add_attr_and_set_value(now_dir, "_sleep_time", sleep_time)
                        
        return now_dir, now_dir_list

    def current_datetime(self, time_option):

        """if option = 1 return time, else return date """                       
        now = datetime.datetime.now()
        now = str(now)
        now = now.split(' ')
        date = now[0]
        time = now[1].split('.')
        time = time[0]

        if time_option:
            return time
        else:
            return date
      
class Export(History):

    def __init__(self, start_dir_list, operating_devices ):
        History.__init__(self, start_dir_list, operating_devices)
        
        pass
                
    def get_export_data(self, export_points_list ):
        """Get export data from Nikitta database """

        points_dirs = client.get_dir_subdirs_dirs( self.history_dir )
        sep = "\t"
        exp_points_dirs = []

        for point_dir in points_dirs:
            if point_dir.name() in export_points_list:                
                exp_points_dirs.append(point_dir)

        sub_header1 = ["Time"+sep]
        sub_header2 = [sep]
        data        = []
        for point_dir in exp_points_dirs:

            point_dir_subdirs = client.get_dir_subdirs_dirs( point_dir )
            sub_header1.append(point_dir.name()+sep*len(point_dir_subdirs))
            
            for device_dir in point_dir_subdirs:
                sub_header2.append(device_dir.name()+point_dir.name()+sep)
                values_list = client.get_dir_values(device_dir)
                data.append( values_list )

        data.insert(0, range(len(data[0])))  # inserting number of scans vector
        header = [sub_header1, sub_header2]

        return header, data
        
    def save_export_data(self, file_name, header, data):
     
        """Save export data in history file"""
        folder_dir = self.create_folder()  
        file_dir = '\\'.join( (folder_dir, file_name) )
        file = open( file_dir, 'w')
        sep = "\t"
                
        header_line  = "".join(header[0])
        devices_line = "".join(header[1])
        file.write(header_line+"\n")
        file.write(devices_line+"\n")

        num_of_lines    = range(len(data[0]))
        num_of_devices  = range(len(data))
        for line_num in data[0]:
            line = ""
            for device_type in num_of_devices:
                value = data[device_type][line_num]
                line = line + str(value) + sep
            file.write(line+"\n")

        file.close()