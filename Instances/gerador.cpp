#include <bits/stdc++.h>

using namespace std;

int sorteia(int min, int max){
	return rand()%(max-min + 1) + min;
}

int main(int argc, char const *argv[]){
	if(argc != 6) return 0;

	int c; sscanf(argv[1], "%d", &c);
	int n; sscanf(argv[2], "%d", &n);
	int m; sscanf(argv[3], "%d", &m);
	int t; sscanf(argv[4], "%d", &t);
	int K; sscanf(argv[5], "%d", &K);

	for(int cont=0;cont<c;cont++){
		int a = sorteia(1, n >> 1);
		int b = sorteia(n >> 1, n);
		sorteia(a, b);
	}

	printf("%d %d %d\n", n, m, K);

	for(int count = 0; count < m; count++){
		int i = sorteia(1, n-(K+1+t));
		int j = sorteia(i+K+1+t, n);

		printf("%d %d\n", i, j);
	}

	return 0;
}