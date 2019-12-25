import struct
import sys
import socket
import lib.wread
import lib.wmsg
import lib.wakeonlan

def wake(ip_addresses,mac_addresses,device_ids,host_names,debug_level):

    count=0
    while count < len(mac_addresses):
        if debug_level >1:
            lib.wmsg.search_mac(mac_addresses[count])
        if lib.wread.look_for_var(mac_addresses[count],'MAC') == True:
            ip = lib.wread.look_for_ip(mac_addresses[count],'MAC')
            host = lib.wread.look_for_host(mac_addresses[count],'MAC')
            print('\nIP Address:  '+str(ip))
            print('Host Name:   '+str(host))
            print('MAC Address: '+str(mac_addresses[count]))
            lib.wakeonlan.send_magic_packet(str(mac_addresses[count]))
            print('Magic Packet Sent.')
        count+=1

    while count < len(ip_addresses):
        if debug_level > 1:
            lib.wmsg.search_ip(ip_addresses[count])
        if lib.wread.look_for_var(ip_addresses[count],'IP') == True:
            mac = lib.wread.look_for_mac(ip_addresses[count],'IP')
            host = lib.wread.look_for_host(ip_addresses[count],'IP')
            print('\nIP Address:  '+str(ip_addresses[count]))
            print('Host Name:   '+str(host))
            print('Mac Address: '+str(mac))
            lib.wakeonlan.send_magic_packet(str(mac))
            print('Magic Packet Sent.')
            count+=1
        else:
            lib.wmsg.not_found('IP address')

    while count < len(host_names):
        if debug_level >1:
            lib.wmsg.search_mac(host_names[count])
        if lib.wread.look_for_var(host_names[count],'HOST') == True:
            mac = lib.wread.look_for_mac(host_names[count],'HOST')
            ip = lib.wread.look_for_ip(host_names[count],'HOST')
            print('\nIP Address:  '+str(ip))
            print('Host Name:   '+str(host_names[count]))
            print('Mac Address: '+str(mac))
            lib.wakeonlan.send_magic_packet(str(mac))
            print('Magic Packet Sent.')
            count+=1
        else:
            lib.wmsg.not_found('Host name')
        count+=1

    while count < len(device_ids):
        if debug_level > 1:
            lib.wmsg.search_dev(device_ids[count])
        if lib.wread.look_for_var(device_ids[count],'ID') == True:
            mac = lib.wread.look_for_mac(device_ids[count],'ID')
            ip = lib.wread.look_for_ip(device_ids[count],'ID')
            host = lib.wread.look_for_host(device_ids[count],'ID')
            print('\nIP Address:  '+str(ip))
            print('Host name:   '+str(host))
            print('MAC Address: '+str(mac))
            print('Magic Packet Sent.')
            lib.wakeonlan.send_magic_packet(str(mac))
        else:
            lib.wmsg.not_found('Device ID')
        count+=1
    print()

