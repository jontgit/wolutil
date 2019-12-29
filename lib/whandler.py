import re
import configparser
import lib.wlist
import lib.wmsg
import lib.wvarcheck
import lib.wwake
import lib.wdb
import lib.wmod
import lib.wformac
import lib.wread
import lib.wping
import lib.wscan

ip_addresses=[]
subnet_masks=[]
mac_addresses=[]
host_names=[]
device_ids=[]
device_ranges=[]
list_operators=[]
addresses_and_masks=[]

'''
==============
COMMAND CHECKS
==============
'''

def check_commands(explicit_commands,implicit_commands,debug_level):
    list_first_print=True
    help_first_print=True
    #all_commands = str(explicit_commands.append(implicit_commands))
    #print(all_commands)
    #FIND HELP AND LIST COMMANDS BEFORE ANYTHING ELSE

    #HELP/LIST - EXPLICIT COMMANDS FIRST
    if debug_level > 0: print('Commands second...')
    count=0
    if debug_level > 1:
        lib.wmsg.debug_warn()
        lib.wmsg.print_commands(explicit_commands,implicit_commands,list_operators)

    while count < len(explicit_commands):
        if re.search(r'help',str(explicit_commands)) \
                or re.search(r'h',str(implicit_commands)) \
                and help_first_print == True:

            if re.search(r'help',str(explicit_commands)):
                help_level = True
            elif re.search(r'h',str(implicit_commands)):
                help_level = False

            list_first_print=False
            if re.search(r'list',str(explicit_commands)) \
                or re.search(r'l',str(implicit_commands)):
                lib.wmsg.print_h_list(help_level)
                help_first_print=False
            elif re.search(r'wake',str(explicit_commands)) \
                or re.search(r'w',str(implicit_commands)):
                lib.wmsg.print_h_wake(help_level)
                help_first_print=False
            elif re.search(r'delete',str(explicit_commands)) \
                or re.search(r'd',str(implicit_commands)):
                lib.wmsg.print_h_del(help_level)
                help_first_print=False
            elif re.search(r'add',str(explicit_commands)) \
                or re.search(r'a',str(implicit_commands)):
                lib.wmsg.print_h_add(help_level)
                help_first_print=False
            elif re.search(r'status',str(explicit_commands)) \
                or re.search(r's',str(implicit_commands)):
                lib.wmsg.print_h_scan(help_level)
                help_first_print=False
            elif re.search(r'ping',str(explicit_commands)) \
                or re.search(r'p',str(implicit_commands)):
                lib.wmsg.print_h_ping(help_level)
                help_first_print=False
            elif help_first_print==True:
                help_first_print=False
                lib.wmsg.print_help()
            exit()

        elif re.search(r'list',str(explicit_commands)) and list_first_print == True:
            list_first_print=False
            lib.wlist.print_data_t(debug_level,list_operators)

        count+=1

    #HELP/LIST - IMPLICIT COMMANDS SECOND

    count=0
    while count < len(implicit_commands):
        if re.search(r'help',str(explicit_commands)) \
                or re.search(r'h',str(implicit_commands)) \
                and help_first_print == True:

            if re.search(r'help',str(explicit_commands)):
                help_level = True
            elif re.search(r'h',str(implicit_commands)):
                help_level = False

            list_first_print=False
            if re.search(r'list',str(explicit_commands)) \
                or re.search(r'l',str(implicit_commands)):
                lib.wmsg.print_h_list(help_level)
                help_first_print=False
            elif re.search(r'wake',str(explicit_commands)) \
                or re.search(r'w',str(implicit_commands)):
                lib.wmsg.print_h_wake(help_level)
                help_first_print=False
            elif re.search(r'delete',str(explicit_commands)) \
                or re.search(r'd',str(implicit_commands)):
                lib.wmsg.print_h_del(help_level)
                help_first_print=False
            elif re.search(r'add',str(explicit_commands)) \
                or re.search(r'a',str(implicit_commands)):
                lib.wmsg.print_h_add(help_level)
                help_first_print=False
            elif re.search(r'status',str(explicit_commands)) \
                or re.search(r's',str(implicit_commands)):
                lib.wmsg.print_h_scan(help_level)
                help_first_print=False
            elif re.search(r'ping',str(explicit_commands)) \
                or re.search(r'p',str(implicit_commands)):
                lib.wmsg.print_h_ping(help_level)
                help_first_print=False
            elif help_first_print==True:
                help_first_print=False
                lib.wmsg.print_help()
            exit()





        if re.search(r'l',str(implicit_commands)) and list_first_print == True:
            list_first_print=False
            lib.wlist.print_data_t(debug_level,list_operators)

        count+=1

    #EXPLICIT COMMAND CHECKS

    count=0
    while count < len(explicit_commands):

        if re.search(r'list',str(explicit_commands[count])):
            if debug_level > 1:
                lib.wmsg.ignore_list_req()
            count+=1

        elif re.search(r'add',str(explicit_commands[count])):
            if debug_level > 0:
                lib.wmsg.exadd_found(explicit_commands[count],count)
            else:
                lib.wmod.addition(ip_addresses,mac_addresses,subnet_masks,host_names)
            count+=1
        
        elif re.search(r'status',explicit_commands[count]):
            if debug_level > 0:
                print('Found status request.')
            elif debug_level == 0:
                if len(ip_addresses) != 0:
                    lib.wping.ping(ip_addresses[count])
                else:
                    lib.wping.ping_all()
                count+=1

        elif re.search(r'scan',explicit_commands[count]):
            lib.wscan.__main__(addresses_and_masks)


        elif re.search(r'delete',explicit_commands[count]):
            if debug_level > 0:
                print('Found delete command.')
            elif debug_level == 0:
                input_vars=[]
                lib.wlist.print_data_t(debug_level,'')
                if len(device_ids) == 0 and len(device_ranges) == 0:
                    selection = int(input('Select an entry to delete: '))
                    total=int(lib.wdb.data_length(0))

                    if int(selection) > int(total):
                        print('Error: '+str(selection)+' Out of range.')
                        exit()

                    hostname=lib.wread.look_for_host(selection,'ID')
                    ipaddress=lib.wread.look_for_ip(selection,'ID')
                    macaddress=lib.wread.look_for_mac(selection,'ID')
                    print('\nDevice ID:  '+str(icount))
                    print('\nIP Address:  '+str(ipaddress))
                    print('MAC Address: '+str(macaddress))
                    print('Host Name:   '+str(hostname)+'\n')

                    confirmation = input('Are you sure you want to delete this?: ')
                    if confirmation in ["y","Y","yes","Yes","YES"]:
                        lib.wdb.remove(debug_level,selection)
                        print('Removed host from database.')
                        count+=1
                    elif confirmation in ["n", "N", "no","No","NO"]:
                        print('Deletion cancelled.')
                        count+=1


                elif len(device_ids) != 0:

                    for dev in device_ids:
                        total=int(lib.wdb.data_length(0))

                        if int(dev) > int(total):
                            print('Error: '+str(dev)+' Out of range.')
                            exit()

                        hostname=lib.wread.look_for_host(int(dev),'ID')
                        ipaddress=lib.wread.look_for_ip(int(dev),'ID')
                        macaddress=lib.wread.look_for_mac(int(dev),'ID')
                        print('\nDevice ID:  '+str(dev))
                        print('\nIP Address:  '+str(ipaddress))
                        print('MAC Address: '+str(macaddress))
                        print('Host Name:   '+str(hostname)+'\n')

                        confirmation = input('Are you sure you want to delete this?: ')
                        if confirmation in ["y","Y","yes","Yes","YES"]:
                            lib.wdb.remove(debug_level,int(dev))
                            print('Removed host from database.')
                            count+=1
                        elif confirmation in ["n", "N", "no","No","NO"]:
                            print('Deletion cancelled.')
                            count+=1

                elif len(device_ranges) != 0:
                    total=int(lib.wdb.data_length(0))
                    ranges = device_ranges[count].split('-')
                    start_count = int(ranges[0])
                    icount = start_count
                    end_count = int(ranges[1])

                    if start_count > total:
                        print('Error: '+str(start_count)+' out of range.')
                        exit()
                    if end_count > total:
                        print('Error: '+str(end_count)+' out of range.')
                        exit()
                    while icount < end_count+1:
                        hostname=lib.wread.look_for_host(start_count,'ID')
                        ipaddress=lib.wread.look_for_ip(start_count,'ID')
                        macaddress=lib.wread.look_for_mac(start_count,'ID')
                        print('\nDevice ID:   '+str(icount))
                        print('IP Address:  '+str(ipaddress))
                        print('MAC Address: '+str(macaddress))
                        print('Host Name:   '+str(hostname)+'\n')

                        confirmation = input('Are you sure you want to delete this?: ')
                        if confirmation in ["y","Y","yes","Yes","YES"]:
                            lib.wdb.remove(debug_level,start_count)
                            print('\nRemoved host from database.')
                            count+=1
                        elif confirmation in ["n", "N", "no","No","NO"]:
                            print('\nDeletion request aborted.')
                            start_count+=1
                        icount+=1
                    count+=1

        elif re.search(r'wake',str(explicit_commands[count])):
            if debug_level > 0:
                lib.wmsg.exwake_found(explicit_commands[count],count)
            if len(ip_addresses) + len(mac_addresses) + len(device_ids) + len(host_names) != 0:
                lib.wwake.wake(ip_addresses,mac_addresses,device_ids,host_names,debug_level)
            if len(device_ranges) != 0:
                rcount = 0
                total=int(lib.wdb.data_length(0))
                ranges = device_ranges[rcount].split('-')
                start_count = int(ranges[0])
                icount = start_count
                end_count = int(ranges[1])

                if start_count > total:
                    print('Error: '+str(start_count)+' out of range.')
                    exit()
                if end_count > total:
                    print('Error: '+str(end_count)+' out of range.')
                    exit()
                while icount < end_count+1:
                    device_ids.append(icount)
                    icount+=1

                lib.wwake.wake(ip_addresses,mac_addresses,device_ids,host_names,debug_level)

            if len(ip_addresses) + len(mac_addresses) + len(device_ids) + len(host_names) + len(device_ranges) == 0:
                lib.wlist.print_data_t(debug_level,'')
                if debug_level < 0:
                    lib.wmsg.wake_input()
                try:
                    variable=input('Please select a device: ')
                    if lib.wvarcheck.identify(variable) == 'IP':
                        ip_addresses.append(variable)
                    if lib.wvarcheck.identify(variable) == 'MAC':
                        mac_addresses.append(variable)
                    if lib.wvarcheck.identify(variable) == 'ID':
                        device_ids.append(variable)
                    if lib.wvarcheck.identify(variable) == 'HOST':
                        host_names.append(variable)
                    if len(host_names)+len(ip_addresses)+len(mac_addresses)+len(device_ids) != 0:
                        lib.wwake.wake(ip_addresses,mac_addresses,device_ids,host_names,debug_level)
                    else:
                        continue
                except:
                    print()
                    break


            count+=1

        else:
            lib.wmsg.invalid_command(explicit_commands[count])
            count+=1

    #IMPLICIT COMMAND CHECKS

    count=0
    while count < len(implicit_commands):


        if re.search(r'l',implicit_commands[count]) and list_first_print == False:
            if debug_level > 1:
                lib.wmsg.ignore_list_req()
            count+=1

        elif re.search(r'a',implicit_commands[count]):
            if debug_level > 0:
                lib.wmsg.imadd_found(implicit_commands[count],count)
            elif debug_level == 0:
                lib.wmod.addition(ip_addresses,mac_addresses,subnet_masks,host_names)
            count+=1

        elif re.search(r's',implicit_commands[count]):
            if debug_level > 0:
                print('Found status request.')
            elif debug_level == 0:
                if len(ip_addresses) != 0:
                    lib.wping.ping(ip_addresses[count])
                else:
                    lib.wping.ping_all()
                count+=1

        elif re.search(r'd',implicit_commands[count]):
            if debug_level > 0:
                print('Found delete command.')
                count+=1
            elif debug_level == 0:
                lib.wlist.print_data_t(debug_level,'')
                input_vars=[]
                if len(device_ids) == 0 and len(device_ranges) == 0:
                    selection = int(input('Select an entry to delete: '))
                    total=int(lib.wdb.data_length(0))

                    if int(selection) > int(total):
                        print('Error: '+str(selection)+' Out of range.')
                        exit()


                    hostname=lib.wread.look_for_host(selection,'ID')
                    ipaddress=lib.wread.look_for_ip(selection,'ID')
                    macaddress=lib.wread.look_for_mac(selection,'ID')
                    print('\nDevice ID:   '+str(icount))
                    print('IP Address: '+str(ipaddress))
                    print('MAC Address: '+str(macaddress))
                    print('Host Name: '+str(hostname)+'\n')

                    confirmation = input('Are you sure you want to delete this?: ')
                    if confirmation in ["y","Y","yes","Yes","YES"]:
                        lib.wdb.remove(debug_level,selection)
                        print('\nRemoved host from database.')
                        count+=1
                    elif confirmation in ["n", "N", "no","No","NO"]:
                        print('\nDeletion request aborted.')
                        count+=1


                elif len(device_ids) != 0:
                    for dev in device_ids:
                        total=int(lib.wdb.data_length(0))

                        if int(dev) > int(total):
                            print('error: '+str(dev)+' out of range.')
                            exit()

                        hostname=lib.wread.look_for_host(int(dev),'ID')
                        ipaddress=lib.wread.look_for_ip(int(dev),'ID')
                        macaddress=lib.wread.look_for_mac(int(dev),'ID')
                        print('\nDevice ID:   '+str(icount))
                        print('IP Address:  '+str(ipaddress))
                        print('MAC Address: '+str(macaddress))
                        print('Host Name:   '+str(hostname)+'\n')

                        confirmation = input('Are you sure you want to delete this?: ')
                        if confirmation in ["y","Y","yes","Yes","YES"]:
                            lib.wdb.remove(debug_level,int(dev))
                            print('Removed host from database.')
                            count+=1
                        elif confirmation in ["n", "N", "no","No","NO"]:
                            print('Aborted.')
                            count+=1

                elif len(device_ranges) != 0:
                    total=int(lib.wdb.data_length(0))
                    rcount = 0
                    ranges = device_ranges[rcount].split('-')
                    start_count = int(ranges[0])
                    icount = start_count
                    end_count = int(ranges[1])

                    if start_count > total:
                        print('Error: '+str(start_count)+' out of range.')
                        exit()
                    if end_count > total:
                        print('Error: '+str(end_count)+' out of range.')
                        exit()
                    while icount < end_count+1:
                        hostname=lib.wread.look_for_host(start_count,'ID')
                        ipaddress=lib.wread.look_for_ip(start_count,'ID')
                        macaddress=lib.wread.look_for_mac(start_count,'ID')
                        print('\nDevice ID:  '+str(icount))
                        print('IP Address:  '+str(ipaddress))
                        print('MAC Address: '+str(macaddress))
                        print('Host Name:   '+str(hostname)+'\n')

                        confirmation = input('Are you sure you want to delete this?: ')
                        if confirmation in ["y","Y","yes","Yes","YES"]:
                            lib.wdb.remove(debug_level,start_count)
                            print('Removed host from database.')
                            count+=1
                        elif confirmation in ["n", "N", "no","No","NO"]:
                            print('Aborted.')
                            start_count+=1
                        icount+=1

                else:
                    input_vars.append(ip_addresses)
                    input_vars.append(mac_addresses)
                    input_vars.append(subnet_masks)
                    input_vars.append(host_names)

                count+=1



        elif re.search(r'w',implicit_commands[count]):
            if debug_level > 0:
                lib.wmsg.imwake_found(implicit_commands[count],count)
            if len(ip_addresses) + len(mac_addresses) + len(device_ids)+len(host_names) != 0:
                lib.wwake.wake(ip_addresses,mac_addresses,device_ids,host_names,debug_level)

            if len(device_ranges) != 0:
                rcount = 0
                total=int(lib.wdb.data_length(0))
                ranges = device_ranges[rcount].split('-')
                start_count = int(ranges[0])
                icount = start_count
                end_count = int(ranges[1])

                if start_count > total:
                    print('Error: '+str(start_count)+' out of range.')
                    exit()
                if end_count > total:
                    print('Error: '+str(end_count)+' out of range.')
                    exit()
                while icount < end_count+1:
                    device_ids.append(icount)
                    icount+=1

                lib.wwake.wake(ip_addresses,mac_addresses,device_ids,host_names,debug_level)

            if len(ip_addresses) + len(mac_addresses) + len(device_ids) + len(host_names) + len(device_ranges) == 0:
                lib.wlist.print_data_t(0,'')
                if debug_level < 0:
                    lib.wmsg.wake_input()
                try:
                    variable=input('Please input a device: ')
                    if lib.wvarcheck.identify(variable) == 'IP':
                        ip_addresses.append(variable)
                    if lib.wvarcheck.identify(variable) == 'MAC':
                        mac_addresses.append(variable)
                    if lib.wvarcheck.identify(variable) == 'ID':
                        device_ids.append(variable)
                    if lib.wvarcheck.identify(variable) == 'HOST':
                        host_names.append(variable)
                    if len(host_names)+len(ip_addresses)+len(mac_addresses)+len(device_ids) != 0:
                        lib.wwake.wake(ip_addresses,mac_addresses,device_ids,host_names,debug_level)
                    else:
                        continue
                except:
                    print()
                    break

            count+=1

        else:
            lib.wmsg.invalid_command(implicit_commands[count])
            count+=1

