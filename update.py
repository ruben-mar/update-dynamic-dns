# script to update the external DNS address
# https://www.namecheap.com/support/knowledgebase/article.aspx/29/11/how-do-i-use-a-browser-to-dynamically-update-the-hosts-ip

import os
import subprocess
import xmltodict
import csv
import io
import fnmatch
from csv import DictWriter
from collections import deque
import re
from datetime import datetime, timezone
from ip import get_router_ip


HOST = "@"
DOMAINNAME = 'blissaporter.com'
PASSWORD = '88d984714afe41338805e533d9a7e131'
FIELDS = ['id', 'date', 'ip']


# Maximum number of lines of the log file
MAX = 100
FILE = 'data/records.csv'

# Let's make sure that FILE will be found
def locate_script():
    script = os.path.realpath(__file__)
    os.chdir(os.path.dirname(script))


def is_csv(file): # Actually this only verifies that the extension of the file name is .csv
    return fnmatch.fnmatch(file.split('.',maxsplit=1)[1], 'csv')


# parse csv files https://realpython.com/python-csv/
def count_lines(file):
    if os.path.exists(file) and is_csv(file):
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
                raise ex
            except:
                # In case of any unhandled error, throw it away
                raise
    else:
        print("{} does not exist or is not csv.".format(file))


# TO-DO
def delete_rows(file):
    if count_lines(file) > 100:
    # Maximum number of lines of the log file
    # https://thispointer.com/python-how-to-delete-specific-lines-in-a-file-in-a-memory-efficient-way/
       print("Not implemented yet")

# TO-DO deal with the case of empty last line
def autoincrement_index(file):
    with open(file, 'r') as f:
        q = deque(f, 1)  # replace 1 lines read at the end
        for elem in q:
            index = int(re.split(',',elem)[0])
            return index + 1


def fetch_last_ip(file):
    with open(file, 'r') as f:
        q = deque(f, 1)  # replace 1 lines read at the end
        for elem in q:
            last_ip = re.split(',',elem)[2]
            return last_ip


def append_line(file, dict,fields):
    # Open file in append mode
    with open(file, 'a+', newline='') as write_obj:
        # Create a writer object from csv module
        dict_writer = DictWriter(write_obj, fieldnames=fields)
        # Add dictionary as wor in the csv
        dict_writer.writerow(dict)
    # print("Appended {} to {}.".format(dict,file))


def new_line():
    timestamp = datetime.now(timezone.utc)
    dict = {'id': autoincrement_index(FILE),'date': timestamp,'ip': get_router_ip()}
    return dict


def update_ip(new):
    # https://dynamicdns.park-your-domain.com/update?host=[host]&domain=[domain_name]&password=[ddns_password]&ip=[your_ip]
    url = 'https://dynamicdns.park-your-domain.com/update?host='+HOST+'&domain='+DOMAINNAME+'&password='+PASSWORD+'&ip='+str(new)
    # '-s' keeps curl quiet
    response = subprocess.check_output(['curl', '-s', url]).decode()
    result = xmltodict.parse(response)
    if result['interface-response']['Done'] == 'true':
        append_line(FILE,new_line(),FIELDS)
    else:
        print("Update failed.")

# MAIN

locate_script()

# total = count_lines(FILE)

# Dictionary {'id': '0001','date':'2020-09-19 18:06:27.389196+00:00','ip':'79.150.249.203'}

current_ip_address = get_router_ip()
stored_ip_address = fetch_last_ip(FILE).rstrip()
if current_ip_address != stored_ip_address:
    update_ip(current_ip_address)
else:
    print("Nothing to update.")
