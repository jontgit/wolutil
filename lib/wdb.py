import csv
from shutil import move
import os, sys, platform
from pathlib import Path

if platform.system().lower()=='windows':
    os.chdir(os.getcwd())
    directory = os.getcwd()
    slash = '\\'
else:
    os.chdir(os.path.dirname(sys.argv[0]))
    directory = Path().absolute()
    slash = '/'

csv_file = str(str(directory)+slash+'hosts.csv')
tmp_csv_file = str(str(directory)+slash+'hosts.tmp.csv')

def change_status(line,status):

    with open(csv_file,'r') as data_read:
        datareader = csv.reader(data_read)
        for rows in datareader:
            print(str(rows[3]))
            with open (csv_file,'w') as data_write:
                datawriter = csv.writer(data_write)
                datawriter.writerow(rows)
             #       if count == line:
                #count+=1

def data_length(debug_level):
    with open (csv_file,'r') as data_read:
        datareader = csv.reader(data_read)
        data_len=sum(1 for entry in data_read)
        return data_len

def search(debug_level,variables):
    with open (csv_file, 'r') as data_read:
        datareader = csv.reader(data_read)
        count = 1
        for var in variables:
            if var in datareader:
                print('yes')

def append(debug_level,variables):
    with open (csv_file,'a',newline='') as data_write:
        datawriter = csv.writer(data_write)
        datawriter.writerow(variables)

def insert(debug_level,variables,line):

    if line != 0:
        with open(csv_file,'r') as data_read:
            datareader = list(csv.reader(data_read))
            datareader.insert(line, variables)
        with open (csv_file,'w') as data_write:
            datawriter = csv.writer(data_write)
            for lines in datareader:
                datawriter.writerow(lines)
    else:
        sys.exit()

def remove(debug_level,line):

    if line == 0:
        sys.exit()

    with open(csv_file,'r') as data_read:
        datareader = csv.reader(data_read)
        with open(tmp_csv_file,'w',newline='') as data_write:
            datawriter = csv.writer(data_write)
            count = 0

            for row in datareader:
                if count != line:
                    datawriter.writerow(row)
                    count += 1
                    #print('wrote '+str(count))
                else:
                    count += 1
            if count <= line:
                print('Error: '+str(line)+' out of range.')
    move(tmp_csv_file,csv_file)

def swap(debug_level,variables,line):
    print()


