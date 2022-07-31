
import sm2,sm3,sm4
import math
import socket
from random import randint
from os.path import commonprefix
#相关参数：
# 选择素域，设置椭圆曲线参数
ellipseN = int('8542D69E4C044F18E8B92435BF6FF7DD297720630485628D5AE74EE7C32E79B7', 16) # g的阶
ellipseP = int('8542D69E4C044F18E8B92435BF6FF7DE457283915C45517D722EDB8B08F1DFC3', 16)
ellipseG = '421DEBD61B62EAB6746434EBC3CC315E32220B3BADD50BDC4C4E6C147FEDD43D0680512BCBB42C07D47349D2153B70C4E5D7FDFCBFA36EA1A85841B9E46E09A2'
ellipse_a = int('787968B4FA32C3FD2417842E73BBFEFF2F3C848B6831D7E0EC65228B3937E498',16)
ellipse_b = int('63E4C6D3B23B0C849CF84241484BFE48F61D59A5B16BA06E6E12D1DA27C5249A',16)
X = 0x421DEBD61B62EAB6746434EBC3CC315E32220B3BADD50BDC4C4E6C147FEDD43D#固定点参数横坐标
Y = 0x0680512BCBB42C07D47349D2153B70C4E5D7FDFCBFA36EA1A85841B9E46E09A2#固定点参数纵坐标
ellipse_a_3 = (ellipse_a + 3) % ellipseP  # 倍点用到的中间值
Fp = 256

def two_p_sign():
    #通信：
    G=str(hex(X))[2:]+str(hex(Y))[2:]
    G_Inv=str(hex(X))[2:]+str(hex(ellipseP-Y%ellipseP))[2:]
    HOST = '127.0.0.1'
    PORT = 1234
    client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    client.bind((HOST, PORT))

    print("user2 已经完成相关配置！")
    print("开始通信\n")
    len_para=int(Fp/4)
    #接收第一轮信息：
    msg,addr=client.recvfrom(1024)
    #print(msg.decode())
    #生成子密钥p2：
    d2=randint(1,ellipseP-1)
    P1=msg.decode()
    #生成共享公钥PK
    PK=sm2.point_add(sm2.kG(sm2.Inverse(d2,ellipseP),P1,len_para),G_Inv,len_para)

    #接收第二轮信息：
    e,addr=client.recvfrom(1024)
    Q1,addr=client.recvfrom(1024)
    e=int(e.decode(),16)#这里e转化为了int类型的变量
    Q1=Q1.decode()

    #计算：
    k2=randint(1, ellipseP-1)
    k3=randint(1, ellipseP-1)
    Q2=sm2.kG(k2,G,len_para)
    res=sm2.point_add(sm2.kG(k3, Q1, len_para),Q2,len_para)


    #计算第三轮交互量：
    x1=int(int(res[:len_para],16))
    y1=int(int(res[len_para:],16))
    r=(x1+e)%ellipseP
    s2=(d2*k3)%ellipseP
    s3=d2*(r+k2)%ellipseP

    #第三轮传输：

    client.sendto(str(r).encode('utf'), addr)
    client.sendto(str(s2).encode('utf'), addr)
    client.sendto(str(s3).encode('utf'),addr)#需要调试

    #end
def two_p_dec():
    #初始配置：
    HOST = '127.0.0.1'
    PORT = 1234
    client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    client.bind((HOST, PORT))
    len_para=int(Fp/4)

    print("user2 已经完成相关配置！")
    print("开始通信\n")
    #生成d2
    d2 = 0x5E35D7D3F3C54DBAC72E61819E730B019A84208CA3A35E4C2E353DFCCB2A3B53
    #接收信息：
    T1,addr=client.recvfrom(1024)
    T1=T1.decode()
    #计算T2：
    T2=sm2.kG(sm2.Inverse(d2, ellipseP), T1, len_para)
    #交互：
    client.sendto(T2.encode('utf-8'), addr)
    #end
# print("2p解密实验：\n")
# two_p_dec()
print("2p签名实验\n")
two_p_sign()


























