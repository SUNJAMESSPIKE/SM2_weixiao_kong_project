from math import ceil
from random import choice

IV = "7380166f 4914b2b9 172442d7 da8a0600 a96f30bc 163138aa e38dee4d b0fb0e4e"
IV = int(IV.replace(" ", ""), 16)
a = []
for i in range(0, 8):
    a.append(0)
    a[i] = (IV >> ((7 - i) * 32)) & 0xFFFFFFFF
IV = a


def out_hex(list1):
    for i in list1:
        print("%08x" % i)
    print("\n")


def rotate_left(a, k):
    k = k % 32
    return ((a << k) & 0xFFFFFFFF) | ((a & 0xFFFFFFFF) >> (32 - k))


T_j = []
for i in range(0, 16):
    T_j.append(0)
    T_j[i] = 0x79cc4519
for i in range(16, 64):
    T_j.append(0)
    T_j[i] = 0x7a879d8a


def FF_j(X, Y, Z, j):
    if 0 <= j < 16:
        ret = X ^ Y ^ Z
    elif 16 <= j < 64:
        ret = (X & Y) | (X & Z) | (Y & Z)
    return ret


def GG_j(X, Y, Z, j):
    if 0 <= j < 16:
        ret = X ^ Y ^ Z
    elif 16 <= j < 64:
        # ret = (X | Y) & ((2 ** 32 - 1 - X) | Z)
        ret = (X & Y) | ((~ X) & Z)
    return ret


def P_0(X):
    return X ^ (rotate_left(X, 9)) ^ (rotate_left(X, 17))


def P_1(X):
    return X ^ (rotate_left(X, 15)) ^ (rotate_left(X, 23))


def CF(V_i, B_i):
    W = []
    for i in range(16):
        weight = 0x1000000
        data = 0
        for k in range(i * 4, (i + 1) * 4):
            data = data + B_i[k] * weight
            weight = int(weight / 0x100)
        W.append(data)

    for j in range(16, 68):
        W.append(0)
        W[j] = P_1(W[j - 16] ^ W[j - 9] ^ (rotate_left(W[j - 3], 15))) ^ (rotate_left(W[j - 13], 7)) ^ W[j - 6]
        str1 = "%08x" % W[j]
    W_1 = []
    for j in range(0, 64):
        W_1.append(0)
        W_1[j] = W[j] ^ W[j + 4]
        str1 = "%08x" % W_1[j]

    A, B, C, D, E, F, G, H = V_i
    """
    print "00",
    out_hex([A, B, C, D, E, F, G, H])
    """
    for j in range(0, 64):
        SS1 = rotate_left(((rotate_left(A, 12)) + E + (rotate_left(T_j[j], j))) & 0xFFFFFFFF, 7)
        SS2 = SS1 ^ (rotate_left(A, 12))
        TT1 = (FF_j(A, B, C, j) + D + SS2 + W_1[j]) & 0xFFFFFFFF
        TT2 = (GG_j(E, F, G, j) + H + SS1 + W[j]) & 0xFFFFFFFF
        D = C
        C = rotate_left(B, 9)
        B = A
        A = TT1
        H = G
        G = rotate_left(F, 19)
        F = E
        E = P_0(TT2)

        A = A & 0xFFFFFFFF
        B = B & 0xFFFFFFFF
        C = C & 0xFFFFFFFF
        D = D & 0xFFFFFFFF
        E = E & 0xFFFFFFFF
        F = F & 0xFFFFFFFF
        G = G & 0xFFFFFFFF
        H = H & 0xFFFFFFFF
        """
        str1 = "%02d" % j
        if str1[0] == "0":
            str1 = ' ' + str1[1:]
        print str1,
        out_hex([A, B, C, D, E, F, G, H])
        """

    V_i_1 = []
    V_i_1.append(A ^ V_i[0])
    V_i_1.append(B ^ V_i[1])
    V_i_1.append(C ^ V_i[2])
    V_i_1.append(D ^ V_i[3])
    V_i_1.append(E ^ V_i[4])
    V_i_1.append(F ^ V_i[5])
    V_i_1.append(G ^ V_i[6])
    V_i_1.append(H ^ V_i[7])
    return V_i_1


def hash_msg(msg):
    # print(msg)
    len1 = len(msg)
    reserve1 = len1 % 64
    msg.append(0x80)
    reserve1 = reserve1 + 1
    # 56-64, add 64 byte
    range_end = 56
    if reserve1 > range_end:
        range_end = range_end + 64

    for i in range(reserve1, range_end):
        msg.append(0x00)

    bit_length = (len1) * 8
    bit_length_str = [bit_length % 0x100]
    for i in range(7):
        bit_length = int(bit_length / 0x100)
        bit_length_str.append(bit_length % 0x100)
    for i in range(8):
        msg.append(bit_length_str[7 - i])

    # print(msg)

    group_count = round(len(msg) / 64)

    B = []
    for i in range(0, group_count):
        B.append(msg[i * 64:(i + 1) * 64])

    V = []
    V.append(IV)
    for i in range(0, group_count):
        V.append(CF(V[i], B[i]))

    y = V[i + 1]
    result = ""
    for i in y:
        result = '%s%08x' % (result, i)
    return result


