import random
#椭圆曲线参数
a = 2
b = 2    
p = 17
x = 5
y = 1
g = [x, y]
n = 19
#辗转相除法求最大公因子
def gcd(a,b):
    r=a%b
    while(r!=0):
        a=b
        b=r
        r=a%b
    return b

#扩展欧几里得求模逆
def Inverse(a, m): 
    if gcd(a, m) != 1:
        return None #如果a和m不互质，则不存在模逆
    u1, u2, u3 = 1, 0, a
    v1, v2, v3 = 0, 1, m
    while v3 != 0:
        q = u3 // v3 # //是整数除法运算符
        v1 , v2, v3, u1 , u2, u3 = (u1 - q * v1), (u2 - q * v2), (u3 - q * v3), v1 , v2, v3
    return u1 % m

#点加
def point_add(P,Q):
    if (P == 0):
        return Q
    if (Q == 0):
        return P
    if P == Q:
        t1 = (3 * (P[0]**2) + a)
        t2 = Inverse(2 * P[1], p)
        k = (t1 * t2) % p 
    else:
        t1 = (P[1] - Q[1])
        t2 = (P[0] - Q[0])
        k = (t1 * Inverse(t2,p)) % p 

    X = (k * k - P[0] - Q[0]) % p 
    Y = (k * (P[0] - X) - P[1]) % p 
    Z = [X,Y]
    return Z


#点乘
def epoint_mul(k, g):
    if k == 0:
        return 0
    if k == 1:
        return g
    r = g
    while (k >= 2):
        r = point_add(r, g)
        k = k - 1
    return r

#签名
def signature(m,d):
    k = random.randint(1,n-1)
    Z = epoint_mul(k,g)
    r = Z[0]%n #r = x mod n
    e = hash(m)
    s = (Inverse(k, n) * (e + d * r)) % n
    return r,s

#验签
def verify(r,s,m,pk):
    e = hash(m)
    t = Inverse(s,n)#t = s^(-1) mod n
    Z = point_add(epoint_mul((e * t) % n,g),epoint_mul((r * t) % n,pk))
    if(Z!=0):
        if(Z[0]%n == r):
            return True
        else:
            return False
    return False


m = 'spike!'
e = hash(m)
d = 7
pk = epoint_mul(d, g)
r,s = signature(m,d)
print("公钥为：",pk,'\n','私钥为:',d,'\n')
print("签名值为：",r,s)
if(verify(r,s,m,pk)):
    print('验证成果!')
else: print('验证失败!')