import platform    # For getting the operating system name
import subprocess  # For executing a shell command
from shutil import move
import re, os, csv, sys, platform
from pathlib import Path
import lib.wdb


if platform.system().lower()=='windows':
    os.chdir(os.getcwd())
    directory = os.getcwd()
    slash = '\\'
    ping_ammount = '-n'
    ping_timeout = '-w'
    ping_timeout_count = '1'
else:
    os.chdir(os.path.dirname(sys.argv[0]))
    directory = Path().absolute()
    slash = '/'
    ping_ammount = '-c'
    ping_timeout = '-W'
    ping_timeout_count = '0.2'


csv_file = str(str(directory)+slash+'hosts.csv')
tmp_csv_file = str(str(directory)+slash+'hosts.tmp.csv')


def ping_all():

    data_len = lib.wdb.data_length(0)

    if data_len <= 1:
        print('Error: No host entries to check.')
        exit()

    count = 0

    data_write = open(tmp_csv_file,'w',newline='')
    datawriter = csv.writer(data_write)
    data_read = open(csv_file,'r')
    datareader = csv.reader(data_read)
    datawriter.writerow(['hostname','ip','mac','status','mask'])
    next(datareader)
    for row in datareader:
        with open(os.devnull, 'w') as DEVNULL:
            try:
                if platform.system().lower()=='windows':
                    output = subprocess.Popen(["ping.exe", ping_timeout,ping_timeout_count,ping_ammount,'1',row[1]], stdout = subprocess.PIPE).communicate()[0]

                    if re.search(r'100% loss',str(output)):
                        is_up = False
                        print(row[0]+': Down')
                        row[3] = 'down'
                        datawriter.writerow(row)
                        count+=1
                    else:
                        is_up = True
                        print(row[0]+': Up')
                        row[3] = 'up'
                        datawriter.writerow(row)
                        count+=1

                else:

                    output = subprocess.Popen(["ping", ping_timeout,ping_timeout_count,ping_ammount,'1',row[1]], stdout = subprocess.PIPE).communicate()[0]

                    if re.search(r'0 received,',str(output)):
                        is_up = False
                        print(row[0]+': Down')
                        row[3] = 'down'
                        datawriter.writerow(row)
                        count+=1
                    else:
                        is_up = True
                        print(row[0]+': Up')
                        row[3] = 'up'
                        datawriter.writerow(row)
                        count+=1

            except subprocess.CalledProcessError:
                is_up = False
                print(row[0]+': Down')
                row[3] = 'down'
                datawriter.writerow(row)
                count+=1

    data_read.close()
    data_write.close()
    move(tmp_csv_file,csv_file)


