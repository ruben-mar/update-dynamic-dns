# Update-Dynamic-DNS
This application updates the IP address of domains registered at Namecheap. It is useful when ISPs change the IP address of your router, for instance following power cuts. This update in the Domain Name System (DNS) is Dynamic DNS (DDNS).  
These scripts compare the current and previous IP address so they detect everytime you ISP allocates a new IP address to your router. Changes trigger these scripts to update the new IP address at Namecheap instead of updating the DNS manually in the regitrar's website or using the desktop application for Windows provided by Namecheap.  
The magic of this software consists in iterating over the parameter of [Namecheap's URL service](https://dynamicdns.park-your-domain.com/update?host=[host]&domain=[domain_name]&password=[ddns_password]&ip=[your_ip]) upon 
https://www.namecheap.com/support/knowledgebase/article.aspx/29/11/how-to-dynamically-update-the-hosts-ip-with-an-http-request/
  
[![Hex.pm](https://img.shields.io/hexpm/l/plug.svg)](/LICENSE.md)  
  
# 1. Overview
## 1.a. Dynamic DNS
This script is an alternative to Dynamic DNS (also known as DDNS or DynDNS) services that map Internet domain names to a computer (hostnames) with dynamic IP addresses. Home Nextcloud servers connect to their router via DHCP. The ISP assigns an IP address to your router every now and then.
# 2. Get started
This application is written in Python so it runs successfully on the following operating systems:
- _Linux_
- _Windows_
- _Mac OS_
The libraries are installed with Anaconda https://docs.anaconda.com/navigator/tutorials/manage-environments/.
`$ conda create --name dyndns --file conda-requirements.txt`
## 2.a. Setup Dynamic DNS and configure domains and subdomains at Namecheap
https://www.namecheap.com/support/knowledgebase/article.aspx/43/11/how-do-i-set-up-a-host-for-dynamic-dns/
## 2.b. Get the Dynamic DNS password at Namecheap
The registrar provides a password to update the DNS in its 'Advanced DNS' section of the management page of each domain.
## 2.c. Install and run
Copy the folder containing the files and simply run from your terminal
`$ python update.py`
You may need to install pycurl and xmltodic
`$ sudo apt install python-pycurl`
`$ pip install xmltodic`
## 2.d. Crontab
Schedule a regular run of the utility cron at fixed times, dates, or intervals. You can use the command crontab in Unix-like computer operating systems.
`$ crontab -e`
Intervals of time and days when to run the application
Command To Execute: path of the python command followed by path of the application
Example of line that runs the aplication every 15 minutes of all hours and days of the week:
`*/15 * * * 0-6 /home/bu/anaconda3/bin/python /home/bu/ruben/applications/Update-Dynamic-DNS/update.py >/dev/null 2>&1`
# 3. Develop
This application requires Python >=3.6 and [curl](https://github.com/curl/curl).
- **Found issues?** Then please **file an issue** [here](https://github.com/ruben-mar/Update-Dynamic-DNS/issues).


