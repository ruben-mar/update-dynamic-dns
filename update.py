# script to auto-update the external IP address
# https://www.namecheap.com/support/knowledgebase/article.aspx/29/11/how-do-i-use-a-browser-to-dynamically-update-the-hosts-ip

import os
import subprocess
import xmltodict
from datetime import datetime, timezone
from csv import DictWriter

HOST = "@"
DOMAINNAME = 'openswiftcodes.com'
PASSWORD = '8a89fe5dc85345578910d17344d2524d' # From section "DYNAMIC DNS" is https://ap.www.namecheap.com/Domains/DomainControlPanel/openswiftcodes.com/advancedns

def locate_script():
    script = os.path.realpath(__file__) 
    print("The path of this script is {}".format(os.path.dirname(script)))
    os.chdir(os.path.dirname(script))
    print(os.getcwd())


def get_ip(): 
    ifconfig = subprocess.check_output("curl -sS ifconfig.me/ip", shell=True)
    # the output of curl is an object with the class bytes
    return ifconfig.decode()

def fetch_ip():
    try:
        with open('log.txt','r') as file: # The rb mode will open the file for binary data reading. 
            file.seek(-2, os.SEEK_END)
            while file.read(1) != b'\n':
                file.seek(-2, os.SEEK_CUR)
            last_line = file.readline().decode()
            return last_line
            
    except:
        print("Failed to open and parse the log.")


def update_ip(new):
    # https://dynamicdns.park-your-domain.com/update?host=[host]&domain=[domain_name]&password=[ddns_password]&ip=[your_ip]
    url = 'https://dynamicdns.park-your-domain.com/update?host='+HOST+'&domain='+DOMAINNAME+'&password='+PASSWORD+'&ip='+str(new)
    # '-s' keeps curl quiet
    response = subprocess.check_output(['curl', '-s', url]).decode()
    result = xmltodict.parse(response)
    if result['interface-response']['Done'] == 'true':
        print("IP address {} updated".format(new))
    else:
        print("Update failed.")

def new_entry(): 
    # https://thispointer.com/python-how-to-append-a-new-row-to-an-existing-csv-file/
    pass

# MAIN

# Dictionary {'id': '0001','date':'2020-09-19 18:06:27.389196+00:00','ip':'79.150.249.203'}

ipaddress = get_ip()

print("The current IP address is",ipaddress)

update_ip(ipaddress)


if ipaddress != get_ip():
    new = get_ip()
    update_ip(new)
else:
    print("Nothing to update.")