'''
================
VARIABLE CHECKS
================
'''

def check_variables(variables,debug_level):
    count=0
    if debug_level > 0: print('Variables first...')
    if debug_level > 1:
        lib.wmsg.print_variables(variables)
    if debug_level > 0 and len(variables) != 0:
        lib.wmsg.identify_var()

    while count < len(variables):
        vartype = lib.wvarcheck.identify(variables[count])

        if vartype == 'IP':
            ip_addresses.append(variables[count])
            if debug_level > 0:
                lib.wmsg.found_ip(variables[count])
            count+=1

        elif vartype == 'IPMSK':
            sub_vars=variables[count].split('/')
            addresses_and_masks.append(variables[count])
            ip_addresses.append(sub_vars[0])
            subnet_masks.append(sub_vars[1])
            if debug_level > 0:
                lib.wmsg.found_ip(variables[count])
            count+=1

        elif vartype == 'MAC':
            formatted_mac = lib.wformac.format_mac(variables[count])
            mac_addresses.append(formatted_mac)
            if debug_level > 0:
                lib.wmsg.found_mac(variables[count])
            count+=1

        elif vartype == 'MASK':
            variables[count] = variables[count].replace('/','')
            subnet_masks.append(variables[count])
            if debug_level > 0:
                print('Found Mask: '+variable[count])
                #lib.wmsg.found_mask(variables[count])
            count+=1

        elif vartype == 'RANGE':
            device_ranges.append(variables[count])
            if debug_level > 0:
                lib.wmsg.found_range(variables[count])
            count+=1

        elif vartype == 'ID':
            device_ids.append(variables[count])
            if debug_level > 0:
                lib.wmsg.found_id(variables[count])
            count+=1

        elif vartype == 'HOST':
            host_names.append(variables[count])
            if debug_level > 0:
                lib.wmsg.found_host(variables[count])
            count+=1
        else:
            lib.wmsg.invalid_var(variables[count])
            lib.wmsg.remove_var()
            variables.remove(str(variables[count]))
            count+=1
    if debug_level > 1:
        lib.wmsg.identified_vars(ip_addresses,mac_addresses,device_ids,subnet_masks,host_names)

