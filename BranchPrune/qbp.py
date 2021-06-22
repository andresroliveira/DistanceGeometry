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

def multiply(A, B, C): # C = A * B 
    for i in range(4):
        for j in range(4):
            aux = 0.0
            for k in range(4):
                aux += A[i][k]*B[k][j]
            C[i][j] = aux

def PosicaoAtomo(B):
    return np.array([B[0][3], B[1][3], B[2][3]])

def copy(B, C):
    for i in range(4):
        for j in range(4):
            B[i][j] = C[i][j]

def h(i):
    x = [np.array([0.0,0.0,0.0]) for _ in range(n+1)]
    x[2] = np.array([ -d[1][2], 0, 0 ])
    x[3] = np.array([ -d[1][2] + d[2][3]*cos(th[3]), d[2][3]*sin(th[3]), 0])

    B2 = [[-1,0,0,-d[1][2]], [0,1,0,0], [0,0,-1,0], [0,0,0,1]]
    ct = cos(th[3])
    st = sin(th[3])
    di = d[2][3]
    B3 = [[-ct, -st, 0, -di*ct], [st, -ct, 0, di*st], [0,0,1,0],[0,0,0,1]]
    B = [[1,0,0,0], [0,1,0,0], [0,0,1,0], [0,0,0,1]]
    multiply(B2, B3, B); # B = B2 * B3

    for k in range(4, n+1):
        sgn = 1
        if i & (1 << (n-k)) == 0:
            sgn = 0
        ct,st = cos(th[k]),sin(th[k])
        di = d[k-1][k]
        sw = (-1)**sgn * sqrt(1 - cw[k]**2)

        A = [[-ct, -st, 0, -di*ct], [st*cw[k], -ct*cw[k], -sw, di*st*cw[k]], [st*sw, -ct*sw, cw[k], di*st*sw], [0, 0, 0, 1]]
        C = [[1,0,0,0], [0,1,0,0], [0,0,1,0], [0,0,0,1]]
        multiply(B, A, C) # C = B * A
        x[k] = PosicaoAtomo(C)
        copy(B, C)

    return np.array(x)

def g(x):
    s = 0.0

    for e in E:
        a, b, c = e
        xa = x[a]
        xb = x[b]
        dab = dist(xa, xb)
        s += (dab**2 - c**2)**2

    return s

def psi(xi):
    p1 = n*n*((n*5)**4 + 5**4)
    p2 = log(DEL/p1)/log(1-EPS)
    return (xi/p1)**(1/p2)


def f(i):
    return 1 - floor(psi(g(h(i)))+ EPS)


def main():
    global EPS
    EPS = 2/3
    global DEL
    DEL = 1e-4
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

    # print(cw[1:n+1], th[1:n+1])

    for i in range(2**(n-3)):
        fi = f(i)
        print("f(", toBin(i),") = ", fi, sep='')
        if fi == 1:
            print(h(i)[1:n+1])
            print()


if __name__ == '__main__':
    main()
