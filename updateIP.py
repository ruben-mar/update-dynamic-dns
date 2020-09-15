# script to auto-update the external IP address
# https://www.namecheap.com/support/knowledgebase/article.aspx/29/11/how-do-i-use-a-browser-to-dynamically-update-the-hosts-ip

import os
import subprocess
import pycurl
import xmltodict
import time

HOST = "@"
DOMAINNAME = 'openswiftcodes.com'
PASSWORD = '8a89fe5dc85345578910d17344d2524d' # From section "DYNAMIC DNS" is https://ap.www.namecheap.com/Domains/DomainControlPanel/openswiftcodes.com/advancedns


def get_ip(): 
    ifconfig = subprocess.check_output("curl -sS ifconfig.me/ip", shell=True)
    # the output of curl is an object with the class bytes
    return ifconfig.decode()


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


# MAIN

ipaddress = get_ip()

print("The current IP address is",ipaddress)

update_ip(ipaddress)


if ipaddress != get_ip():
    new = get_ip()
    update_ip(new)
else:
    print("Nothing to update.")

