import sm3
from sm2 import Inverse
import sys
import json
import random
import socket
from os.path import commonprefix


def _toint(STR):
    s=''
    for i in STR:
        temp=ord(i)
        s=s+str(temp)
    return int(s,10)


d = 5
n = 23
name = 'usr'
password = '123456'

HOST = '127.0.0.1'
PORT = 1234
client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

try:
    client.connect((HOST, PORT))
    print("客户端已连接")
except Exception:
    print('连接失败')
    sys.exit()
else:
    name_int=_toint(name)
    password_int=_toint(password)
    name_password=_toint(name+password)
    # 客户端计算key-value
    h = sm3.sm3(name_password)
    k = h[:2]
    v = str((pow(int(h,16),d))%n)

    # 向服务端发送k与v
    addr = (HOST, PORT)
    client.sendto(k.encode('utf-8'), addr)
    client.sendto(v.encode('utf-8'), addr)

    # 从服务端接收H_ab与data set S
    H_ab,addr = client.recvfrom(1024 * 5)
    H_ab = int(H_ab.decode(),16)
    json_v,addr = client.recvfrom(1024 * 5)
    json_v = json_v.decode('utf-8')
    S = json.loads(json_v)
    print("S:",S)

    # 计算并检查H_b是否在S中
    H_b = (pow(H_ab,Inverse(d,n)))%n
    tmp = 0
    for item in S:
        b = item
        if b == H_b:
            tmp = 1
    if tmp == 0:
        print('账户:',name,'安全!')
    else:
        print('账户:',name,'不安全！')