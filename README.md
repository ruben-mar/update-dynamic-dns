# Update-Dynamic-DNS
This application updates the IP address of domains registered at Namecheap to run a Nextcloud server without having to update the DNS manually nor install a local client.

[![Hex.pm](https://img.shields.io/hexpm/l/plug.svg)](/LICENSE.md)

# 1. Overview

## 1.a. Dynamic DNS

This script is an alternative to Dynamic DNS (also known as DDNS or DynDNS) services that map Internet domain names to a computer (hostnames) with dynamic IP addresses. Home Nextcloud servers connect to their router via DHCP. The ISP assigns an IP address to your router every now and then.


# 2. Get started

This application is written in Python so it runs successfully on the following operating systems:

- _Linux_
- _Windows_
- _Mac OS_

as long as they have Python installed.

## 2.a. Install and run
Copy the folder containing the files and simply run from your terminal
`$ python updateIP.py`
You may need to install pycurl and xmltodic
`$ sudo apt install python-pycurl`
`$ pip install xmltodic`

# 3. Develop

This application requires Python >=3.6 and the project [exif 1.0.0](https://pypi.org/project/exif/).
- **Found issues?** Then please **file an issue** [here](https://github.com/ruben-mar/Olympus-file-manager/issues).


