#实现PGP协议
import sm2,sm4
#sm2相关参数：
ellipseN = int('8542D69E4C044F18E8B92435BF6FF7DD297720630485628D5AE74EE7C32E79B7', 16) # g的阶
ellipseP = int('8542D69E4C044F18E8B92435BF6FF7DE457283915C45517D722EDB8B08F1DFC3', 16)
ellipseG = '421DEBD61B62EAB6746434EBC3CC315E32220B3BADD50BDC4C4E6C147FEDD43D0680512BCBB42C07D47349D2153B70C4E5D7FDFCBFA36EA1A85841B9E46E09A2'
ellipse_a = int('787968B4FA32C3FD2417842E73BBFEFF2F3C848B6831D7E0EC65228B3937E498',16)
ellipse_b = int('63E4C6D3B23B0C849CF84241484BFE48F61D59A5B16BA06E6E12D1DA27C5249A',16)
ellipse_a_3 = (ellipse_a + 3) % ellipseP  # 倍点用到的中间值
Fp = 256

#这里使用SM3来对会话密钥进行加密


def tostr_16(num,Len):
    temp=['0']*Len
    n_str=list(hex(num))[2:]
    l=len(n_str)
    for i in range(l):
        temp[Len-1-i]=n_str[l-1-i]
    return ''.join(temp)

#sm2生成公私密钥：
def gen_sm2_keys(len_para):
    #pa是公钥，d是私钥
    d = sm2.get_random_str(len_para)
    Pa = sm2.kG(int(d, 16), ellipseG, len_para)
    return(Pa,d)


#PGP加密：
def PGP_en(keys,msg,Pa):
    #参数说明：SK：sm4的起始密钥，msg待加密信息（msg不要超过128位）
    (C_m,K)=sm4.SM4_en(msg, keys)
    K_str=''
    for i in K:
        K_str+=tostr_16(i, 8)
    C_sk=sm2.encryption(K_str, Pa,len_para,1)
    return(C_sk,C_m)


#PGP解密：
def PGP_dec(C_sk,C_m,d,len_para):
    #解密C_sk
    K=sm2.decryption(C_sk,d,len_para)
    #分割K使之还原
    keys=[]
    for i in range(32):
        temp=K[i*8:i*8+8]
        keys.append(int(temp,16))
    #解密C_m:
    M=sm4.SM4_dec(C_m, keys)
    return M


#PGP开始：
#接收方生成公私密钥：
len_para = int(Fp / 4)
(pk,sk)=gen_sm2_keys(len_para)


#接收方发布公钥（pk），保留私钥（sk）
#文件发送方使用pk加密会话密钥：
msg=0x123456789acdef123456789acdef
keys=[0xA3B1BAC6, 0x56AA3350, 0x677D9197, 0xB27022DC]
(C_sk,C_m)=PGP_en(keys, msg, pk)
print("会话密钥加密为：\n",C_sk,'\n')
print("长度为：\n",len(C_sk))
print("消息加密为：\n",C_m,'\n')
#文件接收方解密：
print("消息解密为：\n")
p=PGP_dec(C_sk, C_m, sk,len_para)
print(hex(p))




    


