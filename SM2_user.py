import sm3
import sys
import math
import time
import socket
import random
import binascii
from random import randint
from os.path import commonprefix



#开始通信：
HOST = '127.0.0.1'
PORT = 1234
client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

try:
    client.connect((HOST, PORT))
    print("user connected!")
except Exception:
    print('Connection failed!')
    sys.exit()
else:
    # 生成子私钥 d1
    d1 = randint(1,n-1)
    
    # 计算P1 = d1^(-1) * G
    P1 = epoint_mult(X,Y,invert(d1,p))
    x,y = hex(P1[0]),hex(P1[1])
    
    # 向客户2发送P1
    addr = (HOST, PORT)
    client.sendto(x.encode('utf-8'), addr)
    client.sendto(y.encode('utf-8'), addr)

    #计算ZA
    m = "hello,this is spike!"
    m = hex(int(binascii.b2a_hex(m.encode()).decode(), 16)).upper()[2:]
    vows = "julia is my love ,and I always love her, but she has gone...... "
    vows = hex(int(binascii.b2a_hex(vows.encode()).decode(), 16)).upper()[2:]
    ENTL_A = '{:04X}'.format(len(vows) * 4)
    ma = ENTL_A + vows + '{:064X}'.format(a) + '{:064X}'.format(b) + '{:064X}'.format(X) + '{:064X}'.format(Y)
    ZA = sm3.SM3(ma)
    e = sm3.SM3(ZA + m)
    
    # 生成随机数k1
    k1 = randint(1,n-1)

    # 计算Q1 = k1 * G
    Q1 = epoint_mult(X,Y,k1)
    x,y = hex(Q1[0]),hex(Q1[1])

    # 向客户2发送Q1,e
    client.sendto(x.encode('utf-8'),addr)
    client.sendto(y.encode('utf-8'),addr)
    client.sendto(e.encode('utf-8'),addr)

    # 从客户2接收r,s2,s3
    r,addr = client.recvfrom(1024)
    r = int(r.decode(),16)
    s2,addr = client.recvfrom(1024)
    s2 = int(s2.decode(),16)
    s3,addr = client.recvfrom(1024)
    s3 = int(s3.decode(),16)

    # 计算s
    s=((d1 * k1) * s2 + d1 * s3 - r)%n
    if s!=0 or s!= n - r:
        print("Sign:")
        print((hex(r),hex(s)))
    client.close()