from __init__ import *

class Turbine_tree_creator():

    def __init__(self):


        self.__main_interface_dir       = client.reset_subdir(client.get_dir(["Turbine"]), "Points")
        self.__history_interface_dir    = client.reset_subdir(client.get_dir(["Turbine", "History"]), "Points")

        self.points_list = [] 
        self.names_dict = {}

    def create_tree(self):

        points_dict = {}
        for point_number in self.points_list:
            points_dict['P'+str(point_number)] = self.point_tree(point_number)
        
        client.create_tree(self.__main_interface_dir, points_dict)
        client.create_tree(self.__history_interface_dir, points_dict)

    def point_tree(self, point_number):

        point_attr = {}
        for value_name in self.names_dict[point_number]:
            point_attr[value_name] = self.attr_value()

        return point_attr

    def attr_value(self):

        value_dict = {}
        value_dict["value"] = 0.  # SPENT 1 HOUR ON MISTAKE HERE. VALUE MUST BE DOUBLE!!!!
        return value_dict



     
            
     