def str2byte(msg):  # 字符串转换成byte数组
    ml = len(msg)
    msg_byte = []
    msg_bytearray = msg.encode('utf-8')
    for i in range(ml):
        msg_byte.append(msg_bytearray[i])
    return msg_byte


def byte2str(msg):  # byte数组转字符串
    ml = len(msg)
    str1 = b""
    for i in range(ml):
        str1 += b'%c' % msg[i]
    return str1.decode('utf-8')


def hex2byte(msg):  # 16进制字符串转换成byte数组
    ml = len(msg)
    if ml % 2 != 0:
        msg = '0' + msg
    ml = int(len(msg) / 2)
    msg_byte = []
    for i in range(ml):
        msg_byte.append(int(msg[i * 2:i * 2 + 2], 16))
    return msg_byte


def byte2hex(msg):  # byte数组转换成16进制字符串
    ml = len(msg)
    hexstr = ""
    for i in range(ml):
        hexstr = hexstr + ('%02x' % msg[i])
    return hexstr


def Hash_sm3(msg, Hexstr=0):
    if (Hexstr):
        msg_byte = hex2byte(msg)
    else:
        msg_byte = str2byte(msg)
    return hash_msg(msg_byte)


def KDF(Z, klen):  # Z为16进制表示的比特串（str），klen为密钥长度（单位byte）
    klen = int(klen)
    ct = 0x00000001
    rcnt = ceil(klen / 32)
    Zin = hex2byte(Z)
    Ha = ""
    for i in range(rcnt):
        msg = Zin + hex2byte('%08x' % ct)
        # print(msg)
        Ha = Ha + hash_msg(msg)
        # print(Ha)
        ct += 1
    return Ha[0: klen * 2]

#sm2的代码：
# 选择素域，设置椭圆曲线参数
ellipseN = int('8542D69E4C044F18E8B92435BF6FF7DD297720630485628D5AE74EE7C32E79B7', 16) # g的阶
ellipseP = int('8542D69E4C044F18E8B92435BF6FF7DE457283915C45517D722EDB8B08F1DFC3', 16)
ellipseG = '421DEBD61B62EAB6746434EBC3CC315E32220B3BADD50BDC4C4E6C147FEDD43D0680512BCBB42C07D47349D2153B70C4E5D7FDFCBFA36EA1A85841B9E46E09A2'
ellipse_a = int('787968B4FA32C3FD2417842E73BBFEFF2F3C848B6831D7E0EC65228B3937E498',16)
ellipse_b = int('63E4C6D3B23B0C849CF84241484BFE48F61D59A5B16BA06E6E12D1DA27C5249A',16)
ellipse_a_3 = (ellipse_a + 3) % ellipseP  # 倍点用到的中间值
Fp = 256

# 随机字符
def get_random_str(strlen):
    letter = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'a', 'b', 'c', 'd', 'e', 'f']
    str = ''
    for i in range(strlen):
        a = choice(letter)
        str = str + a
    return str

# 扩展欧几里得算法
def exgcd(a, b):
    old_s, s = 1, 0
    old_t, t = 0, 1
    old_r, r = a, b
    if b == 0:
        return 1, 0, a
    else:
        while r != 0:
            q = old_r // r
            old_r, r = r, old_r - q * r
            old_s, s = s, old_s - q * s
            old_t, t = t, old_t - q * t
    return old_s


def MjrCal(Mj, mj):
    s = exgcd(Mj, mj)
    while s < 1:
        s += mj
    return s

#点乘
def kG(k, point, length):
    P = point
    Q = point
    k1 = bin(k)
    start = str(k1).find('1')
    for i in range(len(k1), start):
        Q = point_double(Q, length)
        if k1[i] == 1:
            Q = point_add(Q, P, length)
    return Q

#点加
def point_add(P, Q, length):
    Px = int(P[:length], 16)
    Py = int(P[length:], 16)
    Qx = int(Q[:length], 16)
    Qy = int(Q[length:], 16)

    lamda = (Qy - Py) * MjrCal(Qx - Px, ellipseP) % ellipseP # 方程初始化
    xNew = pow(lamda, 2) - Px - Qx
    yNew = lamda * (Px - xNew) - Py
    xNew = xNew % ellipseP
    yNew = yNew % ellipseP
    xNew = hex(xNew)
    yNew = hex(yNew)
    return str(xNew)[2:] + str(yNew)[2:]

