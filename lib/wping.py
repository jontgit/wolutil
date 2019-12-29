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
                    
                    subprocess.check_call(['ping',
                        ping_timeout,
                        ping_timeout_count,
                        ping_ammount, 
                        '1',
                        row[1]],stdout=DEVNULL,stderr=DEVNULL)
                
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


            
def ping(host):
    """
    Returns True if host (str) responds to a ping request.
    Remember that a host may not respond to a ping (ICMP) request even if the host name is valid.
    """

    # Option for the number of packets as a function of
    param = '-n' if platform.system().lower()=='windows' else '-c'

    # Building the command. Ex: "ping -c 1 google.com"
    command = ['ping', param, '1', host]
   

    with open(os.devnull, 'w') as DEVNULL:
        try:
            subprocess.check_call(
                ['ping', param, '1', host],
                stdout=DEVNULL,  # suppress output
                stderr=DEVNULL
            )
            is_up = True
            print(str(is_up))
        except subprocess.CalledProcessError:
            is_up = False
            print(str(is_ip))

'''
    try:
        response = subprocess.check_output(
            ['ping', '-c', '3', '192.168.0.1'],
            stderr=subprocess.STDOUT,  # get all output
            universal_newlines=True  # return string not bytes
        )
    except subprocess.CalledProcessError:
        response = None

'''

    #output = subprocess.check_output(command)# stdout=open(os.devnull, "w"), stderr=subprocess.STDOUT)

    #output = subprocess.Popen(command,stdout=subprocess.PIPE)#, shell=True, preexec_fn=os.setsid)
    
    #output.poll()

    #output = subprocess.run(command, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL); print('finished')

#    if re.search('0',str(output)):
#        print('True')
#    else:
#        print('False')
