import numpy as np 
from math import cos, sin, acos, sqrt

def dist(p, q):
	return sqrt(sum((px - qx) ** 2.0 for px, qx in zip(p, q)))

def ComprimentoAresta(g, u, v):
	duv = 0.0

	for i in range(len(g[u])):
		if g[u][i][0] == v:
			duv = g[u][i][1]
			break

	return duv

def PontosIniciais(n, g):
	X = [np.array([0.0, 0.0, 0.0]) for _ in range(n+1)]
	X = np.array(X)

	d12 = ComprimentoAresta(g, 1, 2)
	d13 = ComprimentoAresta(g, 1, 3)
	d23 = ComprimentoAresta(g, 2, 3)

	# print(d12, d13, d23)

	cth = (d12**2 + d23**2 - d13**2)/(2*d12*d23)
	th = acos(cth)
	sth = sin(th)

	X[2] = np.array([-d12, 0.0, 0.0])
	X[3] = np.array([-d12 + d23*cth, d23*sth, 0.0])

	return X

def Intersecao3Esferas(A, ra, B, rb, C, rc):
	x1 = A
	x2 = B
	x3 = C
	d12 = dist(x1, x2)
	d13 = dist(x1, x3)
	d14 = ra
	d23 = dist(x2, x3)
	d24 = rb
	d34 = rc

	r = (x3 - x2)/d23
	k234 = (d24**2 + d23**2 - d34**2)/(2*d23)
	p234 = sqrt(d24**2 - k234**2)

	v = x1 - x2;
	k123 = (d12**2 + d23**2 - d13**2)/(2*d23);
	p123 = sqrt(d12**2 - k123**2)

	alpha = ((k234 - k123)**2 + p234**2 + p123**2)/(2*p234*p123)
	beta  = -(1/(2*p234*p123))

	cw = alpha + beta*d14**2
	sw = sqrt(1 - cw**2);

	X1 = x2 + k234*r + (p234/p123) * ((v - k123*r)*cw + np.cross(r, v)*sw)
	X2 = x2 + k234*r + (p234/p123) * ((v - k123*r)*cw - np.cross(r, v)*sw)

	return np.array([X1, X2])

def CalculaPonto(g, X, b, k):
	d1 = ComprimentoAresta(g, k-3, k)
	d2 = ComprimentoAresta(g, k-2, k)
	d3 = ComprimentoAresta(g, k-1, k)
	# print(k-3, k-2, k-1, k);
	pp = Intersecao3Esferas(X[k-3], d1, X[k-2], d2, X[k-1], d3)
	return pp[b]

def CalculaErro(g, X, v):
	erro = 0.0
	for i in range(len(g[v])):
		u  = g[v][i][0]
		di = g[v][i][1]

		if u < v:
			duv = dist(X[u], X[v])
			erro += (duv - di)**2

	return erro

def bp(n, g, onesol = False):
	delta = 10**-6

	X = PontosIniciais(n, g)
	branch = [0 for _ in range(n+1)]
	branch = np.array(branch)
	vist = [0 for _ in range(n+1)]
	vist[1] = 1
	vist[2] = 1
	vist[3] = 1

	sol = {"X": [], "branch": []}

	k = 4

	while k > 3:
		vist[k] += 1
		X[k] = CalculaPonto(g, X, branch[k], k)
		erro = CalculaErro(g, X, k)

		prune = erro > delta

		if not prune and k == n:
			sol["X"].append(np.copy(X))
			sol["branch"].append(np.copy(branch))
			if onesol:
				return sol

		prune = prune or k == n

		if prune and branch[k] == 1:
			while k > 3 and branch[k] == 1:
				k-=1

		if prune and branch[k] == 0:
			branch[k] = 1
			for i in range(k+1, n+1):
				branch[i] = 0

		if not prune:
			k+=1

	return sol

def isSol(E, n, X):
	s = 0.0

	for e in E:
		u = e[0]
		v = e[1]
		d = e[2]
		Xu = X[u]
		Xv = X[v]
		duv = dist(Xu, Xv)

		s += (duv - d)**2

	return s

def main():
	n, m = map(int, input().split())

	g = [ [] for _ in range(n+1)]
	E = []

	for _ in range(m):
		a, b, c = input().split();
		a = int(a)
		b = int(b)
		c = float(c);

		g[a].append((b, c))
		g[b].append((a, c))
		E.append((a, b, c))

	sol = bp(n, g, False)

	X = sol["X"]
	branch = sol["branch"]

	# print(len(X), '\n')

	for i in range(len(X)):
		print(branch[i])
		print(X[i])
		# print(isSol(E, n, X[i]))
		print()


if __name__ == '__main__':
	main()