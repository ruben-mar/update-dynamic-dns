# script to auto-update the external IP address
# https://www.namecheap.com/support/knowledgebase/article.aspx/29/11/how-do-i-use-a-browser-to-dynamically-update-the-hosts-ip

import os
import csv
import io
import fnmatch
from csv import DictWriter
from collections import deque
import re
from datetime import datetime, timezone


# Maximum number of lines of the log file
MAX = 100
FILE = 'data/records.csv'
FIELDS = ['id', 'date', 'ip']


def locate_script():
    script = os.path.realpath(__file__) 
    print("The path of this script is {}".format(os.path.dirname(script)))
    os.chdir(os.path.dirname(script))


def is_csv(file): # Actually this only verifies that the extension of the file name is .csv
    if fnmatch.fnmatch(file.split('.',maxsplit=1)[1], 'csv'):
        return True


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


def autoincremnet_index(file):
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


def append_line(file, dict, fields):
    # Open file in append mode
    with open(file, 'a+', newline='') as write_obj:
        # Create a writer object from csv module
        dict_writer = DictWriter(write_obj, fieldnames=fields)
        # Add dictionary as wor in the csv
        dict_writer.writerow(dict)
    print("Appended {} to {}.".format(dict,file))


# MAIN
# Dictionary {'id': '0001','date':'2020-09-19 18:06:27.389196+00:00','ip':'79.150.249.203'}


locate_script()
print(os.listdir())
print(is_csv(FILE))
total = count_lines(FILE)
print("The number of lines is {}".format(total))
timestamp = datetime.now(timezone.utc)

dict = {'id': '0006','date':'2020-09-21 22:39:57.321836+00:00','ip':'2.17.39.106'}
print()
# append_line(FILE,dict,FIELDS)
print(fetch_last_ip(FILE))
