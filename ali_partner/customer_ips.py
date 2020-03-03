import socket
from os import path
import json
import re

res = []
json_path = path.join(path.dirname(path.abspath(__file__)), "customer_ips.json")
with open(json_path) as json_file:
    data = json.load(json_file)
    for item in data:
        res.append(item)

# PROM.UA
res.append('193.34.169')
# META.UA
res.append('194.0.131')
# LOCALHOST
res.append('127.0.0')
# EMPTY
res.append('0.0.0')
# OFFICE
res.append('178.165.81.178')

res = sorted(res, key=lambda item: socket.inet_aton(item))
ip_pattern = re.compile('|'.join(x.replace('.', '\.') for x in res))
