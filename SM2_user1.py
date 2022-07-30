import sm3
import sm2 
import sys
import math
import time
import socket
import random
import binascii
from random import randint
from os.path import commonprefix
#相关参数：
#选择素域，设置椭圆曲线参数：
ellipseN = int('8542D69E4C044F18E8B92435BF6FF7DD297720630485628D5AE74EE7C32E79B7', 16) # g的阶
ellipseP = int('8542D69E4C044F18E8B92435BF6FF7DE457283915C45517D722EDB8B08F1DFC3', 16)
ellipseG = '421DEBD61B62EAB6746434EBC3CC315E32220B3BADD50BDC4C4E6C147FEDD43D0680512BCBB42C07D47349D2153B70C4E5D7FDFCBFA36EA1A85841B9E46E09A2'
ellipse_a = int('787968B4FA32C3FD2417842E73BBFEFF2F3C848B6831D7E0EC65228B3937E498',16)
ellipse_b = int('63E4C6D3B23B0C849CF84241484BFE48F61D59A5B16BA06E6E12D1DA27C5249A',16)
X = 0x421DEBD61B62EAB6746434EBC3CC315E32220B3BADD50BDC4C4E6C147FEDD43D#固定点参数横坐标
Y = 0x0680512BCBB42C07D47349D2153B70C4E5D7FDFCBFA36EA1A85841B9E46E09A2#固定点参数纵坐标
ellipse_a_3 = (ellipse_a + 3) % ellipseP  # 倍点用到的中间值
Fp = 256







def KDF(z,klen):
    tmp = 1
    key = ''
    for i in range(math.ceil(klen/256)):
        t = hex(int(z + '{:032b}'.format(tmp),2))[2:]
        t=int(t,16)
        key = key + hex(int(sm3.sm3(msg)(t),16))[2:]
        tmp = tmp + 1
    key ='0'*((256-(len(bin(int(key,16))[2:])%256))%256)+bin(int(key,16))[2:]
    return key[:klen]

def two_p_sign():
    #通信：
    HOST = '127.0.0.1'
    PORT = 1234
    client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    try:
        client.connect((HOST, PORT))
        print("user1 完成相关配置")
    except Exception:
        print('Connection failed!')
        sys.exit()
    else:
        len_para=int(Fp/4)
        print("开始通信：")
        addr = (HOST, PORT)
        #生成子密钥：
        d1=randint(1, ellipseP-1)
        #计算第一轮信息
        G=str(hex(X))[2:]+str(hex(Y))[2:]
        msg=sm2.kG(sm2.Inverse(d1, ellipseP),G,len_para)#注意这里返回的是一个字符串（str）  
        client.sendto(msg.encode('utf-8'), addr)

        #生成身份确认信息：
        m="I'm sun spike!"
        m=hex(int(binascii.b2a_hex(m.encode()).decode(), 16)).upper()[2:]
        e=sm3.sm3(int(m,16))
        #生成k1
        k1=randint(1, ellipseP-1)
        Q1=sm2.kG(k1,G,len_para)
        #第二轮传输信息：

        client.sendto(e.encode('utf-8'), addr)#注意这里e的类型是str
        client.sendto(Q1.encode('utf-8'),addr)#注意这里Q1的类型是str

        #接收信息：


        r,addr=client.recvfrom(1024)
        s2,addr=client.recvfrom(1024)
        s3,addr=client.recvfrom(1024)

        r=int(r,10)
        s2=int(s2,10)
        s3=int(s3,10)

        #生成签名：

        s=((d1*k1)*s2+d1*s3-r)%ellipseP
        if s!=0 and s!=ellipseP-r:
            print("签名为：\n")
            print((hex(r),hex(s)))
def two_p_dec():
     #通信：
    HOST = '127.0.0.1'
    PORT = 1234
    client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    try:
        client.connect((HOST, PORT))
        print("user1 完成相关配置")
    except Exception:
        print('Connection failed!')
        sys.exit()
    else:
        len_para=int(Fp/4)
        print("开始通信：")
        addr = (HOST, PORT)
        #生成d1
        d1 = 0x6FCBA2EF9AE0AB902BC3BDE3FF915D44BA4CC78F88E2F8E7F8996D3B8CCEEDEE
        
        # 获取密文 C = C1||C2||C3
        C1 = (0x26518fd38aa48284d30ce6e5c42d34b57840d1a03b64947b6a300ffe81797cc8,
            0x208be67614cc4562c219dc0cc060aeca05c52bfc1a990f9f02a4ed972ee91df6)
        C2 = 0x4e1d4176afeec9e0ddc7702c1bd9a0393b54bb
        C3 = 0xDF31DE4A7A859CF0E06297030D4F8DE7ACA5D182D89FE278423F7D12F9C3E03C
        klen = len(hex(C2)[2:])*4
        #计算：
        C1_Inv=str(hex(C1[0]))[2:]+str(hex(ellipseP-C1[1]%ellipseP))[2:]
        C1=str(hex(C1[0]))[2:]+str(hex(C1[1]))[2:]
        T1=sm2.kG(sm2.Inverse(d1,ellipseP),C1,len_para)

        client.sendto(T1.encode('utf-8'), addr)
        #接收消息：
        T2,addr=client.recvfrom(1024)
        T2=T2.decode()

        #计算：
        NEW_point=sm2.point_add(T2, C1_Inv, len_para)
        t=sm2.KDF(NEW_point, klen)
        M2 = C2 ^ int(t,16)
        temp=NEW_point[:len_para].upper()+hex(M2)[2:].upper()+NEW_point[len_para:].upper()
        temp=int(temp,16)
        u=sm3.sm3(temp)
        print("the result is: \n",hex(M2))    
two_p_dec()





    





