'''
===========
INPUT CHECK
===========
'''

def check_input(input_variables,debug_level):
    count = 1
    explicit_supplied_commands=[]
    implicit_supplied_commands=[]
    supplied_variables=[]
    found_ops=[]
    list_ops=[]
    while count < len(input_variables):

        #LOOK FOR EXPLICIT COMMANDS

        if re.search('\A--+\w+',input_variables[count]):
            input_variables[count]=input_variables[count].replace('-','')

            #LOOK FOR LIST OPERATORS

            if re.search(':',input_variables[count]):
                list_ops=input_variables[count].split(':')
                explicit_supplied_commands.append(list_ops[0])

            else:
                explicit_supplied_commands.append(input_variables[count])

            if debug_level > 1:
                lib.wmsg.found_explicit(str(explicit_supplied_commands[count-1]))


                count+=1
            if len(list_ops) != 0:
                while count < len(list_ops):
                    list_operators.append(list_ops[count])
                    if debug_level > 1:
                        lib.wmsg.found_list_op(list_ops[count])
                    count+=1


        #LOOK FOR IMPLICIT COMMANDS

        elif re.search('^\-\w+',input_variables[count]):
            input_variables[count]=input_variables[count].replace('-','')

            #LOOK FOR LIST OPERATORS
            if re.search(':',input_variables[count]):
                lcount=1
                list_ops = input_variables[count].split(':')
                list_ops[lcount].replace('l','')
                while lcount < len(list_ops):
                    input_variables[count]=input_variables[count].replace(list_ops[lcount],'')
                    lcount+=1
                input_variables[count]=input_variables[count].replace(':','')
                implicit_supplied_commands.append(input_variables[count])

                while count < len(list_ops):

                    if re.match('i',list_ops[count]):
                        list_operators.append('ip')
                        if debug_level > 1:
                            lib.wmsg.found_list_op(list_ops[count])

                    elif re.match('h',list_ops[count]):
                        list_operators.append('host')
                        if debug_level > 1:
                            lib.wmsg.found_list_op(list_ops[count])

                    elif re.match('b',list_ops[count]):
                        list_operators.append('mask')
                        if debug_level > 1:
                            lib.wmsg.found_list_op(list_ops[count])

                    elif re.match('m',list_ops[count]):
                        list_operators.append('mac')
                        if debug_level > 1:
                            lib.wmsg.found_list_op(list_ops[count])

                    elif re.match('s',list_ops[count]):
                        list_operators.append('status')
                        if debug_level > 1:
                            lib.wmsg.found_list_op(list_ops[count])
                    else:
                        wcount=1
                        while wcount > len(input_variables):
                            print(input_variables[wcount])
                            if debug_level > 0:
                                lib.wmsg.invalid_op(list_ops[wcount])
                            wcount+=1
                    count+=1
            else:

                for letter in input_variables[count]:
                    implicit_supplied_commands.append(letter)
                    if debug_level > 1:
                        lib.wmsg.found_implicit(letter)

        #LOOK FOR VARIABLES
        else:
            if input_variables[count] not in implicit_supplied_commands and input_variables[count] not in explicit_supplied_commands:
                supplied_variables.append(input_variables[count])
                if debug_level > 1:
                    lib.wmsg.found_variable(input_variables[count])
                count+=1
            else:
                count+=1

    if debug_level > 1:
        lib.wmsg.checking_commands()

    check_variables(supplied_variables,debug_level)
    check_commands(explicit_supplied_commands,implicit_supplied_commands,debug_level)
