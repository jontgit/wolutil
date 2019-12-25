import re

def identify(input_variable):

    ip_address = re.compile("^(([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\.){3}([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])$")

    ipv4_with_cidr=re.compile("^(([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\.){3}([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])(\/(3[0-2]|[1-2][0-9]|[0-9]))$")

    mac_address = re.compile("^[0-9A-Fa-f]{2}['.'':'][0-9A-Fa-f]{2}['.'':'][0-9A-Fa-f]{2}['.'':'][0-9A-Fa-f]{2}['.'':'][0-9A-Fa-f]{2}['.'':'][0-9A-Fa-f]{2}$")
    mac_address_a = re.compile("^[0-9A-Fa-f]{4}['.'':'][0-9A-Fa-f]{4}['.'':'][0-9A-Fa-f]{4}$")

    device_id = re.compile("\d")
    #cidr_mask = re.compile("^([/]{1}[1-9]{1}|[/][1-2][0-9]{2}|[/][3][0-2]{2})$")
    device_range = re.compile("^\d+-\d+")
    subnet_mask = re.compile("^((25[0-5]|2[0-4]\d|1\d\d|[1-9]\d|\d)\.){3}(25[0-5]|2[0-4]\d|1\d\d|[1-9]\d|\d)$")
    
    cidr_mask = re.compile("^([/][1-9]\d|[1-3][1-9]\d\d)$")
    
    host_name = re.compile(r"\w+")

    if ip_address.match(input_variable):
        return 'IP'
    elif ipv4_with_cidr.match(input_variable):
        return 'IPMSK'
    elif cidr_mask.match(input_variable):
        return 'MASK'
    elif mac_address.match(input_variable) or mac_address_a.match(input_variable):
        return 'MAC'
    elif device_range.match(input_variable):
        return 'RANGE'
    elif device_id.match(input_variable):
        return 'ID'
    elif host_name.match(input_variable):
        return 'HOST'
    else:
        return 'NULL'
