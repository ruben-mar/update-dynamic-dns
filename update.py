# script to update the external DNS address
# https://www.namecheap.com/support/knowledgebase/article.aspx/29/11/how-do-i-use-a-browser-to-dynamically-update-the-hosts-ip

import subprocess
import os
import fnmatch
import subprocess
import xmltodict
import csv
import io
import re
from csv import DictWriter
from collections import deque
try: 
    from datetime import datetime, timezone
except ImportError:
    import datetime


DOMAINNAME = ''
PASSWORD = ''
FIELDS = ['id', 'date', 'ip']
FILE = 'log/ip-log.csv'
MAX = 1000

# Host is the computer running this application
def get_host_ip() -> int: 
    ifconfig = subprocess.check_output("curl -sS ifconfig.me/ip", shell=True)
    # the output of curl is an object with the class bytes
    return ifconfig.decode()


# Domain is the domain name whose A + Dynamic DNS Record needs updating
def get_domain_ip() -> int:
    host_ip = subprocess.check_output("host "+DOMAINNAME+" | grep 'has\ address' | sed 's/blissaporter\.com has address //g'", shell=True)
    return host_ip.decode().rstrip()


# The log is in the relative path of the script for convenience
def locate_script():
    script = os.path.realpath(__file__)
    os.chdir(os.path.dirname(script))


# Control the size of the logs
def count_lines(file) -> int:
    if os.path.exists(file):
        with open(file) as input:
            try: 
                file_content = csv.reader(input)
                line_count = 0
                for row in file_content:
                    line_count += 1
                return line_count
            except EOFError as ex:
                print("Caught the EOF error.")
                raise ex
            except IOError as e:
                print("Caught the I/O error.")
                raise e
            except:
                # In case of any unhandled error, throw it away
                raise
    else:
        print("There is a problem with {} or it does not exist.".format(file))


# Trim the excess lines of the log
def trim_log(file):
    if count_lines(file) > MAX:
        n = count_lines(file) - MAX 
        subprocess.check_output("sed -i '1,"+str(n)+"d' "+ file, shell= True) 
        return [file, n]

def autoincrement_index(file):
    with open(file, 'r') as f:
        q = deque(f, 1)  # replace 1 lines read at the end
        for elem in q:
            index = int(re.split(',',elem)[0])
            return index + 1


# The most recent record of IP address in the log
def get_log_ip(file) -> str:
    subprocess.check_output("sed -i '/^[[:space:]]*$/d' " + file, shell= True) # Removes all blank lines first
    with open(file, 'r') as f:
        q = deque(f, 1)  # replace 1 lines read at the end
        for elem in q:
            last_ip = re.split(',',elem)[2].rstrip()
            return last_ip


def append_line(file, dict,fields):
    # Open file in append mode
    with open(file, 'a+', newline='') as write_obj:
        # Create a writer object from csv module
        dict_writer = DictWriter(write_obj, fieldnames=fields)
        # Add dictionary as a row in the csv
        dict_writer.writerow(dict)


def new_line() -> dict: # Dictionary {'id': '0001','date':'2020-09-19 18:06:27.389196+00:00','ip':'79.150.249.203'}
    timestamp = datetime.now(timezone.utc)
    dict = {'id': autoincrement_index(FILE),'date': timestamp,'ip': get_host_ip()}
    return dict


def update_dns(new):
    # https://dynamicdns.park-your-domain.com/update?host=@&domain=[domain_name]&password=[ddns_password]&ip=[your_ip]
    url = 'https://dynamicdns.park-your-domain.com/update?host=@&domain='+DOMAINNAME+'&password='+PASSWORD+'&ip='+str(new)
    # '-s' keeps curl quiet
    response = subprocess.check_output(['curl', '-s', url]).decode()
    result = xmltodict.parse(response)
    if result['interface-response']['Done'] != 'true':
        print("Update failed.")

# MAIN

locate_script()


current_host_address = get_host_ip()
current_domain_address = get_domain_ip()
stored_ip_address = get_log_ip(FILE)


try:
    if current_host_address != current_domain_address and current_host_address != stored_ip_address:
        update_dns(current_host_address)
        append_line(FILE,new_line(),FIELDS)
    elif current_host_address == current_domain_address and current_host_address != stored_ip_address:
        append_line(FILE,new_line(),FIELDS)
except ValueError:
    print("The domain address {} has not been updated with the current host {} address".format(current_domain_address, current_host_address))
finally:
    if trim_log(FILE):
        trimmed = trim_log(FILE)
        print("Knocked {} lines off {}".format(trimmed[0],trimmed[1]))
    elif trim_log('log/cron-log.txt'):
        trimmed = trim_log('log/cron-log.txt')
        print("Knocked {} lines off {}".format(trimmed[0],trimmed[1]))
    else:
        print("Successful run of {} at {}".format(__file__,datetime.now(timezone.utc)))
