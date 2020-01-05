#!/usr/bin/python3

import sys, os, platform, configparser, re
from pathlib import Path
import lib.wlist
import lib.wwake
import lib.whandler
import lib.wmsg

if platform.system().lower()=='windows':
    os.chdir(os.getcwd())
    directory = os.getcwd()
    slash = '\\'
else:
    os.chdir(os.path.dirname(sys.argv[0]))
    directory = Path().absolute()
    slash = '/'

ops_file = str(str(directory)+slash+'config.ini')

try:

    options = configparser.ConfigParser()
    options.read(ops_file)
    debug_level=int(options['OPTIONS']['DEBUG'])

    user_input=sys.argv

    if len(user_input)==1:
        lib.wmsg.print_banner()
    count=1
    while count < len(user_input):

        if re.search(r'DEBUG=2',str(user_input[count])):
            user_input.remove('DEBUG=2')
            debug_level = 2
            count+=1

        elif re.search(r'DEBUG=1',str(user_input[count])):
            user_input.remove('DEBUG=1')
            debug_level = 1
            count+=1
        else:
            count+=1

    if debug_level > 0:
        lib.wmsg.debug_level(debug_level)
        lib.wmsg.checking_input()
    lib.whandler.check_input(user_input,debug_level)

except KeyboardInterrupt:
    print()
    sys.exit(0)
