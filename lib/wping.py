import lib.wdb
from lib.ASCII import *
import re, os, csv, sys, platform, subprocess
from shutil import move
from pathlib import Path
from lib.colorama import *
from lib.mac_vendor_lookup import MacLookup

CURSOR_UP_ONE = '\x1b[1A'
ERASE_LINE = '\x1b[2K'

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
    ping_timeout_count = '0.01'


csv_file = str(str(directory)+slash+'hosts.csv')
tmp_csv_file = str(str(directory)+slash+'hosts.tmp.csv')

def ping(provided_ip,overwrite_in):

    if overwrite_in == True:
        overwrite = "\n"
    else:
        overwrite = '\n'
    spaces=''
    spaces_needed = 15 - len(provided_ip)
    for i in range(spaces_needed):
        spaces+=' '

    if platform.system().lower()=='windows':
        output = subprocess.Popen(["ping.exe", ping_timeout,ping_timeout_count,ping_ammount,'1',provided_ip], stdout = subprocess.PIPE).communicate()[0]

        if re.search(r'100% loss',str(output)):
            print(spaces+provided_ip+' '+line_v+' '+Fore.RED+' Down'+Style.RESET_ALL)
            sys.stdout.write(ERASE_LINE)
        else:
            print(spaces+provided_ip+' '+line_v+' '+Fore.GREEN+'  Up'+Style.RESET_ALL)

    else:
        output = subprocess.Popen(["ping", ping_timeout,ping_timeout_count,ping_ammount,'1',provided_ip], stdout = subprocess.PIPE).communicate()[0]
        
        if re.search(r'0 received,',str(output)):
            print(spaces+provided_ip+' '+line_v+' '+Fore.RED+' Down'+Style.RESET_ALL, end='\r')
            #sys.stdout.write(CURSOR_UP_ONE)
            sys.stdout.write(ERASE_LINE)
        else:
            print(spaces+provided_ip+' '+line_v+' '+Fore.GREEN+'  Up '+Style.RESET_ALL, end=overwrite)

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
    print('\n       Hostname '+line_v+' Status '+line_v+' Vendor')
    print('      '+line_h*10+line_v_h+line_h*8+line_v_h+line_h*9)
    for row in datareader:
        with open(os.devnull, 'w') as DEVNULL:
            try:
                if platform.system().lower()=='windows':
                    output = subprocess.Popen(["ping.exe", ping_timeout,ping_timeout_count,ping_ammount,'1',row[1]], stdout = subprocess.PIPE).communicate()[0]

                    if re.search(r'100% loss',str(output)):
                        is_up = False
                        row[3] = 'down'
                        vendor = mac.lookup(row[2])
                        print(spaces+row[0]+' '+line_v+' '+Fore.RED+' Down '+Style.RESET_ALL+' '+line_v+' '+row[5])
                        if re.search(',',vendor):
                            vendor.replace(',','')
                        row[5] = vendor
                        datawriter.writerow(row)
                        count+=1
                    else:
                        is_up = True
                        row[3] = 'up'
                        vendor = mac.lookup(row[2])
                        print(spaces+row[0]+' '+line_v+' '+Fore.GREEN+'  Up  '+Style.RESET_ALL+' '+line_v+' '+row[5])
                        if re.search(',',vendor):
                            vendor.replace(',','')
                        row[5] = vendor
                        datawriter.writerow(row)
                        count+=1

                else:

                    output = subprocess.Popen(["ping", ping_timeout,ping_timeout_count,ping_ammount,'1',row[1]], stdout = subprocess.PIPE).communicate()[0]
                    spaces=''
                    spaces_needed = 15 - len(row[0])
                    for i in range(spaces_needed):
                        spaces+=' '

                    if re.search(r'0 received,',str(output)):
                        is_up = False
                        print(spaces+row[0]+' '+line_v+' '+Fore.RED+' Down '+Style.RESET_ALL+' '+line_v+' '+row[5])
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
                        print(spaces+row[0]+' '+line_v+' '+Fore.GREEN+'  Up  '+Style.RESET_ALL+' '+line_v+' '+row[5])
                        datawriter.writerow(row)
                        count+=1
            except subprocess.CalledProcessError:
                is_up = False
                print(row[0]+': Down')
                row[3] = 'down'
                datawriter.writerow(row)
                count+=1

    print()
    data_read.close()
    data_write.close()
    move(tmp_csv_file,csv_file)


