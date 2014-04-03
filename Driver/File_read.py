import xlrd
import csv
import sys
from Settings import *

class File_handler():

    TXT = "txt"
    CSV = "csv"
    XLS = "xls"

    def __init__(self):
        pass

    def create_csv_files(self, files_names ):

        xls_path  = DEVICES_PATH + [DEVICES_DATA]
        path_list =  DEVICES_PATH     
        int_attributes = [ID, ENABLED, POINT, CHARACTERISTIC]

        wb = self.open_file(xls_path, File_handler.XLS, 'r')
        for sheet_index, file_name in enumerate(files_names):

            #sh = wb.sheet_by_index(file_name)
            sh = wb.sheet_by_name(file_name)                           
            f = self.open_file(path_list + [file_name], File_handler.CSV, 'wb')
            c = csv.writer(f)
            attributes  =   sh.row_values(0)
            int_cols    =   self.__get_int_cols_numbers(attributes, int_attributes)
            for r in range(0, sh.nrows):
                row = []
                if sh.cell_value(r, 0) == '#':
                    continue

                for col in range(0 , sh.ncols):
                    if col in int_cols:
                        try:
                            cell = int(sh.cell_value(r, col))
                        except ValueError:
                            cell = sh.cell_value(r, col)
                    else:
                        cell = sh.cell_value(r, col)
                    row.append(cell)
                c.writerow(row)
            f.close()
       
    def open_file(self, path_list, file_ext, mode):
        path = self.convert_list_to_path(path_list, file_ext)

        if file_ext == File_handler.TXT:            
                return open(path, mode)

        if file_ext == File_handler.XLS:            
            return xlrd.open_workbook(path)

        if file_ext == File_handler.CSV:           
            return open(path, mode)
                
    def convert_list_to_path(self, path_list, file_ext):
        path_list[-1]   =  ".".join([path_list[-1], file_ext]) 
        path = "\\".join(path_list)
        return path     

    def __get_int_cols_numbers(self, attributes, int_attributes):
        int_cols = []
        for num, attr in enumerate(attributes):
            if attr in int_attributes:
                int_cols.append(num)
        return int_cols

    def get_first_line(self, path_list):

        xls_path = self.convert_list_to_path(path_list, File_handler.XLS)
        with xlrd.open_workbook(xls_path) as wb:
            sh = wb.sheet_by_index(0)
            return sh.row_values(0)

    def save_launch_time(self, data):

        f = self.open_file(DEVICES_PATH + [LAUNCH_TIME], 'txt', 'a')
        f.write(','.join(data) + '\n')
        f.close()

    def read_last_launch_time(self, ):

        f = self.open_file(DEVICES_PATH + [LAUNCH_TIME], 'txt', 'r')
      
        line = f.readline()
        line_size = sys.getsizeof(line)
        
        f.seek(-line_size-1, 2)
        line = f.readline() # one line before end of file
        line = line.rstrip('\n')
        date, time = line.split(',')
        f.close()

        return date, time