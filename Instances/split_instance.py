import numpy as np

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

def PrintInstance(it):
	print(it['n'], it['m'])

	for edge in it['edges']:
		u = edge[0]
		v = edge[1]
		d = edge[2]

		print("%5d %5d" %(u, v), end = ' ')
		print(d)

def SplitInstance(n, g, prune_edges):
	S = sym(n, prune_edges)
	S.append(n+1)

	# print(S)

	h = []

	for i in range(1, len(S)):
		u = S[i-1]-3
		v = S[i]

		it = {"n": v-u, "m": 0, "edges": []}

		for j in range(u, v):
			for k, d in g[j]:
				if j < k and k < v:
					it["edges"].append((j-u+1, k-u+1, d))
					it["m"] += 1

		h.append(it)

	return h

def main():
	n, m = map(int, input().split())

	prune_edges = []
	g = [[] for _ in range(n+1)]

	for _ in range(m):
		a, b, c = input().split()
		a = int(a)
		b = int(b)
		c = float(c)

		g[a].append((b, c))
		g[b].append((a, c))
		if a + 3 < b:
			prune_edges.append((a, b, c))


	h = SplitInstance(n, g, prune_edges)

	for it in h:
		PrintInstance(it)



if __name__ == '__main__':
	main()