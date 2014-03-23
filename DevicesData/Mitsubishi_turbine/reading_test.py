import csv
import xlrd

def save():
    with xlrd.open_workbook('devices_map.xls') as wb:
        sh = wb.sheet_by_index(0)  # or wb.sheet_by_name('name_of_the_sheet_here')
        with open('devices_map.csv', 'wb') as f:
            c = csv.writer(f)
            for r in range(sh.nrows):
                c.writerow(sh.row_values(r))

def read():

    with open('devices_map.csv', 'r') as f:
        for line in f:
            print line

save()
read()

