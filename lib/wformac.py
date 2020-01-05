import re
def format_mac(mac_address):

    #if re.search(':.',mac_address):
    #    print('Error: Found both . and : in inputted MAC address')
    #    sys.exit()

    if re.search(':',mac_address):
        formatted_address=''
        mac_address=mac_address.replace(':','')
        count = 0
        for letter in mac_address:
            if count in [2,4,6,8,10]:
                formatted_address =formatted_address+':'
                formatted_address = formatted_address+str(letter)
                count +=1
            else:
                formatted_address = formatted_address+str(letter)
                count +=1
        formatted_address=formatted_address.upper()
        return str(formatted_address)

    elif re.search('.',mac_address):
        formatted_address=''
        mac_address=mac_address.replace('.','')
        count = 0
        for letter in mac_address:
            if count in [2,4,6,8,10]:
                formatted_address =formatted_address+':'
                formatted_address = formatted_address+str(letter)
                count +=1
            else:
                formatted_address = formatted_address+str(letter)
                count +=1
        formatted_address=formatted_address.upper()
        return str(formatted_address) 
    else:
        print('not sure how you managed that mate.')
