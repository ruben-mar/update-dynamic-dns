#!/usr/bin/env python3
""" script to update the external DNS address
https://www.namecheap.com/support/knowledgebase/article.aspx/29/11/how-do-i-use-a-browser-to-dynamically-update-the-hosts-ip
"""
import subprocess
import os
import re
import csv
from collections import deque
import json
import time
import xmltodict
import internet_connection

try:
    from datetime import datetime, timezone
except ImportError:
    import datetime


def get_host_ip() -> str:
    """IP address of the host computer running this application"""
    ifconfig = subprocess.check_output("curl -sS ifconfig.me/ip", shell=True)
    # the output of curl is an object with the class bytes
    return ifconfig.decode()


def get_domain_ip(subdomain, domainname) -> str:
    """Command hosts in Linux returns the IP address of a domain.
    Domain is the subdomain and the domain name whose A + Dynamic DNS Record needs updating"""
    while subdomain not in ["@", ""]:
        host_ip = subprocess.check_output(
            "host "
            + subdomain
            + "."
            + domainname
            + " | grep 'has address' | sed 's/"
            + subdomain+'.'+domainname
            + " has address //g'",
            shell=True,
        )
        return host_ip.decode().rstrip()


def count_lines(log) -> int:
    """ Control the size of the logs
    """
    if os.path.exists(log):
        with open(log) as input:
            try:
                log_content = csv.reader(input)
                line_count = 0
                for row in log_content:
                    line_count += 1
                return line_count
            except EOFError as ex:
                print("Caught the EOF error.")
                raise ex
            except IOError as e:
                print("Caught the I/O error.")
                raise e
    else:
        print("There is a problem with {log} or it doesn't exist.")


def trim_log(log):
    """ Trim the excessive lines of the log """
    while count_lines(log) > MAX:
        n = count_lines(log) - MAX
        subprocess.check_output("sed -i '1," + str(n) + "d' " + log, shell=True)
        return [log, n]


def autoincrement_index(ip_log):
    if os.path.isfile(ip_log):
        with open(ip_log, "r") as f:
            q = deque(f, 1)  # replace 1 line read at the end
            for elem in q:
                index = int(re.split(",", elem)[0])
                return index + 1


def get_log_ip(ip_log) -> str:
    """ Get The most recent record of IP address in the log
    Remove all blank lines
    '[[' and ']]' are shell keywords
    The [[ ]] bash construct is the extended test command
    The brackets [] delineate a range of characters to match as part of a regular expression
    [:space:] matches whitespace characters (space and horizontal tab)
    [[:space:]] matches any sequence of whitespace character/s and empty lines
    """
    if os.path.isfile(ip_log):
        subprocess.check_output("sed -i '/^[[:space:]]*$/d' " + ip_log, shell=True)
        with open(ip_log, "r") as f:
            q = deque(f, 1)  # replace 1 line read at the end
            for elem in q:
                last_ip = re.split(",", elem)[3].rstrip()
                return last_ip
    else:
        print(f"Missing {ip_log}. Check its path.")


def append_dict(ip_log, dict, fields):
    if os.path.isfile(ip_log):
        # Open ip_log in append mode
        with open(ip_log, "a+", newline="") as write_obj:
            # Create a writer object from csv module
            dict_writer = csv.DictWriter(write_obj, fieldnames=fields)
            # Add dictionary as a row in the csv
            if not dict_writer.writerow(dict):
                return False
    else:
        print("Missing {}. Check its path.".format(ip_log))


def append_line(log, line):
    """ append mode """
    file = open(log, "a")
    file.write(line)
    file.close()


def new_ip_record(domainname) -> dict:
    """ Dictionary {'id': '0001','date':'2020-09-19 18:06:27.389196+00:00',
    'domainname': '', ip':''}
    """
    timestamp = datetime.now(timezone.utc)
    dict = {
        "id": autoincrement_index(ip_log),
        "date": timestamp,
        "domainname": domainname,
        "ip": get_host_ip(),
    }
    return dict


