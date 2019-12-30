import lib.wdb
import lib.wvarcheck
import lib.wformac
import re


def addition(ip_addresses,mac_addresses,subnet_masks,host_names):
    unique_inputs = max(len(ip_addresses),len(mac_addresses),len(subnet_masks),len(host_names))
    count = 0
    if unique_inputs==0:
        unique_inputs+=1
    while count < unique_inputs:
        if len(ip_addresses) <= count:
            try:
                input_ip = input('Please enter an IP address: ')
                if lib.wvarcheck.identify(input_ip) == 'IPMSK':
                    split_ip_mask=input_ip.split('/')
                    ip_addresses.append(split_ip_mask[0])
                    subnet_masks.append(split_ip_mask[1])
                    split_ip_mask=[]
                elif lib.wvarcheck.identify(input_ip) == 'IP':
                    ip_addresses.append(input_ip)
                else:
                    print('Error - Invalid IP: '+input_ip)
                    continue
            except:
                print()
                break
        if len(subnet_masks) <= count:
            try:
                input_mask = input('Plese enter a Mask: ')
                if lib.wvarcheck.identify(input_mask) == 'MASK':
                    input_mask = input_mask.replace('/','')
                    subnet_masks.append(input_mask)
                else:
                    print('Error - Invalid Mask: '+input_mask)
                    continue
            except:
                print()
                break

        if len(mac_addresses) <= count:
            try:
                input_mac = input('Plese enter a MAC address: ')
                if lib.wvarcheck.identify(input_mac) == 'MAC':
                    input_mac=lib.wformac.format_mac(input_mac)
                    mac_addresses.append(input_mac)
                else:
                    print('Error - Invalid MAC: '+input_mac)
                    continue
            except:
                print()
                break

        if len(host_names) <= count:
            try:
                input_name = input('Please enter a host name: ')
                if lib.wvarcheck.identify(input_name) == 'HOST':
                    host_names.append(input_name)
                else:
                    print('Error - Invalid Host Name: '+input_name)
                    continue
            except:
                print()
                break

        print('\nDevice ID:   '+str(count+1)+' of '+str(len(ip_addresses)))
        print('IP Address:  '+ip_addresses[count])
        print('Subnet Mask: '+subnet_masks[count])
        print('MAC Address: '+mac_addresses[count])
        print('Host Name:   '+host_names[count]+'\n')

        csv_line=[]
        csv_line.append(host_names[count])
        csv_line.append(ip_addresses[count])
        csv_line.append(mac_addresses[count])
        csv_line.append('down')
        csv_line.append('/'+str(subnet_masks[count]))

        confirmation = input('Is the above correct?: ')

        if count >= len(ip_addresses)-1:
            exit()
        if confirmation in ["y","Y","yes","Yes","YES"]:
            lib.wdb.append(0,csv_line)
            print('\nAdded host to database.')
            count+=1
        elif confirmation in ["n", "N", "no","No","NO"]:
            print('\nSkipping Entry.')
            count+=1
