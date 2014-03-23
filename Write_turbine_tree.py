import datetime
from __init__ import *

class Turbine_tree_creator():

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

        main_interface_dir       = client.reset_subdir(client.get_dir(PRESENT_DIR[:-1]), PRESENT_DIR[-1])   
        history_interface_dir    = client.reset_subdir(client.get_dir(HISTORY_DIR[:-1]), HISTORY_DIR[-1]) 
        

        points_dict = all_points_tree()
        client.create_tree(main_interface_dir, points_dict)
        date, time = get_timestamp()
        history_points_dict = {date: {time: points_dict}}
        client.create_tree(history_interface_dir, history_points_dict)
        pass








     
            
     