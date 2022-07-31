import sm3,sm2,sm4
#ECMH
ellipseN = int('8542D69E4C044F18E8B92435BF6FF7DD297720630485628D5AE74EE7C32E79B7', 16) # g的阶
ellipseP = int('8542D69E4C044F18E8B92435BF6FF7DE457283915C45517D722EDB8B08F1DFC3', 16)
ellipseG = '421DEBD61B62EAB6746434EBC3CC315E32220B3BADD50BDC4C4E6C147FEDD43D0680512BCBB42C07D47349D2153B70C4E5D7FDFCBFA36EA1A85841B9E46E09A2'
ellipse_a = int('787968B4FA32C3FD2417842E73BBFEFF2F3C848B6831D7E0EC65228B3937E498',16)
ellipse_b = int('63E4C6D3B23B0C849CF84241484BFE48F61D59A5B16BA06E6E12D1DA27C5249A',16)
ellipse_a_3 = (ellipse_a + 3) % ellipseP  # 倍点用到的中间值
Fp = 256

#这里我们调用sm2内部的函数来实现
def tostr_16(num,Len):
    temp=['0']*Len
    n_str=list(hex(num))[2:]
    l=len(n_str)
    for i in range(l):
        temp[Len-1-i]=n_str[l-1-i]
    return ''.join(temp)


def ECMH_add(res,coord,len_para):
    if res=='infinf':
        return  coord
    else:
        return sm2.point_add(res, coord, len_para)

def ECMH_hash(SET):
    #SET内部元素是int类型
    #起始值为无穷远
    len_para=int(Fp/4)
    res="infinf"
    for i in SET:
        X=int(sm3.sm3(i),16)
        temp=(X**2+ellipse_a*X+ellipse_b)%ellipseP
        Y=sm2.QR(temp,ellipseP)
        #接口转化
        X=tostr_16(X, len_para)
        Y=tostr_16(Y, len_para)
        coord=X+Y
        res=ECMH_add(res,coord,len_para)
    return res
SET=(1234,5678)
print(ECMH_hash(SET))



