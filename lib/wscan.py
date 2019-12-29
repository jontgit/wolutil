import os, csv, sys, platform, re
from pathlib import Path
import lib.wvarcheck
from lib.mac_vendor_lookup import MacLookup

mac = MacLookup()


if platform.system().lower()=='windows':
    os.chdir(os.getcwd())
    directory = os.getcwd()
    slash = '\\'
else:
    os.chdir(os.path.dirname(sys.argv[0]))
    directory = Path().absolute()
    slash = '/'

tmp_arptable = str(str(directory)+slash+'arptable.tmp')

vendors=[]
ip_addresses=[]
mac_addresses=[]

def ping_sweep():

    valid_input = False
    while valid_input == False:
        try:
            usr_input = input('Please enter a network range: ')
            if lib.wvarcheck.identify(usr_input) == 'IPMSK':
                usr_input = usr_input.split('/')
                mask = int(usr_input[1])
                network_id = usr_input[0]
                host_bits = 32 - int(mask)
                hosts = pow(2,int(host_bits))
                print('Hosts: '+str(hosts-2))
                valid_input = True
        except:
                print('Error, incorrect host format. ')
                break

    #if hosts > 254:
    #    print('Warning: You are about to ping '+str(hosts)+' devices.')
    
    possible_net_ids=['0','0','0','0']
    host_count = 0
    split_address = network_id.split('.')
    
    #if hosts <= 256:

    #while octet <= 3:
    if hosts <= 256:
        while host_count <= 256:
            if host_count > int(split_address[3]):
                possible_net_ids[3] = str(host_count-hosts)
                possible_net_ids[2] = split_address[2]
                possible_net_ids[1] = split_address[1]
                possible_net_ids[0] = split_address[0]
                break
            else:
                host_count+=hosts
    elif hosts > 256 and hosts < 65536:
        div=int(hosts/256)
        while host_count <= 65536:
            int_metric = int(host_count/256)
            if int_metric > int(split_address[2]):
                possible_net_ids[2] = str(int(int_metric-div))
                possible_net_ids[1] = split_address[1]
                possible_net_ids[0] = split_address[0]
                break
            host_count+=hosts 
    elif hosts > 16777216 and hosts < 4295967296:
        div=int(hosts/int(256*256))
        while host_count <= 16777216:
            int_metric = int(host_count/int(256*256))
            if int_metric > int(split_address[1]):
                possible_net_ids[1] = str(int(int_metric-div))
                possible_net_ids[0] = split_address[0]
                break
            host_count+=hosts
    elif hosts > 4295967296:
        div=int(hosts/int(256*256*256))
        while host_count <= 4294967296:
            int_metric = int(host_count/int(256*256*256))
            if int_metric > int(split_address[0]):
                possible_net_ids[0] = str(int(int_metric-div))
                break
            host_count+=hosts
       # octet+=1


    if hosts < 256:
        octet = 3
    elif hosts > 256:
        octet = 2
    elif hosts > 65536:
        octet = 1
    else:
        octet = 0

    dot = '.'
    first_address = dot.join(possible_net_ids)
    network_id = dot.join(possible_net_ids)
    print('Network ID: '+network_id+'/'+str(mask))
    print()
    #print('First Address: '+first_address)




#    while octet <= 3:
#        if octet == 3:
#            for count in range(hosts):
#                first_add
#        elif octet == 2:
#        elif octet == 1:
#        elif octet == 0:



#
#    if hosts > 256:
#
#        while host_count <= 65536:
#            if host_count > int(split_address[2]):
#                possible_net_ids[0].append(host_count-hosts)
#                break
#            host_count+=hosts
#        print(possible_net_ids)


    mod_count = 1
    while mod_count < hosts:
        if mod_count % hosts != 0:
            mod_count +=1
        else:
            network_start = mod_count
            print('Found network ID: '+str(mod_count))
            mod_count+=1

    ping_count = 1
    while ping_count < hosts:
        current_host = int(possible_net_ids[0])+int(ping_count)
        split_address[3] = str(current_host)
        dot = '.'
        rejoined_address = dot.join(split_address)
        #print(rejoined_address)
        ping_count+=1

def arp_scan():
    ping_sweep()
    os.system('sudo arp -a >> ./arptable.tmp')
    with open(tmp_arptable) as arp_data:
        arpreader = csv.reader(arp_data)
        for line in arpreader:
            current_line=int(arpreader.line_num)
            line = str(line).split(' ')
            count = 0
            while count < len(line):
                if re.search('(|)',line[count]):
                    line[count] = line[count].replace('(','')
                    line[count] = line[count].replace(')','')
                if re.search('<incomplete>',line[count]):
                    del ip_addresses[-1:]
                if lib.wvarcheck.identify(line[count]) == 'MAC':
                    mac_addresses.append(line[count])
                    vendors.append(mac.lookup(line[count]))
                if lib.wvarcheck.identify(line[count]) == 'IP':
                    ip_addresses.append(line[count])
                count+=1
    count =0
    while count < len(ip_addresses):
        print(ip_addresses[count],
                mac_addresses[count],
                vendors[count])
        count+=1
    os.system('rm '+tmp_arptable)
    exit()