def update_dns(subdomain, domainname, password, new_ip):
    """ Load the URL
    https://dynamicdns.park-your-domain.com/update?host=@&domain=[domain_name]&password=[ddns_password]&ip=[your_ip]
    """
    url = (
        "https://dynamicdns.park-your-domain.com/update?host="
        + subdomain
        + "&domain="
        + domainname
        + "&password="
        + password
        + "&ip="
        + str(new_ip)
    )
    # '-s' keeps curl quiet
    response = subprocess.check_output(["curl", "-s", url]).decode()
    result = xmltodict.parse(response)
    return result["interface-response"]["Done"] == 'true'


def read_csv_ip_log(ip_log):
    if os.path.exists(ip_log):
        with open(ip_log) as input:
            try:
                ip_log_content = csv.reader(input)
                line_count = 0
                for row in ip_log_content:
                    line_count += 1
            except EOFError as ex:
                print("Caught the EOF error.")
                raise ex
            except IOError as e:
                print("Caught the I/O error.")
                raise e
            except Exception:
                # In case of any unhandled error, throw it away
                raise
    else:
        print("There is a problem with {} or it doesn't exist.".format(ip_log))


def curb_logs(ip_log, runs_log):
    """ Keep the size of logs to some size """
    if os.path.exists(ip_log) and os.path.exists(runs_log):
        curbed = []
        logs = [ip_log, runs_log]
        for log in logs:
            if trim_log(log):
                trimmed = trim_log(log)
                curbed.append(trimmed)
        if len(curbed) <= 1:
            return curbed
    else:
        print("There is a problem with the files {ip_log} or {runs_log}.")


def update_dynamic_ip():
    """ Iterate over config file and update all subdomains and domains' IP addresses """
    if internet_connection.is_cnx_active(5):
        for domain in content["domains"]:
            subdomains = list(domain["hosts"])
            for subdomain_id in subdomains:
                subdomain = domain.get("hosts").get(subdomain_id)
                domainname = domain.get("name")
                password = domain.get("password")
                current_host_address = get_host_ip()
                current_domain_address = get_domain_ip(subdomain, domainname)
                try:
                    if current_domain_address and current_host_address != current_domain_address:
                        update = update_dns(
                            subdomain, domainname, password, current_host_address
                        )
                        if not update:
                            return domainname, password, current_host_address
                        else:
                            if logs_exist(ip_log, runs_log):
                                append_dict(ip_log, new_ip_record(domainname), FIELDS)
                    elif (
                        current_domain_address and current_host_address == current_domain_address
                        and current_host_address != stored_ip_address
                    ):
                        if logs_exist(ip_log, runs_log):
                            append_dict(ip_log, new_ip_record(domainname), FIELDS)
                except ValueError:
                    print(
                        "The domain {}'s IP address {} wasn't updated with the current host's {} one.".format(
                            domainname, current_domain_address, current_host_address
                        )
                    )
                finally:
                    if logs_exist(ip_log, runs_log) and curb_logs(ip_log, runs_log):
                        trimmed = curb_logs()
                        print(f"Knocked lines off {trimmed}")
    else:
        # wait for the connection to work
        time.sleep(600)
    return current_host_address


def logs_exist(ip_log, runs_log):
    if os.path.exists(ip_log) and os.path.exists(runs_log):
        return True


def write_run(new_ip_address, runs_log):
    """ Write in the log """
    if new_ip_address and os.path.isfile(runs_log):
        line = "Successful run of {} to update to {} at {}".format(
            __file__, new_ip_address, datetime.now(timezone.utc)
        )
        append_line(runs_log, line)
        return line


FIELDS = ["id", "date", "domainname", "ip"]
MAX = 10000

# MAIN

# The log is in the relative path of the script for convenience
script = os.path.realpath(__file__)
folder = os.path.dirname(script)
# The script executed from the command line by crontab require absolute paths
# Else, the run w'd throw a 'sed: can't read log/ip-log.csv: No such file or directory'
ip_log = os.path.join(folder, "log/ip-log.csv")
runs_log = os.path.join(folder, "log/cron-log.txt")
stored_ip_address = get_log_ip(ip_log)
# Get domain names and password to Namecheap's Dynamic DNS feature
configuration = os.path.join(folder, "config/config.json")
# parse domains:
with open(configuration, "r") as j:
    content = json.loads(j.read())
new_ip_address = update_dynamic_ip()

log_run = write_run(new_ip_address, runs_log)
if log_run:
    print(log_run)
else:
    print("Failed to write the run in the log file.")
