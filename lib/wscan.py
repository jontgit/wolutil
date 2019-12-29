import os, csv, sys, platform, re, time
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

network_ids=[]
last_addresses=[]
first_addresses=[]
host_groups=[]
net_ips=[]

def network_id_lookup(passed_vars):

    usr_input = passed_vars.split('/')
    mask = int(usr_input[1])
    in_ip = usr_input[0]
    host_bits = 32 - int(mask)
    hosts = pow(2,int(host_bits))
    valid_input = True

    private_address = False
    possible_net_id=['0','0','0','0']
    first_address=['0','0','0','0']
    last_address=['0','0','0','0']
    host_count = 0
    split_address = in_ip.split('.')

    if split_address[0] == '10':
        private_address = True
    elif split_address[0] in ['172'] and int(split_address[1]) in range(16,32):
        private_address = True
    elif split_address[0] in ['192'] and split_address[1] in ['168']:
        private_address = True

    if private_address == False:
        print('Error: Unable to send ICMP requests to external hosts.')
        print('\n  ### Please do not abuse this script. ###\n')
        exit()

    if hosts == 1:
        div = hosts
        print('Single host')
        possible_net_id = split_address

    elif hosts == 2:
        div = hosts
        print('Point to Point connection')
        possible_net_id[3] = split_address[3]
        possible_net_id[2] = split_address[2]
        possible_net_id[1] = split_address[1]
        possible_net_id[0] = split_address[0]

    elif hosts <= 256:
        print('Endpoints: '+str(hosts-2))
        if hosts == 256:
            div=int(hosts-1)
        elif hosts == 2:
            div=int(hosts+2)
        else:
            div=int(hosts)
        while host_count <= 256:
            if host_count > int(split_address[3]):
                possible_net_id[3] = str(host_count-hosts)
                possible_net_id[2] = split_address[2]
                possible_net_id[1] = split_address[1]
                possible_net_id[0] = split_address[0]
                break
            else:
                host_count+=hosts


    elif hosts > 256 and hosts < 65536:
        div=int(hosts/256)
        print('Endpoints: '+str(hosts-2))
        while host_count <= 65536:
            int_metric = int(host_count/256)
            if int_metric > int(split_address[2]):
                possible_net_id[2] = str(int(int_metric-div))
                possible_net_id[1] = split_address[1]
                possible_net_id[0] = split_address[0]
                break
            host_count+=hosts 


    elif hosts >= 65536 and hosts < 16777216:
        div=int(hosts/int(256*256))
        print('Endpoints: '+str(hosts-2))
        while host_count <= 16777216:
            int_metric = int(host_count/int(256*256))
            if int_metric > int(split_address[1]):
                possible_net_id[1] = str(int(int_metric-div))
                possible_net_id[0] = split_address[0]
                break
            host_count+=hosts


    elif hosts >= 16777216:
        div=int(hosts/int(256*256*256))
        print('Endpoints: '+str(hosts-2))
        while host_count <= 4294967296:
            int_metric = int(host_count/int(256*256*256))
            if int_metric > int(split_address[0]):
                possible_net_id[0] = str(int(int_metric-div))
                break
            host_count+=hosts
       # octet+=1


    if hosts <= 256:
        count = 1
    elif hosts > 256 and hosts < 65536:
        count = 2
    elif hosts >= 65536 and hosts < 16777216:
        count = 3
    elif hosts >= 16777216:
        count = 4

    dot = '.'
    network_id = dot.join(possible_net_id)
    print('Network ID: '+network_id+'/'+str(mask))
    network_ids.append(network_id+'/'+str(mask))

    first_address = network_id.split('.')
    if hosts >= 4:
        first_address[3] = str(int(first_address[3])+1)
    print('First Address: '+dot.join(first_address))
    first_addresses.append(dot.join(first_address))

    last_address = network_id.split('.')

    if hosts == 4:
        div-=1
    if count == 1:
        last_address[3] = str(int(last_address[3])+div-1)
    elif count == 2:
        last_address[3] = str(254)
        last_address[2] = str(int(last_address[2])+div-1)
    elif count == 3:
        last_address[3] = str(254)
        last_address[2] = str(255)
        last_address[1] = str(int(last_address[1])+div-1)
    elif count == 4:
        last_address[3] = str(254)
        last_address[2] = str(255)
        last_address[1] = str(255)
        last_address[0] = str(int(last_address[0])+div-1)
    else:
        print('Error, host_count out of range.')
    last_addresses.append(dot.join(last_address))
    print('Last Address: '+dot.join(last_address))
    host_groups.append(hosts)
    print()

