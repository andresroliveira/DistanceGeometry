import numpy as np
from math import *

def dist(p, q):
    return sqrt(sum((px - qx) ** 2.0 for px, qx in zip(p, q)))

def toBin(i):
    s = ""
    k = 0

    while (1 << k) <= i:
        if i & (1 << k) == 0:
            s += "0"
        else:
            s += "1"

        k += 1

    while(len(s) < n-3):
        s += "0"

    s = s[::-1]
    return s

def h(i):
    ori = np.array([0.0,0.0,0.0,1.0])
    x = np.array([np.array([0.0,0.0,0.0]) for _ in range(n+1)])
    x[2] = np.array([ -d[1][2], 0, 0 ])
    x[3] = np.array([ -d[1][2] + d[2][3]*cos(th[3]), d[2][3]*sin(th[3]), 0])

    B2 = np.array([[-1,0,0,-d[1][2]], [0,1,0,0], [0,0,-1,0], [0,0,0,1]])
    ct = cos(th[3])
    st = sin(th[3])
    di = d[2][3]
    B3 = np.array([[-ct, -st, 0, -di*ct], [st, -ct, 0, di*st], [0,0,1,0],[0,0,0,1]])
    B = B2.dot(B3)

    for k in range(4, n+1):
        sgn = 1
        if i & (1 << (n-k)) == 0:
            sgn = 0
        ct,st = cos(th[k]),sin(th[k])
        di = d[k-1][k]
        sw = (-1)**sgn * sqrt(1 - cw[k]**2)
        Bi = np.array([[-ct, -st, 0, -di*ct], [st*cw[k], -ct*cw[k], -sw, di*st*cw[k]], [st*sw, -ct*sw, -cw[k], di*st*sw], [0,0,0,1]])
        B = B.dot(Bi)
        xi = B.dot(ori)
        x[k] = np.array([ xi[0]/xi[3], xi[1]/xi[3], xi[2]/xi[3] ])
    return x

def g(x):
    s = 0.0

    for e in E:
        a, b, c = e
        xa = x[a]
        xb = x[b]
        dab = dist(xa, xb)
        s += (dab - c)**2

    return s

def f(i):
    EPS = 1/2
    DEL = 10**-6

    p1 = n*n*((n*5)**4 + 5**4)
    p2 = log(DEL/p1)/log(1-EPS)

    return (1 - floor((g(h(i))/p1)**(1/p2)+ EPS))


def main():
    global n
    n, m = map(int, input().split())
    global E
    E = []
    global d
    d = np.zeros( (n+1, n+1) )
    for _ in range(m):
        a, b, c = input().split()
        a = int(a)
        b = int(b)
        c = float(c)
        E.append((a, b, c))
        d[a][b] = c
        d[b][a] = c

    global th
    th = np.zeros(n+1)
    for i in range(3, n+1):
        th[i] = acos( (d[i-1][i]**2 + d[i-2][i-1]**2 - d[i-2][i]**2)/(2*d[i-1][i]*d[i-2][i-1]) )

    global cw
    cw = np.zeros(n+1)
    for i in range(4,n+1):
        rij = d[i-3][i-2]
        rjk = d[i-2][i-1]
        rkl = d[i-1][i]
        rjl = d[i-2][i]
        ril = d[i-3][i]
        st  = sin(th[i-1])
        ct  = cos(th[i-1])

        num = rij**2 + rjl**2 - ril**2 - rij*(rjl**2 + rjk**2 - rkl**2)*ct/rjk
        den = rij*sqrt(4*rjl**2 * rjk**2 - (rjl**2 + rjk**2 - rkl**2)**2)*st/rjk
        cw[i] = num/den

    for i in range(2**(n-3)):
        print("f(", toBin(i),") = ", f(i), sep='')
        print(h(i)[1:n+1])
        print()


if __name__ == '__main__':
    main()
