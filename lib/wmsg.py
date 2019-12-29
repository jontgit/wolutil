MSG_banner="""
                 __      __   _
                 \ \    / /__| |
                  \ \/\/ / _ \ |__
                   \_/\_/\___/____|

                 WakeOnLan Utility
                   Version 0.7
                Created by:  JonT

      use --help or -h for a list of commands.
"""

MSG_help="""
Usage: wol [OPTION]... [VARIABLE]...
Wake hosts in stored in the local CSV file
Lists the host and status entries unless additional 
operators are supplied

Explicit commands are passed by using the '--' delimiter.
Implicit commands are passed by using the '-' delimiter.

Use "wol [Command] -h" for examples

Commands:

    Explicit    |   Implicit
                |
    --list      |      -l
    --add       |      -a
    --delete    |      -d
    --wake      |      -w
    --status    |      -s
    --scan      |      -p
"""
MSG_list_desc="""
-l, --list      
    
    Lists the current database that has
    been configured by the user. Additional
    operators can be passed withthe ':'
    delimiter to show certain information."""
MSG_list_examples="""
    --list:[List Operators]
    
    List Operators are: 
        :host   :h
        :mac    :m
        :ip     :i
        :mask   :b
        :status :s

    Examples:
    Implicit:   -l:h:m
    Explicit:   --list:host:mac

    Will list the hostname, followed by the MAC address

    Implicit:   -l:i:s:h
    Explicit:   --list:ip:status:host

    Lists the IP address, followed by status and hostname
"""
MSG_add_desc="""
-a, --add       

    Adds a new host to the host database. If no variables
    are provided with the command, the user will be promp-
    ted to confirm the details to append them to the host
    list. Host variables must be seperated by a space. IP
    address variables must contain a CIDR mask after the 
    address. If not enough variables are passed to add a
    full entry to the database, you will be prompted to
    input the neccesary remaining fields."""
MSG_add_examples="""
    --add [Hostname | IP Address | MAC Address | CIDR Mask ]

    Examples:
    Implicit:   -a Hostname1 192.168.0.25/24 FF:FF:FF:FF:FF:FF
                -a 10.0.0.1/24 10.0.0.2/24
                -a 10.0.0.0 host-name3 /22

    Explicit:   --add Host2 10.3.4.2/23 AA.BB.CC.DD.EE.FF.AA
                --add 10.0.0.1/24 10.0.0.2/24
                --add 10.1.41.254 FFFF:FFFF:FFFF
"""
MSG_delete_desc="""
-d, --delete    

    Removes the selected host from the database. 
    Device IDscan be passed as variables, or if 
    none are stated, you will be prompted for a 
    selection to delete."""
MSG_delete_examples="""
    --delete [Device ID]

    Examples:
    Implicit:   -d 3-4

    Explicit:   --delete 3 4
"""
MSG_wake_desc="""
-w, --wake      

    Wakes the target computer specified by the user. this
    works in a simliar way to the addition command, if no
    variables are passed by the user, the host list will
    print and they will be prompted to select a host by
    either a host ID, IP address, Hostname or MAC address.

    Multiple arguments can be passed to send multiple magic
    packets in one command. Any combination of the below
    variables may be referenced at once."""
MSG_wake_examples="""
    --wake [Device ID | Hostname | IP Address | MAC Address]

    Examples:
    Implicit:   -w 1 2 4-7
                -w hostname1 hostname2 10.1.1.1
                -w 2-3 hostname 8 ffff.aaaa.cccc

    Explicit:   --wake 1,4,8-9
                --wake 10.33.44.1 FF:FF:AA:AA:BB:BB
                --wake hostname2 3 4-5
"""

def print_h_list(desc):
    if desc == True:
        print(MSG_list_desc)
        print(MSG_list_examples)
    else:
        print(MSG_list_examples)

def print_h_del(desc):
    if desc == True:
        print(MSG_delete_desc)
        print(MSG_delete_examples)
    else:
        print(MSG_delete_examples)


def print_h_add(desc):
    if desc == True:
        print(MSG_add_desc)
        print(MSG_add_examples)
    else:
        print(MSG_add_examples)

def print_h_wake(desc):
    if desc == True:
        print(MSG_wake_desc)
        print(MSG_wake_examples)
    else:
        print(MSG_wake_examples)

def print_help():
    print(MSG_help)
    exit()

def print_banner():
    print(MSG_banner)
    exit()

MSG_ip_addr='IP Addresses: '
MSG_mac_addr='MAC Addresses: '
MSG_dev_ids='Device IDs: '
MSG_sub_msks='Subnet Masks: '
MSG_hst_nms='Host Names: '
def identified_vars(ip_addresses,mac_addresses,device_ids,subnet_masks,host_names):
    if len(host_names) != 0:
        print(MSG_hst_nms+str(host_names))
    if len(subnet_masks) != 0:
        print(MSG_sub_msks+str(subnet_masks))
    if len(ip_addresses) != 0:
        print(MSG_ip_addr+str(ip_addresses))
    if len(mac_addresses) != 0:
        print(MSG_mac_addr+str(mac_addresses))
    if len(device_ids) != 0:
        print(MSG_dev_ids+str(device_ids))

