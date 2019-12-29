import lib.wdb
import re, os, csv, sys, platform, subprocess
from shutil import move
from pathlib import Path
from lib.colorama import *
from lib.mac_vendor_lookup import MacLookup

mac = MacLookup()

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
    datawriter.writerow(['hostname','ip','mac','status','mask','vendor'])
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
                        vendor = mac.lookup(row[2])
                        if re.search(',',vendor):
                            vendor.replace(',','')
                        row[5] = vendor
                        datawriter.writerow(row)
                        count+=1
                    else:
                        is_up = True
                        print(row[0]+'-'+Fore.GREEN+'  Up'+Style.RESET_ALL)
                        row[3] = 'up'
                        vendor = mac.lookup(row[2])
                        if re.search(',',vendor):
                            vendor.replace(',','')
                        row[5] = vendor
                        datawriter.writerow(row)
                        count+=1

                else:

                    output = subprocess.Popen(["ping", ping_timeout,ping_timeout_count,ping_ammount,'1',row[1]], stdout = subprocess.PIPE).communicate()[0]
                    spaces=''
                    spaces_needed = 15 -len(row[0])
                    for i in range(spaces_needed):
                        spaces+=' '

                    if re.search(r'0 received,',str(output)):
                        is_up = False
                        print(row[0]+spaces+'-'+Fore.RED+' Down'+Style.RESET_ALL+' - '+row[5])
                        row[3] = 'down'
                        vendor = mac.lookup(row[2])
                        if re.search(',',vendor):
                            vendor.replace(',','')
                        row[5] = vendor
                        datawriter.writerow(row)
                        count+=1
                    else:
                        is_up = True
                        row[3] = 'up'
                        vendor = mac.lookup(row[2])
                        if re.search(',',vendor):
                            vendor.replace(',','')
                        row[5] = vendor
                        print(row[0]+spaces+'-'+Fore.GREEN+'  Up'+Style.RESET_ALL+'  - '+row[5])
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


