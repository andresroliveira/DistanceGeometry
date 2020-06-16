import numpy as np 
import copy
from math import cos, sin, acos, sqrt

def TrocaSinal(s, piv):
	t = copy.deepcopy(s)

	for i in range(piv, len(t)):
		t[i] = 1 - t[i]

	return t

def EncontraCaminhos(sol, S):
        tree = [0 for _ in range(2**(len(S) + 1))]
        tree[1] = copy.deepcopy(sol)

        piv = 0
        k = 0
        for i in range(1, 2**len(S)):
                if 2**k == i:
                        piv = S[k]
                        k += 1
                tree[2*i] = copy.deepcopy(tree[i])
                tree[2*i + 1] = copy.deepcopy(TrocaSinal(tree[i], piv))

        return tree[2**len(S):2**(len(S)+1)]


def main():
	n, ns = map(int, input().split())
	s = [a for a in map(int, input().split())]
	sol = [0]+[a for a in map(int, input().split())]

	branches = EncontraCaminhos(sol, s)
	branches.sort()
	for i in range(len(branches)):
		print(branches[i][1:n+1])

if __name__ == '__main__':
	main()
