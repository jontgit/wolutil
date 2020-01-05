import lib.wdb
from lib.ASCII import *
import re, os, csv, sys, platform, subprocess
from shutil import move
from pathlib import Path
from lib.colorama import *
import asyncio
from lib.core import *
from itertools import islice

CURSOR_UP_ONE = '\x1b[1A'
ERASE_LINE = '\x1b[2K'

        
if platform.system().lower()=='windows':
    os.chdir(os.getcwd())
    directory = os.getcwd()
    slash = '\\'


else:
    os.chdir(os.path.dirname(sys.argv[0]))
    directory = Path().absolute()
    slash = '/'



csv_file = str(str(directory)+slash+'hosts.csv')
tmp_csv_file = str(str(directory)+slash+'tmp'+slash+'hosts.tmp.csv')
oui_table = str(str(directory)+slash+'lib'+slash+'oui.txt')


def mac_lookup(mac):
    mac = mac.replace(':','')
    mac = mac.replace('-','')
    mac = mac[:6].upper()

    with open(oui_table,'r') as ouireader:
    
        count = len(list(csv.reader(open(oui_table))))
        while True:
            next_n_lines = list(islice(ouireader, 100))
            for line in next_n_lines:
                
                if re.search(str(mac),str(line)):
                    vendor = line.split(' ',1)
                    vendor = str(vendor[1].replace('\n',''))
                    return vendor
            
 
            if not next_n_lines:

                break
    
        """for line in ouireader:
            #print(line)
            try:
                if re.search(line,mac):
                    split_line = line.split(' ')
                    vendor = split_line[0]
                    return vendor
            except:
                continue
                #print('Error: OUI not found in lookup table.')
                #exit()"""

def ping(provided_ip,overwrite_in,last):

    status='DOWN'
    if overwrite_in == True:
        overwrite = "\r"
    else:
        overwrite = '\n'
    
    spaces=''
    spaces_needed = 14 - len(provided_ip)
    for i in range(spaces_needed):
        spaces+=' '
    #print('\n'+str(last))
    
    resp = lib.core.ping(provided_ip)
    if resp.ret_code == 0:
        print(spaces+provided_ip+'  '+line_v+Fore.GREEN+'   Up '+Style.RESET_ALL, end = '\n')
        status = 'UP'
    
    elif resp.ret_code == 1:
        print(spaces+provided_ip+'  '+line_v+Fore.RED+'  Down'+Style.RESET_ALL, end= overwrite)
    
    if last == True:
       print('           memes        ',end='\r')
       sys.stdout.write(ERASE_LINE)

        
    return status

def ping_all():
    init()

    data_len = lib.wdb.data_length(0)

    if data_len <= 1:
        print('Error: No host entries to check.')
        sys.exit()

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
        

        try:
            spaces=''
            spaces_needed = 15 - len(row[0])
            for i in range(spaces_needed):
                spaces+=' '

            resp = lib.core.ping(row[1])
            
            vendor = mac_lookup(row[2])
            row[5] = vendor
            
            if resp.ret_code == 0:
                print(spaces+row[0]+' '+line_v+' '+Fore.GREEN+'  Up  '+Style.RESET_ALL+' '+line_v+' '+row[5])
                row[3] = 'up'

            elif resp.ret_code == 1:
                print(spaces+row[0]+' '+line_v+' '+Fore.RED+' Down '+Style.RESET_ALL+' '+line_v+' '+row[5])
                row[3] = 'down'
                
            else:
                sys.exit()

                       
            datawriter.writerow(row)
        except subprocess.CalledProcessError:
            print('\nError in ping_all print.')
            #is_up = False
            #print(row[0]+': Down')
            #row[3] = 'down'
            #datawriter.writerow(row)
            #count+=1

    print()
    data_read.close()
    data_write.close()
    move(tmp_csv_file,csv_file)

