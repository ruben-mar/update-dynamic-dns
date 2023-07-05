#!/usr/bin/env python3
# Check if the server is connected to the Internet


import requests

def is_cnx_active(timeout):
    try:
        requests.head("https://www.wikipedia.org/", timeout=timeout)
        return True
    except requests.ConnectionError:
        return False