#自加
def point_double(point, length):
    xPoint = int(point[:length], 16)
    yPoint = int(point[length:], 16)
    lamda = (3 * pow(xPoint, 2) + ellipse_a) * MjrCal(2 * yPoint, ellipseP) % ellipseP

    xNew = pow(lamda, 2) - 2 * xPoint
    yNew = lamda * (xPoint - xNew) - yPoint
    xNew = xNew % ellipseP
    yNew = yNew % ellipseP
    xNew = hex(xNew)
    yNew = hex(yNew)
    return str(xNew)[2:] + str(yNew)[2:]


#判读是否为二次剩余
def isQR(n,p):
    return pow(n, (p - 1) // 2, p)


#求解二次剩余
def QR(n,p):
    if isQR(n, p)==-1:
        return
    if p % 4 == 3:
        return pow(n, (p + 1) // 4, p)
    q = p - 1
    s = 0
    while q % 2 == 0:
        q = q // 2
        s += 1
    for z in range(2, p):
        if isQR(z, p) == p - 1:
            c = pow(z, q, p)
            break
    r = pow(n, (q + 1) // 2, p)
    t = pow(n, q, p)
    m = s
    if t % p == 1:
        return r
    else:
        i = 0
        while t % p != 1:
            temp = pow(t, 2 ** (i + 1), p)
            i += 1
            if temp % p == 1:
                b = pow(c, 2 ** (m - i - 1), p)
                r = r * b % p
                c = b * b % p
                t = t * c % p
                m = i
                i = 0
        return r

def encryption(M, PA, length, strHex=0):  # 加密函数，M消息，PA公钥
    if strHex:
        msg = M  # 输入消息本身是16进制字符串
    else:
        msg = M.encode('utf-8')
        msg = msg.hex()  # 消息转化为16进制字符串
    k = get_random_str(length)

    C1 = kG(int(k, 16), ellipseG, length)
    # print(len(C1))
    # print(length)

    if str(PA)[:length] == '0' and str(PA)[length:] == '0':
        print("Infinite point!")
        exit(1)
    xy = kG(int(k, 16), PA, length)

    x2 = xy[0:length]
    y2 = xy[length:2 * length]
    lenMsg = len(msg)

    t = KDF(xy, lenMsg / 2)

    if int(t, 16) == 0:
        temp = encryption(M, PA, length)
        return temp
    else:
        form = '%%0%dx' % lenMsg
        C2 = form % (int(msg, 16) ^ int(t, 16))

        C3 = Hash_sm3(x2 + msg + y2, 1)

        return C1 + C3 + C2


def decryption(C, DA, length):  # 解密函数，C密文（16进制字符串），DA私钥
    len_2 = 2 * length
    len_3 = len_2 + 64
    C1 = C[0:len_2]

    x = int(C1[:length], 16)
    y = int(C1[length:], 16)
    if pow(y, 2) % ellipseP != (pow(x, 3) + ellipse_a * x + ellipse_b) % ellipseP:
        print("C1不满足方程")
        exit(1)
    if (C1[:length],C1[length:]) == (0,0):
        print("Infinite point!")
        exit(1)
    C3 = C[len_2:len_3]
    C2 = C[len_3:]
    xy = kG(int(DA, 16), C1, length)

    x2 = xy[0:length]
    y2 = xy[length:len_2]
    cl = len(C2)

    t = KDF(xy, cl / 2)

    if int(t, 16) == 0:
        return None
    else:
        form = '%%0%dx' % cl
        M = form % (int(C2, 16) ^ int(t, 16))

        u = Hash_sm3(x2 + M + y2, 1)
        if u == C3:
            return M
        else:
            return None

def verification(i):
    len_para = int(Fp / 4)
    # print(len_para)
    e = get_random_str(len_para)
    d = get_random_str(len_para)
    k = get_random_str(len_para)

    Pa = kG(int(d, 16), ellipseG, len_para)
    print("Public key is :")
    print(Pa)
    print("\nSecret key is :")
    print(d)
    print("\nSecret is :")
    print(e)

    C = encryption(e, Pa, len_para, 0)
    print("\nCipher text is :")
    print(C)

    m = decryption(C, d, len_para)
    print(m)
    print(m)
    M = bytes.fromhex(m)
    print(M)
    print("\nDecrypt secret is :")
    print(M.decode())

def gcd(a,b):
    if a<b:
        t=a
        a=b
        b=t
    while a%b!=0:
        temp=a%b
        a=b
        b=temp
    return b

def Inverse(a,m):#
    Gcd=gcd(a, m)
    if Gcd!=1:
        return None
    u1,u2,u3 = 1,0,a
    v1,v2,v3 = 0,1,m
    while v3!=0:
        q = u3//v3
        v1,v2,v3,u1,u2,u3 = (u1-q*v1),(u2-q*v2),(u3-q*v3),v1,v2,v3
    return u1%m

