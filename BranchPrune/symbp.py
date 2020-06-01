import numpy as np 
import copy
from math import cos, sin, acos, sqrt

def dist(p, q):
	return sqrt(sum((px - qx) ** 2.0 for px, qx in zip(p, q)))

def norm(v):
	return dist(v, np.array([0,0,0]))

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

def sym(n, prune_edges):
	w = [0 for _ in range(n+1)]

	for ep in prune_edges:
		u = ep[0]
		v = ep[1]

		w[u] = max(w[u], v)

	eps = []

	for i in range(n+1):
		if w[i] != 0:
			eps.append((i, w[i]))

	u_bar, v_bar = eps[0]
	S_bar = []

	for k in range(1, len(eps)):
		u_k = eps[k][0]
		v_k = eps[k][1]

		if v_bar >= u_k + 3:
			v_bar = max(v_bar, v_k)
		else:
			S_bar.append((u_bar+4, v_bar))
			u_bar = u_k
			v_bar = v_k

	S_bar.append((u_bar+4, v_bar))

	S = [4]
	i = 0
	for v in range(5, n+1):
		u_bar = S_bar[i][0]
		v_bar = S_bar[i][1]

		if not(u_bar <= v and v <= v_bar):
			S.append(v)

		if v == v_bar and i+1 < len(S_bar):
			i += 1

	return S

def ReflexaoPlano(x1, x2, x3, x):
	v1 = x1 - x2
	v2 = x3 - x2
	n = np.cross(v1, v2)
	n = n/norm(n)
	t = 2*np.dot(n, x2 - x)
	return x + t*n

def TrocaSinal(s, piv):
	x1 = s["X"][piv - 3]
	x2 = s["X"][piv - 2]
	x3 = s["X"][piv - 1]
	t = copy.deepcopy(s)

	for i in range(piv, len(t['X'])):
		t['X'][i] = ReflexaoPlano(x1,x2,x3, t['X'][i])
		t['branch'][i] = 1 - t['branch'][i]

	return t

def EncontraCaminhos(sol, S):
	tree = [0 for _ in range(2**(len(S) + 1))]
	tree[1] = copy.deepcopy(sol)

	piv = 0
	k = 0
	# print("tree[1]:", tree[1] )
	for i in range(1, 2**len(S)):
		if 2**k == i:
			piv = S[k]
			k += 1
		tree[2*i] = copy.deepcopy(tree[i])
		tree[2*i + 1] = copy.deepcopy(TrocaSinal(tree[i], piv))


	return tree[2**len(S):2**(len(S)+1)]


def symbp(n, g, prune_edges):
	sol = bp(n, g, True)
	S = sym(n, prune_edges)
	first_sol = {"X": sol["X"][0], "branch": sol["branch"][0]}
	sol = {"X": [], "branch": []}
	ans = EncontraCaminhos(first_sol, S)

	for a in ans:
		# print(a["branch"][4:n+1])
		sol["X"].append(a["X"])
		sol["branch"].append(a["branch"])

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
	prune_edges = []

	for _ in range(m):
		a, b, c = input().split();
		a = int(a)
		b = int(b)
		c = float(c);

		g[a].append((b, c))
		g[b].append((a, c))
		E.append((a, b, c))
		if a + 3 < b:
			prune_edges.append((a, b))

	sol = symbp(n, g, prune_edges)

	X = sol["X"]
	branch = sol["branch"]

	print(len(X), '\n')

	for i in range(len(X)):
		print(branch[i])
		print(X[i][1:n+1])
		print(isSol(E, n, X[i]))
		print()


if __name__ == '__main__':
	main()