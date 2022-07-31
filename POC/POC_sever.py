import SM3
import sys
import json
import random
import socket
from os.path import commonprefix

d = 7
n = 23
HOST = ''
PORT = 1234
client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
client.bind((HOST, PORT))

print("Server connected!")

# 从客户端接收数据
k,addr = client.recvfrom(1024)
k = int(k.decode(),16)
v,addr = client.recvfrom(1024)
v = int(v.decode(),16)

# create key-value table
table = []
for i in range(20000 ,20000 + pow(2,16)):
    h = SM3._hash(str(i) + str(i))
    table.append(h)   
V = []
for m in table:
    if m[:2] == k:
        V.append((pow(int(m,16),d))%n)

print("V:",V)

# 计算H_ab
H_ab=(pow(v,d))%n

# 向客户端发送H_ab与data set
client.sendto(hex(H_ab).encode(),addr)
json_v = json.dumps(V)
client.sendto(json_v.encode('utf-8'),addr)
client.close()

print("Server closed!")