def debug_warn():
    print('Functionality disabled in debug mode.')

MSG_remove_var='Removing invalid variable...'
def remove_var():
    print(MSG_remove_var)

MSG_invalid_var='Invalid variable:  '
def invalid_var(variable):
    print(MSG_invalid_var+str(variable))

MSG_invalid_op='Invalid Operator:  '
def invalid_op(variable):
    print(MSG_invalid_var+str(variable))

MSG_found_host='Found Host name: '
def found_host(variable):
    print(MSG_found_host+str(variable))

MSG_found_ip='Found IP address:  '
def found_ip(variable):
    print(MSG_found_ip+str(variable))

MSG_found_mac='Found MAC address: '
def found_mac(variable):
    print(MSG_found_mac+str(variable))

MSG_found_id='Found Device ID:   '
def found_id(variable):
    print(MSG_found_id+str(variable))

MSG_found_range='Found Device Range: '
def found_range(variable):
    print(MSG_found_range+str(variable))

MSG_identify_var='Identifying variables...'
def identify_var():
    print(MSG_identify_var)

MSG_variables='Variables: '
def print_variables(variables):
    if len(variables)!=0:
        print(MSG_variables+str(variables))


MSG_request_input='\nRequesting user input...'

MSG_found_var='Found Variable: '
def found_variable(variable):
    print(MSG_found_var+variable)

MSG_checking_input='Checking provided input...'
def checking_input():
    print(MSG_checking_input)

MSG_debug_level='DEBUG LEVEL: '
def debug_level(debug_level):
    print(MSG_debug_level+str(debug_level))

MSG_command_check='Checking variables and commands...'
def checking_commands():
    print(MSG_command_check)





MSG_ex_found='Found explicit command: '
def found_explicit(command):
    print(MSG_ex_found+command)

MSG_im_found='Found implicit command: '
def found_implicit(command):
    print(MSG_im_found+command)


MSG_ex_commands='Explicit commands: '
MSG_im_commands='Implicit commands: '
MSG_list_operators='List operators: '
def print_commands(explicit_commands,implicit_commands,list_operators):
    if len(explicit_commands) != 0:
        print(MSG_ex_commands+str(explicit_commands))
    if len(implicit_commands) != 0:
        print(MSG_im_commands+str(implicit_commands))
    if len(list_operators) != 0:
        print(MSG_list_operators+str(list_operators))

MSG_invalid_c='Error: Invalid command entered: '
def invalid_command(command):
    print(MSG_invalid_c+str(command))

MSG_list_prior='Ignoring list request.'
def ignore_list_req():
    print(MSG_list_prior)


MSG_add_varsearch='\nSearching Variables for potential entries...'

MSG_request_input='Requesting user input...'

MSG_wake_host='\nLooking for provided Hosts...'
MSG_exwake_found='Found wake request at explicit command: '
def exwake_found(command, count):
    print(MSG_exwake_found+str(count+1)+MSG_wake_host)

MSG_imwake_found='Found wake request at implicit command: '
def imwake_found(command,count):
    print(MSG_imwake_found+str(count+1)+MSG_wake_host)

MSG_search_ip='Searching database for IP: '
def search_ip(ip_address):
    print(MSG_search_ip+ip_address)

MSG_search_mac='Searching database for MAC: '
def search_mac(mac_address):
    print(MSG_search_mac+mac_address)

MSG_search_dev='Searching database for ID: '
def search_dev(device_id):
    print(MSG_search_dev+device_id)

MSG_no_variable_sup='No variables supplied.'
def wake_input():
    print(MSG_no_variable_sup)
    print(MSG_request_input)

MSG_imadd_found='Found addition request at implicit command: '
def imadd_found(command,count):
    print(MSG_imadd_found+str(count+1))

MSG_exadd_found='Found addition request at explicit command: '
def exadd_found(command,count):
    print(MSG_exadd_found+str(count+1))

MSG_found_list_op='Found list operator: '
def found_list_op(operator):
    print(MSG_found_list_op+str(operator))

MSG_not_found=' not found.'
def not_found(variable):
    print(str(variable)+MSG_not_found)

MSG_list_print='Printing the host database...'
def list_print():
    print(MSG_list_print)
MSG_imlist_found='Found list request at implicit command: '
def imlist_found(command,count):
    print(MSG_imlist_found+str(count+1))

MSG_exlist_found='Found list request at explicit command: '
def exlist_found(command,count):
    print(MSG_exlist_found+str(count+1))
