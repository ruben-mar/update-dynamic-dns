# script to auto-update the external IP address
# https://www.namecheap.com/support/knowledgebase/article.aspx/29/11/how-do-i-use-a-browser-to-dynamically-update-the-hosts-ip

import os
import csv
import io
import fnmatch

# Maximum number of lines of the log file
MAX = 100

def locate_script():
    script = os.path.realpath(__file__) 
    print("The path of this script is {}".format(os.path.dirname(script)))
    os.chdir(os.path.dirname(script))
    print(os.getcwd())

def is_csv(file):
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
                    print("The row is {}".format(row))
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

def delete_rows(file):
    if count_lines(file) > 100:
    # Maximum number of lines of the log file
    # https://thispointer.com/python-how-to-delete-specific-lines-in-a-file-in-a-memory-efficient-way/
        pass


# MAIN
locate_script()
print(os.listdir())
print(is_csv("log3.csv"))
total = count_lines("log2.csv")
print("The number of lines is {}".format(total))
#  print(datetime.now(timezone.utc))