def arp_lookup():
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

def ping_sweep():
    count = len(network_ids)
    for i in range(count):
        net_ip = network_ids[i].split('/')
        net_ips.append(net_ip[0])
    dot = '.'
    count = 0
    start_time = time.time()
    for entry in host_groups:
        print('You are about to ping '+str(host_groups[count]-2)+' hosts.')
        if get_confirmation() == True:
            os.system('setterm -cursor off')
            current_ip = net_ips[count].split('.')
            print()
            if int(host_groups[count]) == 1:
                print('   '+str(current_ip))

            elif int(host_groups[count]) == 2:
                for t_ip in range(host_groups[count]):
                    current_ip[3] = str(int(current_ip[3])+t_ip)
                    
                    print('   '+str(dot.join(current_ip)+' - '+t_ip+1), end='\r')
                    
            elif int(host_groups[count]) < 256:
                for t_ip in range(host_groups[count]-1):
                    current_ip[3] = str(int(current_ip[3])+1)
                    
                    print('   '+str(dot.join(current_ip))+' - '+str(t_ip+1), end='\r')
                    
                    if current_ip[3] == '255':
                        current_ip[2] = str(int(current_ip[2])+1)
                        current_ip[3] = '-1'
                    if current_ip[2] == '255':
                        current_ip[1] = str(int(current_ip[1])+1)
                        current_ip[2] = '-1'
 
            elif int(host_groups[count]) in [4, 256, 65536, 16777216]:
                for t_ip in range(host_groups[count]-2):
                    current_ip[3] = str(int(current_ip[3])+1)
                    
                    spaces=''
                    ip_len = len(dot.join(current_ip))
                    while ip_len <= 15:
                        spaces+=' '
                        ip_len+=1

                    print('   '+str(dot.join(current_ip))+spaces+str(t_ip+1), end='\r')
                    
                    if current_ip[3] == '255':
                        current_ip[2] =  str(int(current_ip[2])+1)
                        current_ip[3] = '-1'
                    if int(current_ip[2]) == 256:
                        current_ip[1] = str(int(current_ip[1])+1)
                        current_ip[2] = '0'
                        current_ip[3] = '-1'
                    if int(current_ip[1]) == 256:
                        current_ip[0] = str(int(current_ip[1])+1)
                        current_ip[1] = '0'
                        current_ip[2] = '0'
                        current_ip[3] = '-1'
 
            else:
                for t_ip in range(host_groups[count]-2):
                    current_ip[3] = str(int(current_ip[3])+1)
                    
                    print('   '+str(dot.join(current_ip))+' - '+str(t_ip+1), end='\r')

                    if current_ip[3] == '255':
                        current_ip[2] =  str(int(current_ip[2])+1)
                        current_ip[3] = '-1'
                    if int(current_ip[2]) == 256:
                        current_ip[1] = str(int(current_ip[1])+1)
                        current_ip[2] = '0'
                        current_ip[3] = '-1'
                    if int(current_ip[1]) == 256:
                        current_ip[0] = str(int(current_ip[1])+1)
                        current_ip[1] = '0'
                        current_ip[2] = '0'
                        current_ip[3] = '-1'
            print('\n\nFinished! Queried '+str(host_groups[count]-2)+' Addresses.')
            print("     --- %s seconds ---" % str(round((time.time()-start_time), 3))+'\n')
            os.system('setterm -cursor on')

def get_valid_range():
    correct = False
    while correct == False:
        usr_in = input('Please enter an IP range: ')
        try:
            if lib.wvarcheck.identify(str(usr_in)) == 'IPMSK':
                correct = True
                break
        except:
            print('Error, invalid range.')
    
    return usr_in

def get_confirmation():
    inp = False
    while inp == False:
        conf = input('Are you SURE you would like to proceed? ')
        if conf in ['Y','y','yes']:
            inp = True
            return inp
        elif conf in ['n','N','no']:
            print('Ping request cancelled.')
            inp = True
            exit()
        else:
            print('Please enter yes or no.')

def __main__(variables):
    count = 0
    print()

    if len(variables) == 0:
        variables.append(get_valid_range())

    for var in variables:
        network_id_lookup(variables[count])
        count+=1
    
    ping_sweep()
    arp_lookup()
    exit()
