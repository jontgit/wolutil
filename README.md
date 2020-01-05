

# wakeonlan
           __      __   _
           \ \    / /__| |
            \ \/\/ / _ \ |__
             \_/\_/\___/____|

		WakeOnLan Utility

### Usage: wol [OPTION]... [VARIABLE]...

   Wake hosts in stored in the local CSV file
   Lists the host and status entries unless 
   additional operators are supplied.

**Explicit** commands are passed by using the **'--'** delimiter.
**Implicit** commands are passed by using the **'-'** delimiter.

#### --help
   can be passed for a description of the
   command along with examples.

#### -h       
   will only show examples of commands.
             
**e.g:**
    wol --wake -h
    wol -d --help

#### Command List:

    Explicit    |   Implicit
                |
    --list      |      -l
    --add       |      -a
    --delete    |      -d
    --wake      |      -w
    --scan      |      -s
    --ping      |      -p
    
### __List Command__
   
#### -l, --list      		
   Lists the current database that has been configured  
   by the user. Additional operators can be passed with  
   the ':' delimiter to show certain information.  
   
   **List Operators**:  
   
   :host   :h  
   :mac    :m  
   :ip     :i  
   :mask   :b  
   :status :s  
 
 --list:[List Operators]

#### List Examples:

   Implicit:   `-l:h:m `  
   Explicit:   `--list:host:mac`  
 
   Implicit:   `-l:i:s:h`  
   Explicit:   `--list:ip:status:host`  
	
### __Addition Command__
	
#### -a, --add
   Adds a new host to the host database. If no variables  
   are provided with the command, the user will be promp-  
   ted to confirm the details to append them to the host  
   list. Host variables must be separated by a space. IP  
   address variables must contain a CIDR mask after the   
   address. If not enough variables are passed to add a  
   full entry to the database, you will be prompted to  
   input the necessary remaining fields.  
 
   --add [Hostname] [IP Address/CIDR Mask] [MAC Address]

#### Add Examples:
   Implicit:	`-a Hostname1 192.168.0.25/24 FF:FF:FF:FF:FF:FF`  
		`-a 10.0.0.1/24 10.0.0.2/24`  
 
   Explicit:	`--add 10.0.0.1/24 10.0.0.2/24`  
   		`--add Host2 10.3.4.2/23 AA.BB.CC.DD.EE.FF.AA`
			
### __Deletion Command__
			
### -d, --delete    
   Removes the selected host from the database. Device IDs  
   can be passed as variables, or if none are stated, you  
   will be prompted for a selection to delete.  
 
   --delete [Device ID]

#### Delete Examples:
   Implicit:	`-d 3`  
   		`-d 5-7`
   Explicit:  	`--delete 3 4`
   		`--delete 2-6 7 9-13`
			
### __Wake Command__
			
### -w, --wake      
   Wakes the target computer specified by the user. this  
   works in a similar way to the addition command, if no  
   variables are passed by the user, the host list will  
   print and they will be prompted to select a host by  
   either a host ID, IP address, Hostname or MAC address.  
   Multiple arguments can be passed to send multiple magic  
   packets in one command. Any combination of the below  
   variables may be referenced at once.  
 
   --wake [Device ID | Hostname | IP Address | MAC Address]

#### Wake Examples:
  Implicit:   `-w 1 2 4-7`
  	      `-w 192.168.0.1`
	      `-w host1 hostname2`
	       
  Explicit:   `--wake 1 2 4-7`
  	      `--wake 192.168.0.1`
	      `--wake host1 hostname2`  
  
  
### __Ping Command__
   
#### -p, --ping

   Ping all hosts currently stored in the database.
   This is used to ascertain the status of the host.
   Currently this is the default behavior if no IP
   is supplied by the user.

   Individual hosts can be called if passed via the
   cli.
   
   --ping [None] | [IP Address | Device ID]

#### Wake Examples:
    

   Implicit:   `-p` 
    	       `-p 192.168.0.1`
		
   Explicit:  `--ping` 
              `--ping 10.3.3.4`
