# import sm3
# import sm2 
# import sys
# import math
# import time
# import socket
# import random
# import binascii
# from random import randint
# from os.path import commonprefix
# ellipseN = int('8542D69E4C044F18E8B92435BF6FF7DD297720630485628D5AE74EE7C32E79B7', 16) # g的阶
# ellipseP = int('8542D69E4C044F18E8B92435BF6FF7DE457283915C45517D722EDB8B08F1DFC3', 16)
# ellipseG = '421DEBD61B62EAB6746434EBC3CC315E32220B3BADD50BDC4C4E6C147FEDD43D0680512BCBB42C07D47349D2153B70C4E5D7FDFCBFA36EA1A85841B9E46E09A2'
# ellipse_a = int('787968B4FA32C3FD2417842E73BBFEFF2F3C848B6831D7E0EC65228B3937E498',16)
# ellipse_b = int('63E4C6D3B23B0C849CF84241484BFE48F61D59A5B16BA06E6E12D1DA27C5249A',16)
# X = 0x421DEBD61B62EAB6746434EBC3CC315E32220B3BADD50BDC4C4E6C147FEDD43D#固定点参数横坐标
# Y = 0x0680512BCBB42C07D47349D2153B70C4E5D7FDFCBFA36EA1A85841B9E46E09A2#固定点参数纵坐标
# ellipse_a_3 = (ellipse_a + 3) % ellipseP  # 倍点用到的中间值
# Fp = 256


# len_para=int(Fp/4)
# print("开始通信：")
# #生成子密钥：
# d1=randint(1, ellipseP-1)
# #计算第一轮信息
# G=str(hex(X))[2:]+str(hex(Y))[2:]
# msg=sm2.kG(sm2.Inverse(d1, ellipseP),G,len_para)#注意这里返回的是一个字符串（str）
def _toint(STR):
    s=''
    for i in STR:
        temp=ord(i)
        s=s+str(temp)
    return int(s,10)
print(_toint('123'))
