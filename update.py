# script to auto-update the external IP address
# https://www.namecheap.com/support/knowledgebase/article.aspx/29/11/how-do-i-use-a-browser-to-dynamically-update-the-hosts-ip

import os
import subprocess
import xmltodict
from ip import get_ip
from recording import FILE
from recording import fetch_last_ip


HOST = "@"
DOMAINNAME = 'openswiftcodes.com'
PASSWORD = '8a89fe5dc85345578910d17344d2524d' # From section "DYNAMIC DNS" is https://ap.www.namecheap.com/Domains/DomainControlPanel/openswiftcodes.com/advancedns


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

# Dictionary {'id': '0001','date':'2020-09-19 18:06:27.389196+00:00','ip':'79.150.249.203'}

ipaddress = fetch_last_ip(FILE)

if ipaddress != get_ip():
    new = get_ip()
    update_ip(new)
else:
    print("Nothing to update.")
