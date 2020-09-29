# script to auto-update the external IP address
# https://www.namecheap.com/support/knowledgebase/article.aspx/29/11/how-do-i-use-a-browser-to-dynamically-update-the-hosts-ip

import os
import subprocess
import xmltodict
from csv import DictWriter

HOST = "@"
DOMAINNAME = 'openswiftcodes.com'
PASSWORD = '8a89fe5dc85345578910d17344d2524d' # From section "DYNAMIC DNS" is https://ap.www.namecheap.com/Domains/DomainControlPanel/openswiftcodes.com/advancedns

def get_ip(): 
    ifconfig = subprocess.check_output("curl -sS ifconfig.me/ip", shell=True)
    # the output of curl is an object with the class bytes
    return ifconfig.decode()

print(get_ip())


