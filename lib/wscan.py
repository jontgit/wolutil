import os, csv, sys, platform, re
from pathlib import Path
import wvarcheck


if platform.system().lower()=='windows':
    os.chdir(os.getcwd())
    directory = os.getcwd()
    slash = '\\'
else:
    os.chdir(os.path.dirname(sys.argv[0]))
    directory = Path().absolute()
    slash = '/'

tmp_arptable = str(str(directory)+slash+'arptable.tmp')

def arp_scan():
    os.system('sudo arp -a >> ./arptable.tmp')
    with open(tmp_arptable) as arp_data:
        arpreader = csv.reader(arp_data)
        for line in arpreader:
            line = str(line).split(' ')
            #for entry in line:
            count = 0 
            while count < len(line)-1:
                if re.search('(|)',line[count]):
                    line[count] = line[count].replace('(','')
                    line[count] = line[count].replace(')','')
                if wvarcheck.identify(line[count]) == 'IP':
                    print('IP Address:'+str(line[count]))
                count+=1
            #print(line)


arp_scan()
