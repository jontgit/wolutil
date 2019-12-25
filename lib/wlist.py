import csv
import lib.wmsg
import re
import os, platform
from pathlib import Path
from lib.colorama import *
from lib.ASCII import *
import platform 
import sys

if platform.system().lower()=='windows':
    os.chdir(os.getcwd())
    directory = os.getcwd()
    slash = '\\'

else:
    os.chdir(os.path.dirname(sys.argv[0]))
    directory = Path().absolute()
    slash = '/'

csv_file = str(str(directory)+slash+'hosts.csv')



def print_title(options):
    line_1=[]
    line_2=[]
    line_3=[]

    line_1.append(line_d_r+line_h*5+line_h_d)
    line_2.append(line_v+'  #  '+line_v)
    line_3.append(line_v_r+line_h*5+line_v_h)

    count=0
    while count < len(options):
        if re.match(r'host',options[count]):
            line_1.append(line_h*18+line_h_d)
            line_2.append('     HOSTNAME     '+line_v)
            line_3.append(line_h*18+line_v_h)
            count+=1
        elif re.match(r'ip',options[count]):
            line_1.append(line_h*17+line_h_d)
            line_2.append('   IP ADDRESS    '+line_v)
            line_3.append(line_h*17+line_v_h)
            count+=1
        elif re.match(r'mac',options[count]):
            line_1.append(line_h*19+line_h_d)
            line_2.append('    MAC ADDRESS    '+line_v)
            line_3.append(line_h*19+line_v_h)
            count+=1
        elif re.match(r'mask',options[count]):
            line_1.append(line_h*5+line_h_d)
            line_2.append(' MSK '+line_v)
            line_3.append(line_h*5+line_v_h)
            count+=1
        elif re.match(r'status',options[count]):
            line_1.append(line_h*10+line_h_d)
            line_2.append('  STATUS  '+line_v)
            line_3.append(line_h*10+line_v_h)
            count+=1

    if count == len(options):
        line_1[count] = line_1[count][:-1]
        line_1.append(line_d_l)
    for count in range(len(line_1)):
        print(str(line_1[count]),end="")
    print()

    for count in range(len(line_2)):
        print(str(line_2[count]),end="")
    print()

    if count == len(options):
        line_3[count] = line_3[count][:-1]
        line_3.append(line_v_l)
    for count in range(len(line_3)):
        print(str(line_3[count]),end="")
    print()

def display_data(options):
    count=0
    dline=[]
    init()
    with open (csv_file) as data:
        data_reader = csv.reader(data)
        next(data_reader)
        total_rows = len(list(csv.reader(open(csv_file))))
        current_line=int(data_reader.line_num)
        for line in data_reader:
            line_num = str(current_line)

            if current_line < 10:

                if current_line % 2 == 1:
                    print(line_v+Style.DIM+'  '+str(line_num)+'  '+Style.RESET_ALL+line_v,end="")
                else:
                    print(line_v+'  '+str(line_num)+'  '+line_v,end="")

                current_line+=1

            elif current_line < 100:

                if current_line % 2 == 1:
                    print(line_v+Style.DIM+' '+str(line_num)+'  '+Style.RESET_ALL+line_v,end="")
                else:
                    print(line_v+' '+str(line_num)+'  '+line_v,end="")
                current_line+=1

            icount=0
            while icount < len(options):

                if re.match(r'host',options[icount]) or re.match(r'h',options[icount]):
                    host_len = len(line[0])
                    while host_len <= 17:
                        line[0] = str(line[0] + ' ')
                        host_len += 1
                        if host_len <= 17:
                            line[0] = str(' ' + line[0])
                            host_len += 1

                    if current_line % 2 == 1:
                            line[0] = str(line[0])

                    else:
                            line[0] = str(Style.DIM+line[0]+Style.RESET_ALL)

                    print(str(line[0]+line_v),end="")

                elif re.match(r'ip',options[icount]):
                    ip_len = len(line[1])
                    while ip_len <= 16:
                        line[1] = str(line[1] + ' ')
                        ip_len += 1
                        if ip_len <= 16:
                            line[1] = str(' '+line[1])
                            ip_len += 1
                    if current_line % 2 == 1:
                        line[1] = str(line[1])

                    else:
                        line[1] = str(Style.DIM+line[1]+Style.RESET_ALL)

                    print(str(line[1]+line_v),end="")

                elif re.match(r'mac',options[icount]):

                    if current_line % 2 == 1:
                        line[2] = str(' '+line[2]+' ')
                    else:
                        line[2] = str(' '+Style.DIM+line[2]+Style.RESET_ALL+' ')
                    print(str(line[2]+line_v),end="")

                elif re.match(r'mask',options[icount]):

                    if current_line % 2 ==1:
                        line[4] = str(' '+line[4]+' ')
                    else:
                        line[4] = str(' '+Style.DIM+line[4]+Style.RESET_ALL+' ')
                    print(str(line[4]+line_v),end="")

                elif re.match(r'status',options[icount]):

                    if line[3] == 'up':
                        line[3] = str(Fore.GREEN+"    "+line[3]+Style.RESET_ALL+'    ')

                    else:
                        line[3] = str(Fore.RED+"   "+line[3]+Style.RESET_ALL+'   ')

                    print(str(line[3]+line_v),end="")

                else:
                    lib.wmsg.invalid_op(options[icount])
                icount+=1
 
            print()
            if count  == 1:
                print('No entries!')
                exit()
        count+=1

def print_last_line(options):
    count=0
    line_final=[]
    line_final.append(line_u_r+line_h*5+line_h_u)
    print(line_final[0],end="")
    while count < len(options):

        if re.search(r'ip',str(options[count])):
            line_final.append(line_h*17+line_h_u)

        elif re.search(r'host',str(options[count])):
            line_final.append(line_h*18+line_h_u)

        elif re.search(r'mac',str(options[count])):
            line_final.append(line_h*19+line_h_u)

        elif re.search(r'mask',str(options[count])):
            line_final.append(line_h*5+line_h_u)

        elif re.search(r'status',str(options[count])):
            line_final.append(line_h*10+line_h_u)

        if count == len(options)-1:
            line_final[count+1] = line_final[count+1][:-1]
            line_final[count+1] = line_final[count+1]+line_u_l
        count+=1
        print(line_final[count],end="")
    print()

def print_data_t(debug_level,options):
    if len(options) == 0:
        options=['host','ip','status']

    if debug_level == 0:
        print_title(options)
        display_data(options)
        print_last_line(options)

    else:
        lib.wmsg.list_print()

