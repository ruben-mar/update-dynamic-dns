# Update-Dynamic-DNS
This application updates the IP address of domains registered at Namecheap to run a Nextcloud server without having to update the DNS manually nor install a local client.

[![Hex.pm](https://img.shields.io/hexpm/l/plug.svg)](/LICENSE.md)

# 1. Overview

## 1.a. Dynamic DNS

This script is an alternative to Dynamic DNS (also known as DDNS or DynDNS) services that map Internet domain names to a computer (hostnames) with dynamic IP addresses. Nextcloud servers connect to their router via DHCP. The ISP assigns an IP address to your router every now and then.

# 2. Get started

This application is written in Python and curl and the UNIX utility sed so it runs successfully on the following operating systems:
- _Linux_
- _Mac OS_

## 2.a. Install
Copy the folder containing the files.
Open update.py with a text editor and enter the values of 
DOMAINNAME
PASSWORD
that you will find in the Advanced DNS page of a domain, section Dynamic DNS in Namecheap.

## 2.b. Run
From the terminal run
`$ python update.py`
If your system have both python 2 and python 3 installed, you may need to run 
`$ python3 update.py`

You may need to install pycurl, xmltodic and other libraries that you may requiere with:
`$ sudo apt install python-pycurl`
`$ pip install xmltodic`

## 2.c. Schedule
Schedule a regular run of the utility with the command crontab in Unix-like computer operating systems.
`$ crontab -e`
Intervals of time and days when to run the application
Command To Execute: path of the python command followed by path of the application
Example of line that runs the aplication every 15 minutes of all hours and days of the week:
`*/15 * * * 0-6 ~/anaconda3/bin/python ~/Update-Dynamic-DNS/update.py >/dev/null 2>&1`

# 3. Develop

This application requires Python >=3.6 and [curl](https://github.com/curl/curl).
- **Found issues?** Then please **file an issue** [here](https://github.com/ruben-mar/Update-Dynamic-DNS/issues).
