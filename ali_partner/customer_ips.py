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
#Google LLC
res.append('35.206')
res.append('35.207')
#ONLINE SAS
res.append('51.158')
res.append('51.159')
#root SA
res.append('195.24.72')
res.append('195.24.73')
res.append('195.24.74')
res.append('195.24.75')
res.append('195.24.76')
res.append('195.24.77')
res.append('195.24.78')
res.append('195.24.79')
#ali
res.append('8.208')
res.append('47.52')
res.append('47.56')
res.append('47.57')
res.append('47.74')
res.append('47.89')
res.append('47.90')
res.append('47.241')
res.append('161.117')

#Akamai Technologies
res.append('2.16')
res.append('2.17')
res.append('2.18')
res.append('2.19')
res.append('2.20')
res.append('2.21')
res.append('2.22')
res.append('2.23')

res = sorted(res, key=lambda item: socket.inet_aton(item))
ip_pattern = re.compile('|'.join('^%s' % x.replace('.', '\.') for x in res))

# for ip in ['192.168.2.16', '127.0.0.1', '176.107.52.167', '176.107.52.168', '50.7.93.85']:
#     if ip_pattern.search(ip) is not None:
#         print(ip)
